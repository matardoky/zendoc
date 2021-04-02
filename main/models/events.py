from dateutil import rrule
import uuid as uuid_lib

from django.db import models

from main.models.authenticate import User
from main.models.rules import Rule
from main.models.calendars import Calendar, Motif
from main.models.utils import OccurrenceReplacer

from rest_framework import serializers

freq_dict_order = {
    "YEARLY": 0,
    "MONTHLY": 1,
    "WEEKLY": 2,
    "DAILY": 3,
    "HOURLY": 4,
    "MINUTELY": 5,
    "SECONDLY": 6,
}
param_dict_order = {
    "byyearday": 1,
    "bymonth": 1,
    "bymonthday": 2,
    "byweekno": 2,
    "byweekday": 3,
    "byhour": 4,
    "byminute": 5,
    "bysecond": 6,
}

class Event(models.Model):
    calendar= models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start= models.DateTimeField(db_index=True)
    end= models.DateTimeField(db_index=True)
    creator= models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="creator"
    )
    end_recurring_period= models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)
    rule= models.ForeignKey(
        Rule, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    uuid= models.UUIDField(db_index=True, default= uuid_lib.uuid4, editable=True)


    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600

    def get_occurrences(self, start, end, clear_prefetch=True):
       
        if clear_prefetch:
            self.occurrence_set._remove_prefetched_objects()

        persisted_occurrences = self.occurrence_set.all()
        occ_replacer = OccurrenceReplacer(persisted_occurrences)
        occurrences = self._get_occurrence_list(start, end)
        final_occurrences = []
        for occ in occurrences:
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)
                if p_occ.start < end and p_occ.end >= start:
                    final_occurrences.append(p_occ)
            else:
                final_occurrences.append(occ)
        
        final_occurrences += occ_replacer.get_additional_occurrences(start, end)
        return final_occurrences

    def get_rrule_object(self, tzinfo):
        if self.rule is None:
            return
        params = self._event_params()
        frequency = self.rule.rrule_frequency()
        if timezone.is_naive(self.start):
            dtstart = self.start
        else:
            dtstart = tzinfo.normalize(self.start).replace(tzinfo=None)

        if self.end_recurring_period is None:
            until = None
        elif timezone.is_naive(self.end_recurring_period):
            until = self.end_recurring_period
        else:
            until = tzinfo.normalize(
                self.end_recurring_period.astimezone(tzinfo)
            ).replace(tzinfo=None)

        return rrule.rrule(frequency, dtstart=dtstart, until=until, **params)

    def _create_occurrence(self, start, end=None):
        if end is None:
            end = start + (self.end - self.start)
        return Occurrence(
            event=self, start=start, end=end, original_start=start, original_end=end
        )

    def get_occurrence(self, date):
        use_naive = timezone.is_naive(date)
        tzinfo = timezone.utc
        if timezone.is_naive(date):
            date = timezone.make_aware(date, timezone.utc)
        if date.tzinfo:
            tzinfo = date.tzinfo
        rule = self.get_rrule_object(tzinfo)
        if rule:
            next_occurrence = rule.after(
                tzinfo.normalize(date).replace(tzinfo=None), inc=True
            )
            next_occurrence = tzinfo.localize(next_occurrence)
        else:
            next_occurrence = self.start
        if next_occurrence == date:
            try:
                return Occurrence.objects.get(event=self, original_start=date)
            except Occurrence.DoesNotExist:
                if use_naive:
                    next_occurrence = timezone.make_naive(next_occurrence, tzinfo)
                return self._create_occurrence(next_occurrence)

    def _get_occurrence_list(self, start, end):
      
        if self.rule is not None:
            duration = self.end - self.start
            use_naive = timezone.is_naive(start)
            tzinfo = timezone.utc
            if start.tzinfo:
                tzinfo = start.tzinfo

            occurrences = []
            if self.end_recurring_period and self.end_recurring_period < end:
                end = self.end_recurring_period

            start_rule = self.get_rrule_object(tzinfo)
            start = start.replace(tzinfo=None)
            if timezone.is_aware(end):
                end = tzinfo.normalize(end).replace(tzinfo=None)

            o_starts = []

            closest_start = start_rule.before(start, inc=False)
            if closest_start is not None and closest_start + duration > start:
                o_starts.append(closest_start)

            occs = start_rule.between(start, end, inc=True)
            
            if len(occs) > 0:
                if occs[-1] == end:
                    occs.pop()
            o_starts.extend(occs)

            for o_start in o_starts:
                o_start = tzinfo.localize(o_start)
                if use_naive:
                    o_start = timezone.make_naive(o_start, tzinfo)
                o_end = o_start + duration
                occurrence = self._create_occurrence(o_start, o_end)
                if occurrence not in occurrences:
                    occurrences.append(occurrence)
            return occurrences
        else:
            if self.start < end and self.end > start:
                return [self._create_occurrence(self.start)]
            else:
                return []

    def _occurrences_after_generator(self, after=None):
   
        tzinfo = timezone.utc
        if after is None:
            after = timezone.now()
        elif not timezone.is_naive(after):
            tzinfo = after.tzinfo
        rule = self.get_rrule_object(tzinfo)
        if rule is None:
            if self.end > after:
                yield self._create_occurrence(self.start, self.end)
            return
        date_iter = iter(rule)
        difference = self.end - self.start
        loop_counter = 0
        for o_start in date_iter:
            o_start = tzinfo.localize(o_start)
            o_end = o_start + difference
            if o_end > after:
                yield self._create_occurrence(o_start, o_end)

            loop_counter += 1

    def occurrences_after(self, after=None, max_occurrences=None):
     
        if after is None:
            after = timezone.now()
        occ_replacer = OccurrenceReplacer(self.occurrence_set.all())
        generator = self._occurrences_after_generator(after)
        trickies = list(
            self.occurrence_set.filter(
                original_start__lte=after, start__gte=after
            ).order_by("start")
        )
        for index, nxt in enumerate(generator):
            if max_occurrences and index > max_occurrences - 1:
                break
            if len(trickies) > 0 and (nxt is None or nxt.start > trickies[0].start):
                yield trickies.pop(0)
            yield occ_replacer.get_occurrence(nxt)

    @property
    def event_start_params(self):
        start = self.start
        params = {
            "byyearday": start.timetuple().tm_yday,
            "bymonth": start.month,
            "bymonthday": start.day,
            "byweekno": start.isocalendar()[1],
            "byweekday": start.weekday(),
            "byhour": start.hour,
            "byminute": start.minute,
            "bysecond": start.second,
        }
        return params

    @property
    def event_rule_params(self):
        return self.rule.get_params()

    def _event_params(self):
        freq_order = freq_dict_order[self.rule.frequency]
        rule_params = self.event_rule_params
        start_params = self.event_start_params
        event_params = {}

        if len(rule_params) == 0:
            return event_params

        for param in rule_params:
            if (
                param in param_dict_order
                and param_dict_order[param] > freq_order
                and param in start_params
            ):
                sp = start_params[param]
                if sp == rule_params[param] or (
                    hasattr(rule_params[param], "__iter__") and sp in rule_params[param]
                ):
                    event_params[param] = [sp]
                else:
                    event_params[param] = rule_params[param]
            else:
                event_params[param] = rule_params[param]

        return event_params

    @property
    def event_params(self):
        event_params = self._event_params()
        start = self.effective_start
        empty = False
        if not start:
            empty = True
        elif self.end_recurring_period and start > self.end_recurring_period:
            empty = True
        return event_params, empty

    @property
    def effective_start(self):
        if self.pk and self.end_recurring_period:
            occ_generator = self._occurrences_after_generator(self.start)
            try:
                return next(occ_generator).start
            except StopIteration:
                pass
        elif self.pk:
            return self.start
        return None

    @property
    def effective_end(self):
        if self.pk and self.end_recurring_period:
            params, empty = self.event_params
            if empty or not self.effective_start:
                return None
            elif self.end_recurring_period:
                occ = None
                occ_generator = self._occurrences_after_generator(self.start)
                for occ in occ_generator:
                    pass
                return occ.end
        elif self.pk:
            return datetime.datetime.max
        return None

class Occurrence(models.Model):

    class Type(models.TextChoices):
        RECCURENCE="RECCURENCE","OUVERTURE RECCURENTE", 
        EXCEPTION="EXCEPTION","OUVERTURE EXCEPTIONNELLE"

    event= models.ForeignKey(Event, on_delete=models.CASCADE, related_name="occurrences")
    start= models.DateTimeField(db_index=True)
    end= models.DateTimeField(db_index=True)
    original_start= models.DateTimeField()
    orginal_end= models.DateTimeField()
    cancelled= models.BooleanField(default=False)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)
    type= models.CharField(max_length=50, choices= Type.choices, default= Type.EXCEPTION)


    class EventSerializer(serializers.ModelSerializer):
        class Meta: 
            model: Event
            fields = ('__all__')

    class OccurrenceSerializer(serializers.ModelSerializer):
        pass
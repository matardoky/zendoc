from dateutil import rrule
from django.db import models

from .rules import Rule
from .calendars import Calendar, Motif
from .utils import OccurrenceReplacer

from rest_framework import serializers

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
    motif= models.ForeignKey(Motif, on_delete=models.CASCADE)

    def _create_occurrence(self, occ_start, occ_end=None):
        """Create an Occurrence instance"""
        if not occ_end:
            occ_end = occ_start + (self.end - self.start)
        return Occurrence(
            event=self,
            start=occ_start,
            end=occ_end,
            original_start=occ_start,
            original_end=occ_end
        )

    def _get_date_gen(self, rr, start, end):
        """Return a generator to create the start dates for occurrences"""
        date = rr.after(start)
        while end and date <= end or not(end):
            yield date
            date = rr.after(date)
    
    def get_rrule_object(self):
        if self.rule:
            params = self.rule.get_params()
            frequency = self.rule.rrule_frequency()
            return rrule.rrule(frequency, dtstart= self.start, **params)
    
    def _get_occurrence_gen(self, start, end):
        """Computes all occurrences for this event from start to end"""
        length = self.end - self.start
        if self.rule:
            if self.end_recurring_period and end and (self.end_recurring_period < end):
                end = self.end_recurring_period
            occ_start_gen = self._get_date_gen(
                self.get_rrule_object(),
                start-length,
                end
            )
            occ_start = next(occ_start_gen)
            while not end or (end and occ_start <= end):
                occ_end = occ_start + length
                yield self._create_occurrence(occ_start, occ_end)
                occ_start = next(occ_start_gen)
        else:
            if (not end or self.start < end) and self.end >= start:
                occ_start_gen = self._get_date_gen(
                    rrule.rrule(
                        "DAILY",
                        dtstart=self.start
                    ),
                    start - length,
                    self.end
                )
                try:
                    occ_start = next(occ_start_gen)
                    while not end or (end and occ_start <= end):
                        occ_end = occ_start + length
                        yield self._create_occurrence(occ_start, occ_end)
                        occ_start = next(occ_start_gen)
                except StopIteration:
                    pass
        
    def get_occurrences(self, start, end=None):
        """Returns all occurrences from start to end."""
        persistent_occurrences = self.occurrences.all()
        occ_replacer = OccurrenceReplacer(persistent_occurrences)
        occurrence_gen = self._get_occurrence_gen(start, end)
        additional_occs = occ_replacer.get_additional_occurrences(start, end)
        occ = next(occurrence_gen)
        while not end or (occ.start < end or any(additional_occs)):
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)
                if (end and p_occ.start < end) and p_occ.end >= start:
                    estimated_occ = p_occ
            else:
                estimated_occ = occ

            if any(additional_occs) and (
                    estimated_occ.start == additional_occs[0].start):
                final_occ = additional_occs.pop(0)
            else:
                final_occ = estimated_occ
            if not final_occ.cancelled:
                yield final_occ
            occ = next(occurrence_gen)

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
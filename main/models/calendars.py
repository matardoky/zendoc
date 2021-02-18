from dateutil import rrule
from django.db import models

from .authenticate import Company, User
from .rules import Rule
from .utils import OccurrenceReplacer

class Address(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE
    )

class Speciality(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Base(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Motif(models.Model): 

    class Type(models.TextChoices):
        NEW="NEW","NOUVEAU PATIENT",
        FOLLOWED="FOLLOWED", "PATIENT SUIVI",
        ALL="ALL", "TOUTES GATEGORIES"

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    duration= models.TimeField()
    duration_max= models.TimeField()
    duration_min= models.TimeField()
    reservable= models.BooleanField(default=True)
    type= models.CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.ALL
    )
    color= models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
        """Returns the rrule object for this ``Event``."""
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
        # get persistent occurrences
        persistent_occurrences = self.occurrences.all()

        # setup occ_replacer with p_occs
        occ_replacer = OccurrenceReplacer(persistent_occurrences)

        # compute own occurrences according to rule that overlap with the
        # period
        occurrence_gen = self._get_occurrence_gen(start, end)
        # get additional occs, that we need to take into concern
        additional_occs = occ_replacer.get_additional_occurrences(
            start, end)
        occ = next(occurrence_gen)
        while not end or (occ.start < end or any(additional_occs)):
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)

                # if the persistent occ falls into the period, replace it
                if (end and p_occ.start < end) and p_occ.end >= start:
                    estimated_occ = p_occ
            else:
                # if there is no persistent match, use the original occ
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
        RECCURENCE="RECCURENCE"," OUVERTURE RECCURENTE", 
        EXCEPTION="EXCEPTION", "OUVERTURE EXCEPTIONNELLE"

    event= models.ForeignKey(Event, on_delete=models.CASCADE)
    start= models.DateTimeField(db_index=True)
    end= models.DateTimeField(db_index=True)
    original_start= models.DateTimeField()
    orginal_end= models.DateTimeField()
    cancelled= models.BooleanField(default=False)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)
    type= models.CharField(
        max_length=50,
        choices= Type.choices,
        default= Type.EXCEPTION
    )
    


    


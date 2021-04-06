from dateutil.rrule import (
    MO,
    TH,
    WE,
    TU,
    FR,
    SA,
    SU,
    YEARLY,
    MONTHLY,
    WEEKLY,
    DAILY,
    HOURLY,
    MINUTELY,
    SECONDLY
)
import uuid as uuid_lib


from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from main.models.authenticate import Company, User


class Rule(models.Model):

    class Freqs(models.TextChoices):
        YEARLY="YEARLY", _("Yearly"),
        MONTHLY="MONTHLY", _("Monthly"),
        WEEKLY="WEEKLY", _("Weekly"),
        DAILY="DAILY", _("Daily"),
        HOURLY="HOURLY", _("Hourly"),
        MINUTELY="MINUTELY", _("Minutely"),
        SECONDLY="SECONDLY", _("Secondly")

    uuid= models.UUIDField(db_index=True, default= uuid_lib.uuid4, editable=True)
    frequency= models.CharField(
        max_length=50, 
        choices=Freqs.choices, 
        default=Freqs.WEEKLY,
        null=True
    )
    params= models.TextField(blank=True)
    _week_day= {"MO": MO, "TU": TU, "WE": WE, "TH": TH, "FR": FR, "SA": SA, "SU": SU}

    company= models.ForeignKey(
        Company,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )

    def rrule_frequency(self):
        compatibility_dict= {
            
            "YEARLY": YEARLY,
            "MONTHLY": MONTHLY,
            "WEEKLY": WEEKLY, 
            "DAILY": DAILY, 
            "HOURLY": HOURLY,
            "MINUTELY": MINUTELY,
            "SECONDLY": SECONDLY,
        }
        return compatibility_dict[self.frequency]

    def _weekday_or_number(self, param):
        try:
            return int(param)
        except:
            uparam = str(param).upper()
            if uparam in Rule._week_day:
                return Rule._week_day[uparam]
    
    def get_params(self):
        params = self.params.split(";")
        param_dict = []
        for param in params:
            param = param.split(":")
            if len(param) != 2:
                continue

            param = (
                str(param[0]).lower(),
                [
                    x
                    for x in [self._weekday_or_number(v) for v in param[1].split(",")]
                    if x is not None
                ],
            )

            if len(param[1]) == 1:
                param_value = self._weekday_or_number(param[1][0])
                param = (param[0], param_value)
            param_dict.append(param)
        return dict(param_dict)

    def __str__(self):
        return "Rule {} params {}".format(self.frequency, self.params)
    




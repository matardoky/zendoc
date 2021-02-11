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

from django.db import models
from django.utils.translation import gettext_lazy as _

from .authenticate import Company

class Rule(models.Model):

    class Freqs(models.TextChoices):
        YEARLY="YEARLY", _("Yearly"),
        MONTHLY="MONTHLY", _("Monthly"),
        WEEKLY="WEEKLY", _("Weekly"),
        DAILY="DAILY", _("Daily"),
        HOURLY="HOURLY", _("Hourly"),
        MINUTELY="MINUTELY", _("Minutely"),
        SECONDLY="SECONDLY", _("Secondly")

    frequency= models.CharField(
        max_length=50, 
        choices=Freqs.choices, 
        default=Freqs.WEEKLY 
    )
    params= models.TextField(blank=True)
    _week_day= {"MO": MO, "TU": TU, "WE": WE, "TH": TH, "FR": FR, "SA": SA, "SU": SU}

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE
    )

    def rrule_frequency(self):
        compatibility_dict = {
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
        pass


    



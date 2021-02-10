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

class Rule(models.Model):

    class Freqs(models.TextChoices):
        pass

    pass


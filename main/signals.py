import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.events import Event

logger = logging.getLogger(__name__)

@receiver(pre_save, sender= Event)
def event_type(sender, instance, **kwargs):
    if instance.rule is None:
        logger.info(
            "OUVERTURE EXECEPTIONELLE",
            instance.rule
        )
        instance.type = Event.Type.EXCEPTION
        
        
        

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Field, Actions

@receiver(post_delete, sender=Field)
def delete_field_property(sender, instance, **kwargs):
    if instance.properties:
        instance.properties.delete()


@receiver(post_delete, sender=Actions)
def delete_action_property(sender, instance, **kwargs):
    print('signal recieves')
    if instance.condition:
        print('deleting')
        instance.condition.delete()
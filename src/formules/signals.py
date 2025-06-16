from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=User)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        patient_group, _ = Group.objects.get_or_create(name='Patient')
        instance.groups.add(patient_group)


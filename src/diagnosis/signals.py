from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_migrate)
def create_defaults(sender, **kwargs):
    Group.objects.get_or_create(name='Врач')
    Group.objects.get_or_create(name='Пациент')

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', email='admin', password='admin')
        print("✅ Суперпользователь 'admin' создан.")

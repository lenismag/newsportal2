from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    group, created = Group.objects.get_or_create(name='common')
    user.groups.add(group)
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # MEDIA_ROOT/user_<id>/<filename>
    return 'upload/user_{0}/{1}'.format(instance.system_user.id, filename)


class Account(models.Model):
    system_user = models.OneToOneField('auth.User', on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, default=None)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(system_user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()

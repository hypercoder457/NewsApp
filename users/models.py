from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField

from users.manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={'unique': 'That email is already taken.'}
    )

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return "%s %s" % (self.first_name, self.last_name)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = ResizedImageField(upload_to='avatars', blank=True)
    about = models.TextField('About me', blank=True)

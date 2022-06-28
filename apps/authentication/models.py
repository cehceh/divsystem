from django.db import models
import os
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def avatar_path(instance, filename):
    file_name, ext = get_filename_ext(filename)
    file_ext = '{ext}'.format(ext=ext)

    first_name = instance.first_name
    phone = instance.phone_number
    
    image_path = 'users/{0}/{1}{2}'.format(
            phone, (first_name + '_'), file_ext
    )
    
    return image_path




class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=30, unique=True)
    country_code = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20, default='2015-01-01')
        
    CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[1][0])
    avatar = models.ImageField(
        upload_to=avatar_path,
        default="", 
        verbose_name=_("Avatar *")
    )

    verified = models.BooleanField(_("Verified"), default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        email = self.email
        username = self.username
        phone_number = self.phone_number
        if bool(email) == False:
            self.email = self.password[:10]
        if bool(username) == False:
            self.username = self.password[:10]
        if bool(phone_number) == False:
            self.phone_number = self.password[:10]
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.username)



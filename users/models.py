from django.db import models
from django.contrib.auth.models import AbstractUser

import os

def get_upload_path(instance, filename):
        return os.path.join(f'{instance.last_name.lower()}-{instance.first_name.lower()}', filename)


class CustomUser(AbstractUser):
    '''Custom user model that extends django's default user class.'''

    # Custom user fields
    date_of_birth = models.DateField(
        null=True,
        help_text='yyyy-mm-dd'
        )
    birthplace = models.CharField(
        max_length=255, 
        null=True, 
        help_text='City, State'
        )
    picture = models.ImageField(
        upload_to=get_upload_path,
        blank=True, 
        null=True,
        help_text = 'Landscape photos work best!'
        )
    slug = models.SlugField(
        null=True, 
        blank=False
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

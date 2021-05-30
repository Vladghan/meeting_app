import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from meetapp.settings import WATERMARK_URL


class Member(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    GENDER_CHOICES = (
        ('м', 'муж'),
        ('ж', 'жен')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        photo = self.photo
        if photo:
            img = Image.open(photo)
            watermark = Image.open(WATERMARK_URL)
            img.paste(watermark, (0, 0), watermark)
            filestream = BytesIO()
            img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.photo.name.split('.'))
            self.photo = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)


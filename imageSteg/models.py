from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class ImageEncoding(models.Model):
    image_file = models.FileField(upload_to='images/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["png", "jpg","jpeg"])])
    message = models.CharField(max_length = 80, null = True, blank = True)

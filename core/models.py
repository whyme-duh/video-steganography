from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Encoding(models.Model):
    file = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
    message = models.CharField(max_length = 80, null = True, blank = True)
    encoded_file = models.FileField(upload_to='videos/', null = True )
    user = models.ForeignKey(User, on_delete = models.CASCADE, null =True)
    changed_frame_after_encoding = models.CharField(max_length=10000, null= True, blank = True)

   


class Decoding(models.Model):
    file = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
  
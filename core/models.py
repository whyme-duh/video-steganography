from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Encoding(models.Model):
    video = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
    message = models.CharField(max_length = 80, null = True, blank = True)
    encoded_file = models.FileField(upload_to='encoded/', null = True )
    user = models.ForeignKey(User, on_delete = models.CASCADE, null =True)
    changed_frame_after_encoding = ArrayField(ArrayField(models.CharField(max_length= 1000, blank = True, null=True), size =8,),size =8, null=True)

   


class Decoding(models.Model):
    video = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
  
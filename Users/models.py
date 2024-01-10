from django.db import models
from core.models import Encoding
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)  


    
    

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
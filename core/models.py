# from django.db import models
# from django.core.validators import FileExtensionValidator
# from django.contrib.auth.models import User

# class Encoding(models.Model):
#     video = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["AVI"])])
#     secret_key = models.CharField(max_length = 10, null = True, blank = True)
#     frame_number = models.IntegerField(null = True, blank = True)
#     message = models.CharField(max_length = 80, null = True, blank = True)
#     encoded_file = models.FileField(upload_to='encoded/', null = True )
#     user = models.ForeignKey(User, on_delete = models.CASCADE, null =True)
#     encoded_file_name = models.CharField(max_length = 20, null = True, blank = True)
    

   


# class Decoding(models.Model):
#     video = models.FileField(upload_to='decoded/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["AVI"])])
#     secret_key = models.CharField(max_length = 10, null = True, blank = True)

  
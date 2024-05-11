from django import forms
from .models import ImageEncoding
from django.core.validators import FileExtensionValidator


class ImageEncodeForm(forms.ModelForm):
    class Meta:
        model = ImageEncoding
        fields = ["image_file",  'message']

    message = forms.CharField(required=True, max_length=80)
    

class DecodeForm(forms.Form):
    encoded_image = forms.FileField( validators=[FileExtensionValidator(allowed_extensions=["png", "jpg","jpeg"])])



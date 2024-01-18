from django import forms
from . models import Encoding, Decoding
from django.core.validators import FileExtensionValidator

class EncodeForm(forms.ModelForm):
    class Meta:
        model = Encoding
        fields = ["video", 'frame_number', 'secret_key', 'message']

    frame_number = forms.IntegerField(required=True)
    secret_key = forms.CharField(required=True)
    message = forms.CharField(required=True)
    encoded_file_name = forms.CharField(required=True, help_text='Enter the file name for encoded file')

class DecodeForm(forms.ModelForm):
    # video = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["MP4", "AVI"])])
    # frame_number = forms.IntegerField(required=True)
    # secret_key = forms.CharField(required=True)
    # encoded_filename = forms.CharField(required=True)
    class Meta:
        model = Encoding
        fields = ["video", 'secret_key']

    secret_key = forms.CharField(required=True)
from django import forms
from . models import Encoding, Decoding
from django.core.validators import FileExtensionValidator

class EncodeForm(forms.ModelForm):
    class Meta:
        model = Encoding
        fields = ["video", 'secret_key', 'message', 'encoded_file_name']

    secret_key = forms.CharField(required=True ,max_length=10)
    message = forms.CharField(required=True, max_length=80)
    encoded_file_name = forms.CharField(required=True, max_length=20)
    video = forms.FileField(required= True, validators=[FileExtensionValidator(allowed_extensions=["AVI"])])


    def clean(self):
        super(EncodeForm, self).clean()
        secret_key = self.cleaned_data.get('secret_key')
        message = self.cleaned_data.get('message')
        encoded_file_name = self.cleaned_data.get('encoded_file_name')
        if (len(secret_key) >= 10):
           raise forms.ValidationError("Secret key should not exceed 10 characters")
        if (len(message) > 50):
            self._errors['message'] = self.error_class(['The message should not be more than 50 characters'])
        if (encoded_file_name.endswith('.mp4') or encoded_file_name.endswith('.avi') or encoded_file_name.endswith('.png') or 
            encoded_file_name.endswith('.jpg') or encoded_file_name.endswith('.jpeg') or encoded_file_name.endswith('.mkv')):
            self._errors['encoded_file_name'] = self.error_class(['The filename should not have any extension.'])
        
        return self.cleaned_data

class DecodeForm(forms.ModelForm):
    # video = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["MP4", "AVI"])])
    # frame_number = forms.IntegerField(required=True)
    # secret_key = forms.CharField(required=True)
    # encoded_filename = forms.CharField(required=True)
    class Meta:
        model = Decoding
        fields = ["video", 'secret_key']

    secret_key = forms.CharField(required=True ,max_length=10)
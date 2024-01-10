from django import forms
from . models import Encoding, Decoding

class EncodeForm(forms.ModelForm):
    class Meta:
        model = Encoding
        fields = ["file", 'frame_number', 'secret_key', 'message']

    frame_number = forms.IntegerField(required=True)
    secret_key = forms.CharField(required=True)
    message = forms.CharField(required=True)


class DecodeForm(forms.ModelForm):
    class Meta:
        model = Decoding
        fields = ['file','frame_number', 'secret_key']

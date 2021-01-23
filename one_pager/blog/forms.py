from django.forms import ModelForm
from .models import AudioFile

class AuditForm(ModelForm):
    class Meta:
        model = AudioFile
        fields = ['checked_status', 'verified_status']

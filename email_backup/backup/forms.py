from django import forms
from .models import EmailConfig

class EmailConfigForm(forms.ModelForm):
    class Meta:
        model = EmailConfig
        fields = ['email', 'server', 'port', 'username', 'password', 'protocol']

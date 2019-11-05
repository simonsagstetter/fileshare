from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.forms.widgets import TextInput, Select

from files.models import File

class MultiUploadForm(forms.ModelForm):

    class Meta:
        model = File
        fields = [
            'upload_file',
        ]

class FileUpdateForm(forms.ModelForm):
    real_filename = forms.CharField(
        label=_('New file name'),
        max_length=60,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control form-control', 'placeholder': _('New file name')}),
    )

    class Meta:
        model = File
        fields = [
            'real_filename',
        ]

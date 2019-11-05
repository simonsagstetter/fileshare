from django import forms
from django.forms.widgets import TextInput, Select
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

from libary.models import Folder

class FolderCreationForm(forms.Form):
    folder_name = forms.CharField(
        label=_('Folder name'),
        max_length=60,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': _('Folder name')}),
    )

class SubfolderCreationForm(forms.Form):
    folder_name = forms.CharField(
        label=_('Folder name'),
        max_length=60,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': _('Folder name')}),
    )

class FolderUpdateForm(forms.ModelForm):
    folder_name = forms.CharField(
        label=_('New folder name'),
        max_length=60,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control form-control', 'placeholder': _('New folder name')}),
    )

    class Meta:
        model = Folder
        fields = [
            'folder_name',
        ]

class FolderMoveForm(forms.ModelForm):
    related_folder = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        empty_label=_('None'),
        to_field_name='folder_name',
        label=_('New folder'),
        widget=forms.Select(attrs={'autofocus': True, 'class': 'form-control form-control'}),
    )

    class Meta:
        model = Folder
        fields = ['related_folder', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        id = self.request.user.id
        self.fields['related_folder'].queryset = Folder.objects.filter(created_by=id)

class FolderChangeOwnerForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=_('None'),
        to_field_name='email',
        label=_('New owner'),
        widget=forms.Select(attrs={'autofocus': True, 'class': 'form-control form-control'}),
    )

    class Meta:
        model = Folder
        fields = ['created_by', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        id = self.request.user.id
        self.fields['created_by'].queryset = User.objects.all().exclude(id=id)

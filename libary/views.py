from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _

from files.models import File
from files.forms import (
FileUpdateForm,
)
from libary.models import Folder
from libary.forms import (
FolderCreationForm,
SubfolderCreationForm,
FolderUpdateForm,
FolderMoveForm,
FolderChangeOwnerForm,
)

from libary.functions import get_folder_size

class Folders(TemplateView):
    template_name = 'libary/folders.html'

    def get(self, request):
        folders = Folder.objects.filter(related_folder__isnull=True, is_deleted=False, created_by=request.user)
        files = File.objects.filter(related_folder__isnull=True, is_deleted=False, created_by=request.user)

        form = FolderCreationForm(request.GET or None)
        update_folder = FolderUpdateForm(request.GET or None)
        move_folder = FolderMoveForm(request.GET or None, request=request)
        change_owner = FolderChangeOwnerForm(request.GET or None, request=request)
        update_file = FileUpdateForm(request.GET or None)

        args = {'folders': folders, 'form': form, 'update_folder': update_folder, 'move_folder': move_folder, 'change_owner': change_owner, 'files': files, 'update_file': update_file}

        return render(request, self.template_name, args)

class Subfolders(TemplateView):
    template_name = 'libary/subfolders.html'

    def get(self, request, pk):
        parent_folder = Folder.objects.get(pk=pk)

        subfolders = Folder.objects.filter(related_folder=pk, is_deleted=False, created_by=request.user)
        files = File.objects.filter(related_folder=pk, is_deleted=False, created_by=request.user)

        form = SubfolderCreationForm(request.GET or None)
        update_folder = FolderUpdateForm(request.GET or None)
        move_folder = FolderMoveForm(request.GET or None, request=request)

        args = {'subfolders': subfolders, 'parent_folder': parent_folder, 'form': form, 'update_folder': update_folder, 'move_folder': move_folder, 'files': files}

        return render(request, self.template_name, args)

def create_folder_view(request):
    form = FolderCreationForm(request.POST or None)
    if form.is_valid():
        folder_name = form.cleaned_data['folder_name']
        created_by = request.user
        Folder.objects.create_folder(folder_name=folder_name, created_by=created_by)

        return redirect('libary:folders')

def create_subfolder_view(request, id):
    form = SubfolderCreationForm(request.POST or None)
    if form.is_valid():
        folder_name = form.cleaned_data['folder_name']
        created_by = request.user
        related_folder = Folder.objects.get(pk=id)
        Folder.objects.create_subfolder(folder_name=folder_name, created_by=created_by, related_folder=related_folder)

        return redirect('libary:subfolders', pk=id)

def update_folder_view(request, id):
    form = FolderUpdateForm(request.POST or None)
    if form.is_valid():
        folder_name = form.cleaned_data['folder_name']
        Folder.objects.update_folder(id=id, folder_name=folder_name)

        folder = Folder.objects.get(pk=id)
        try:
            isParentFolder = folder.related_folder.id
            return redirect('libary:subfolders', pk=str(isParentFolder))
        except:
            return redirect('libary:folders')

def move_folder_view(request, id):
    form = FolderMoveForm(request.POST or None, request=request)
    if form.is_valid():
        related_folder = form.cleaned_data['related_folder']
        if str(id) == str(related_folder.id):
            messages.error(request, _('You can not move a folder to itself!'))
            return redirect('libary:folders')
        else:
            Folder.objects.move_folder(id=id, related_folder=related_folder)
            return redirect('libary:subfolders', pk=related_folder.id)

def promote_folder_view(request, id):
    Folder.objects.promote_folder(id=id)

    return redirect('libary:folders')

def change_owner_view(request, id):
    form = FolderChangeOwnerForm(request.POST or None, request=request)
    if form.is_valid():
        created_by = form.cleaned_data['created_by']
        Folder.objects.change_folder_owner(id=id, created_by=created_by)

        return redirect('libary:folders')

def delete_folder_view(request, id):
    Folder.objects.delete_folder(id=id)

    return redirect('libary:folders')

def delete_subfolder_view(request, id):
    instance = Folder.objects.get(id=id)
    redirect_id = str(instance.related_folder.id)
    Folder.objects.delete_folder(id=id)

    return redirect('libary:subfolders', pk=redirect_id)

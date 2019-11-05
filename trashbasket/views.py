from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _

from libary.models import Folder
from files.models import File

class TrashBasket(TemplateView):
    template_name = 'trashbasket/trash_basket.html'

    def get(self, request):
        folders = Folder.objects.filter(is_deleted=True, created_by=request.user)
        files = File.objects.filter(is_deleted=True, created_by=request.user)

        args = {'folders': folders, 'files': files}

        return render(request, self.template_name, args)

''' Actions for Folders '''

def restore_folder_view(request, id):
    Folder.objects.restore_folder(id=id)

    return redirect('trashbasket:object-list')

def restore_all_view(request):
    Folder.objects.restore_all()
    File.objects.restore_all()

    return redirect('trashbasket:object-list')

def remove_folder_view(request, id):
    Folder.objects.remove_folder(id=id)

    return redirect('trashbasket:object-list')

def remove_all_view(request):
    Folder.objects.remove_all()
    File.objects.remove_all()

    return redirect('trashbasket:object-list')

''' Actions for Files '''

def restore_file_view(request, id):
    File.objects.restore_file(id=id)

    return redirect('trashbasket:object-list')

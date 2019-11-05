from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from files.forms import MultiUploadForm, FileUpdateForm
from files.models import File
from libary.models import Folder

User = get_user_model()

def Upload(request):
    if request.method == 'POST':
        form = MultiUploadForm(request.POST, request.FILES)
        if form.is_valid():
            created_by = request.user
            upload_file = request.FILES.get('upload_file')
            name = upload_file.name
            real_filename = name.split('.')[0]
            file = File.objects.upload_file(real_filename=real_filename, upload_file=upload_file, related_folder=None, created_by=created_by)
            data = {'is_valid': True, 'name': file.real_filename, 'url': file.upload_file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return redirect('libary:folders')

def UploadWithID(request, id):
    if request.method == 'POST':
        form = MultiUploadForm(request.POST, request.FILES)
        if form.is_valid():
            created_by = request.user
            upload_file = request.FILES.get('upload_file')
            name = upload_file.name
            real_filename = name.split('.')[0]
            related_folder = Folder.objects.get(id=id)
            file = File.objects.upload_file(real_filename=real_filename, upload_file=upload_file, related_folder=related_folder, created_by=created_by)
            data = {'is_valid': True, 'name': file.real_filename, 'url': file.upload_file.url, 'id': file.related_folder.id}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return redirect('libary:folders')

def UploadSuccess(request):
    id = File.objects.filter(created_by=request.user.id, is_deleted=0).latest('related_folder')
    return redirect('libary:subfolders', pk=id.related_folder.id)

def update_file_view(request, id):
    form = FileUpdateForm(request.POST or None)
    if form.is_valid():
        real_filename = form.cleaned_data['real_filename']
        File.objects.update_file(id=id, real_filename=real_filename)

        folder = File.objects.get(pk=id)
        try:
            isParentFolder = folder.related_folder.id
            return redirect('libary:subfolders', pk=str(isParentFolder))
        except:
            return redirect('libary:folders')

def delete_file_view(request, id):
    File.objects.delete_file(id=id)

    return redirect('libary:folders')

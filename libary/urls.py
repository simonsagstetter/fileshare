from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

from libary.views import (
Folders,
Subfolders,
create_folder_view,
delete_folder_view,
create_subfolder_view,
update_folder_view,
move_folder_view,
promote_folder_view,
change_owner_view,
delete_subfolder_view,
)

app_name = 'libary'

urlpatterns = [
    path('', login_required(RedirectView.as_view(url='/folders/')) ),
    path('folders/', login_required(Folders.as_view()), name='folders' ),
    path('folders/create/folder/', login_required(create_folder_view), name='create-folder'),
    path('folders/delete/folder/<id>/', login_required(delete_folder_view), name='delete-folder' ),
    path('folders/update/<id>/', login_required(update_folder_view), name='update-folder'),
    path('folders/move/<id>/', login_required(move_folder_view), name='move-folder'),
    path('folders/promote/<id>/', login_required(promote_folder_view), name='promote-folder'),
    path('folders/change-owner/<id>/', login_required(change_owner_view), name='change-owner'),
    path('folders/<pk>/', login_required(Subfolders.as_view()), name='subfolders' ),
    path('folders/create/subfolder/<id>/', login_required(create_subfolder_view), name='create-subfolder' ),
    path('folders/delete/subfolder/<id>/', login_required(delete_subfolder_view), name='delete-subfolder' ),
]

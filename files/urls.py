from django.urls import path
from django.contrib.auth.decorators import login_required

from files.views import (
Upload,
UploadWithID,
UploadSuccess,
delete_file_view,
update_file_view,
)

app_name = 'files'

urlpatterns = [
    path('upload/', login_required(Upload), name='upload' ),
    path('upload-in/<id>/', login_required(UploadWithID), name='upload' ),
    path('upload-success/', login_required(UploadSuccess), name='upload-success' ),
    path('delete/<id>/', login_required(delete_file_view), name='delete-file' ),
    path('update/<id>/', login_required(update_file_view), name='update-file'),
]

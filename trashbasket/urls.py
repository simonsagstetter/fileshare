from django.urls import path
from django.contrib.auth.decorators import login_required

from trashbasket.views import (
TrashBasket,
restore_folder_view,
restore_all_view,
remove_folder_view,
remove_all_view,
restore_file_view,
)

app_name = 'trashbasket'

urlpatterns = [
    path('', login_required(TrashBasket.as_view()), name='object-list' ),
    path('restore/folder/<id>/', login_required(restore_folder_view), name='restore-folder' ),
    path('remove/folder/<id>/', login_required(remove_folder_view), name='remove-folder' ),
    path('restore/file/<id>/', login_required(restore_file_view), name='restore-file' ),
    path('remove-all/', login_required(remove_all_view), name='remove-all' ),
    path('restore-all/', login_required(restore_all_view), name='restore-all' ),
]

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from fileshare.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(RedirectView.as_view(url='/libary/folders/')) ),
    path('libary/', include('libary.urls', namespace='libary') ),
    path('manage/', include('manage.urls', namespace='manage') ),
    path('files/', include('files.urls', namespace='files') ),
    path('trash-basket/', include('trashbasket.urls', namespace='trashbasket') ),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

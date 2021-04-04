from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


api_endpoints = [
    url('^', include('images.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(api_endpoints)),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("upload/", views.index, name="index"),
    path('upload_image/', views.upload_image, name='upload_image'),
     path('camera/', views.camera_view, name='camera_view'),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
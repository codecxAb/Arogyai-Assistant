from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('', views.index, name='index'),
    # path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'),
]


from django.urls import path
from . import views
from . import sign

urlpatterns = [
    path('', views.index, name='index'),
    path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'), 
    path('signin/', sign.signin, name='signin'),
    path('signup/', sign.signup, name='signup'),
]


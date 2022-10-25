from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.admin_signin, name = 'ciaoadmin_signin'),
    path('eventlog/', views.event_log , name='event_log'),
]

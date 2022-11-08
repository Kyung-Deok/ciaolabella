from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='nolabel'),
    path('click/', views.click)
]
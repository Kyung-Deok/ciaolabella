from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.member_page, name='member_page'),
    path('register/', views.member_reg, name='member_reg'),
    path('login/', views.member_login, name='member_login'),
    path('logout/', views.member_logout, name='member_logout'),
]

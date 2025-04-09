from django.contrib import admin
from django.urls import path
from . import views

app_name='Home'

urlpatterns = [
    path('Home/<str:username>/',views.Home ,name='Home'),
    path('',views.Home_public_page.as_view(),name='Home'),
    path('logout/', views.logout_view, name='logout'),
]
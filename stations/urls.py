from django.urls import path
from .views import station_List_Fournisseur
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'stations'

urlpatterns = [
    path('station_List_Fournisseur/<str:username>', station_List_Fournisseur.as_view(), name='station_List_Fournisseur'),
    path('add_station/<str:username>', views.add_station, name='add_station'),
    path('delete_station/<int:ID_Station>/<str:username>', views.delete_station, name='delete_station'),
    path('update_station/<int:ID_Station>/<str:username>', views.update_station, name='update_station'),
    path('delete_photo/<int:ID_Station>/<int:photo_id>/<str:username>/', views.delete_photo, name='delete_photo'),
]


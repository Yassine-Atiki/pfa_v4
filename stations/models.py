from django.db import models
from users.models import ProprietaireVE , Fournisseur


class station(models.Model):
    username = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)
    ID_Station=models.AutoField(primary_key=True)
    adresse=models.CharField(max_length=255 , unique=True)
    puissance=models.FloatField()
    prix_kw=models.FloatField()
    disponibilite=models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    nom = models.CharField(max_length=100, default="Station de recharge")
    connector_types = models.CharField(max_length=255, blank=True, null=True)  # Ex. "Type 2, CCS"
    power = models.CharField(max_length=50, blank=True, null=True)  # Ex. "22 kW"
    operator = models.CharField(max_length=255, blank=True, null=True)  
    

class photo(models.Model):
    ID_Station= models.ForeignKey(station, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stations_photos/')  

class avi(models.Model):
    ID_Station= models.ForeignKey(station, related_name='avis', on_delete=models.CASCADE)
    username = models.ForeignKey(ProprietaireVE, on_delete=models.SET_NULL, null=True, blank=True)  
    commentaire = models.TextField()
    note = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Note entre 1 et 5
    date_ajout = models.DateTimeField(auto_now_add=True)
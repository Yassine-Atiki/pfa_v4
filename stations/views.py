from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.urls import reverse
from .models import station, photo, avi
from users.models import Fournisseur

class station_List_Fournisseur(ListView):
    model = station
    template_name = 'station_List_Fournisseur.html'

    def get(self, request, username, *args, **kwargs):
        # Filtrer les stations par le champ 'username' du modèle Fournisseur
        stations = station.objects.filter(username__username=username)  # Utilisez 'username__username'
        
        # Récupérer les photos et avis associés
        photos = photo.objects.filter(ID_Station__in=stations.values_list('ID_Station', flat=True))  
        avis = avi.objects.filter(ID_Station__in=stations.values_list('ID_Station', flat=True))
        
        # Calculer la note moyenne
        note = 0
        total_notes = 0
        for avis_obj in avis:
            note += avis_obj.note  # Assurez-vous que le champ 'note' existe dans le modèle 'avi'
            total_notes += 1
        
        note_moyenne = note / total_notes if total_notes > 0 else 0
        
        

        # Renvoyer les données au template
        return render(request, self.template_name, {
            'stations': stations,
            'photos': photos,
            'note': note_moyenne,
            'username': username,
        })

def add_station(request, username):
    F = Fournisseur.objects.get(username=username)
    if request.method == 'POST':
        adresse = request.POST.get('adresse')
        puissance = request.POST.get('puissance')
        prix_kw = request.POST.get('prix_kw')
        disponibilite = request.POST.get('disponibilite')
        photos = request.FILES.getlist('photos[]')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        nom = request.POST.get('nom')

        # Vérification des champs requis
        if not all([adresse, puissance, prix_kw, disponibilite, latitude, longitude,nom]):
            error = {'error': 'All fields are required.'}
            return render(request, 'ADD_Station.html', {'error': error, 'username': username})

        # Vérification si la station existe déjà
        if station.objects.filter(adresse=adresse).exists():
            error = {'error': 'This station already exists.'}
            return render(request, 'ADD_Station.html', {'error': error ,'username': username})

        # Création de la station
        F = Fournisseur.objects.get(username=username)
        new_station = station.objects.create(
            username=F,
            adresse=adresse,
            puissance=puissance,
            prix_kw=prix_kw,
            disponibilite=disponibilite,
            latitude=latitude,
            longitude=longitude,
            nom=nom
        )
        new_station.save()

        # Ajout des photos associées
        for photo_file in photos:
            photo.objects.create(
                ID_Station=new_station,
                image=photo_file
            )
        # Redirection après succès
        return redirect(reverse('stations:station_List_Fournisseur', kwargs={'username': username}))

    # Si la méthode est GET, afficher le formulaire
    return render(request, 'ADD_Station.html', {'username':username})

def delete_station(request, ID_Station, username):
        photos_delete= photo.objects.filter(ID_Station=ID_Station)
        for photo_obj in photos_delete:
            delete_photo(request,ID_Station=ID_Station, photo_id=photo_obj.id , username=username)
            
        avis_station_to_delete = avi.objects.filter(ID_Station=ID_Station)
        avis_station_to_delete.delete()

        station_to_delete = station.objects.get(ID_Station=ID_Station)
        station_to_delete.delete()

        return redirect(reverse('stations:station_List_Fournisseur', kwargs={'username':username}))

def update_station(request, ID_Station, username): 
    station_update = station.objects.get(ID_Station=ID_Station)
    
    if request.method == 'POST':
        adresse = request.POST.get('adresse')
        puissance = request.POST.get('puissance')
        prix_kw = request.POST.get('prix_kw')
        disponibilite = request.POST.get('disponibilite')
        photos = request.FILES.getlist('photos[]')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        nom = request.POST.get('nom')

        # Vérification des champs requis
        if not all([adresse, puissance, prix_kw, disponibilite, latitude, longitude, nom]):
            error = {'error': 'All fields are required.'}
            return render(request, 'update_station.html', {'error': error, 'station': station_update, 'username': username})

        # Mise à jour de la station
        station_update.adresse = adresse
        station_update.puissance = puissance
        station_update.prix_kw = prix_kw
        station_update.disponibilite = disponibilite
        station_update.latitude = latitude
        station_update.longitude = longitude
        station_update.nom = nom
        station_update.save()

        for photo_file in photos:
            photo.objects.create(
                ID_Station=station_update,
                image=photo_file
            )

        # Redirection après succès
        return redirect(reverse('stations:station_List_Fournisseur', kwargs={'username': username}))
    
    # Gérer la requête GET : afficher le formulaire pré-rempli
    return render(request, 'update_station.html', {'station': station_update, 'username': username})

def delete_photo(request, ID_Station, photo_id, username):
    # Suppression de la photo
    photo_to_delete = photo.objects.get(id=photo_id, ID_Station=ID_Station)
    photo_to_delete.delete()

    return redirect(reverse('stations:station_List_Fournisseur', kwargs={'username': username}))
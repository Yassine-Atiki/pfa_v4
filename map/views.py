import json
from django.shortcuts import render
from django.http import JsonResponse
from stations.models import station
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def map_view(request):
    if request.method == "POST":
        try:
            user_lat = float(request.POST.get('lat'))
            user_lon = float(request.POST.get('lon'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Coordonnées invalides'}, status=400)

        # Récupérer toutes les stations
        stations = station.objects.all()
        print(f"Nombre total de stations récupérées : {stations.count()}")  # Log

        # Renvoyer les stations avec des coordonnées valides
        nearby_stations = []
        for s in stations:
            if s.latitude is None or s.longitude is None:
                print(f"Station ignorée (coordonnées manquantes) : {s.nom}")
                continue
            try:
                lat = float(s.latitude)
                lng = float(s.longitude)
                nearby_stations.append({
                    'name': s.nom if s.nom else "Nom inconnu",
                    'lat': lat,
                    'lng': lng,
                    'address': s.adresse if s.adresse else "Adresse inconnue",
                    'connector_types': s.connector_types if s.connector_types else "Non spécifié",
                    'power': s.power if s.power else "Non spécifié",
                    'operator': s.operator if s.operator else "Opérateur inconnu",
                    'available': s.disponibilite
                })
            except (ValueError, TypeError):
                print(f"Station ignorée (coordonnées invalides) : {s.nom}, latitude={s.latitude}, longitude={s.longitude}")
                continue

        print(f"Nombre de stations valides : {len(nearby_stations)}")  # Log
        return JsonResponse({'stations': nearby_stations})

    return render(request, 'map.html', {})
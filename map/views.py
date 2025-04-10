from django.http import JsonResponse
from django.shortcuts import render
from stations.models import station

def map_view(request):
    if request.method == "POST":
        try:
            user_lat = float(request.POST.get('lat'))
            user_lon = float(request.POST.get('lon'))
            print(f"Position de l'utilisateur : lat={user_lat}, lon={user_lon}")
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Coordonnées invalides'}, status=400)

        stations = station.objects.all()
        print(f"Nombre total de stations récupérées : {stations.count()}")

        all_stations = []
        for s in stations:
            if s.latitude is None or s.longitude is None:
                print(f"Station ignorée (coordonnées manquantes) : {s.nom}")
                continue
            try:
                lat = float(s.latitude)
                lng = float(s.longitude)
                if lat < -90 or lat > 90 or lng < -180 or lng > 180:
                    print(f"Station ignorée (coordonnées hors limites) : {s.nom}, latitude={lat}, longitude={lng}")
                    continue
                available = bool(s.disponibilite) if s.disponibilite is not None else True
                all_stations.append({
                    'name': s.nom if s.nom else "Nom inconnu",
                    'lat': lat,
                    'lng': lng,
                    'address': s.adresse if s.adresse else "Adresse inconnue",
                    'connector_types': s.connector_types if s.connector_types else "Non spécifié",
                    'power': s.power if s.power else "Non spécifié",
                    'operator': s.operator if s.operator else "Opérateur inconnu",
                    'available': available,
                    'has_username': s.username is not None  # Indique si la station a un username
                })
                print(f"Station ajoutée : {s.nom}, lat={lat}, lng={lng}, available={available}, has_username={s.username is not None}")
            except (ValueError, TypeError):
                print(f"Station ignorée (coordonnées invalides) : {s.nom}, latitude={s.latitude}, longitude={s.longitude}")
                continue

        print(f"Nombre total de stations valides : {len(all_stations)}")
        return JsonResponse({'stations': all_stations})

    return render(request, 'map.html', {})
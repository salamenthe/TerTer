from django.http import JsonResponse
from django.shortcuts import render
from map.models import TrainStation

from geopy.distance import geodesic

# Create your views here.
def index(request):
    stations = list(TrainStation.objects.values('latitude','longitude'))
    print(stations[:2])
    context = {'stations':stations}
    return render(request, 'map/index.html', context)

def nearest_station(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    user_location = (latitude,longitude)
    station_distances ={}
    for station in TrainStation.objects.all():
        station_location = station.latitude,station.longitude

        distance = geodesic (user_location, station_location).km
        station_distances[distance] = station_location
    
    min_distance = min(station_distances)
    station_coords = station_distances[min_distance]
    return JsonResponse({
        'coordinates': station_coords,
        'distance': min_distance
    })
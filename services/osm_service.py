import requests
from flask import current_app
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

class OSMService:
    
    @staticmethod
    def get_geocoder():
        """
        Obtiene un objeto geocodificador de Nominatim [citation:2][citation:7]
        IMPORTANTE: Debes usar un user_agent personalizado para cumplir con la política de uso [citation:7]
        """
        user_agent = current_app.config.get('OSM_USER_AGENT', 'MiApp/1.0')
        timeout = current_app.config.get('OSM_TIMEOUT', 10)
        
        geolocator = Nominatim(
            user_agent=user_agent,
            timeout=timeout
        )
        return geolocator
    
    @staticmethod
    def geocode_address(address):
        """
        Convierte una dirección en coordenadas (lat, lon) usando Nominatim [citation:2]
        """
        try:
            geolocator = OSMService.get_geocoder()
            location = geolocator.geocode(address)
            
            if location:
                return {
                    'lat': location.latitude,
                    'lon': location.longitude,
                    'direccion_completa': location.address,
                    'raw': location.raw  # Datos adicionales de OpenStreetMap
                }
            return None
        except GeocoderTimedOut:
            print("Timeout en geocodificación")
            return None
        except GeocoderUnavailable:
            print("Servicio de geocodificación no disponible")
            return None
        except Exception as e:
            print(f"Error en geocodificación: {e}")
            return None
    
    @staticmethod
    def reverse_geocode(lat, lon):
        """
        Convierte coordenadas en una dirección [citation:2]
        """
        try:
            geolocator = OSMService.get_geocoder()
            location = geolocator.reverse(f"{lat}, {lon}")
            
            if location:
                return {
                    'direccion': location.address,
                    'raw': location.raw
                }
            return None
        except Exception as e:
            print(f"Error en reverse geocoding: {e}")
            return None
    
    @staticmethod
    def search_places(query, limit=10):
        """
        Busca lugares por texto usando Nominatim
        """
        try:
            geolocator = OSMService.get_geocoder()
            locations = geolocator.geocode(query, exactly_one=False, limit=limit)
            
            if locations:
                results = []
                for loc in locations:
                    results.append({
                        'nombre': loc.raw.get('display_name', '').split(',')[0],
                        'direccion': loc.address,
                        'lat': loc.latitude,
                        'lon': loc.longitude,
                        'raw': loc.raw
                    })
                return results
            return []
        except Exception as e:
            print(f"Error en búsqueda de lugares: {e}")
            return []
    
    @staticmethod
    def calculate_distance(point1, point2):
        """
        Calcula la distancia entre dos puntos (lat, lon) en kilómetros [citation:2]
        """
        try:
            distance = geodesic(point1, point2).kilometers
            return round(distance, 2)
        except Exception as e:
            print(f"Error calculando distancia: {e}")
            return None
    
    @staticmethod
    def search_nearby_places(lat, lon, place_type=None, radius=1000, limit=20):
        """
        Busca lugares cercanos usando Overpass API de OpenStreetMap
        """
        # Overpass API query [citation:5]
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Mapear tipos a tags de OpenStreetMap
        type_mapping = {
            'restaurante': 'amenity=restaurant',
            'cafe': 'amenity=cafe',
            'gimnasio': 'leisure=fitness_centre OR sport=gym',
            'parque': 'leisure=park',
            'supermercado': 'shop=supermarket',
            'tienda_saludable': 'shop=health_food OR shop=organic',
            'farmacia': 'amenity=pharmacy',
            'hospital': 'amenity=hospital',
            'clinica': 'amenity=clinic',
        }
        
        osm_tag = type_mapping.get(place_type, place_type) if place_type else ''
        
        # Construir consulta Overpass
        overpass_query = f"""
        [out:json];
        (
          node["{osm_tag}"](around:{radius},{lat},{lon});
          way["{osm_tag}"](around:{radius},{lat},{lon});
          relation["{osm_tag}"](around:{radius},{lat},{lon});
        );
        out body center;
        """
        
        try:
            response = requests.post(overpass_url, data=overpass_query)
            response.raise_for_status()
            data = response.json()
            
            places = []
            for element in data.get('elements', [])[:limit]:
                # Obtener coordenadas
                if element['type'] == 'node':
                    place_lat = element['lat']
                    place_lon = element['lon']
                else:
                    # Para ways y relations, usar el centro
                    if 'center' in element:
                        place_lat = element['center']['lat']
                        place_lon = element['center']['lon']
                    else:
                        continue
                
                # Calcular distancia
                distance = OSMService.calculate_distance(
                    (lat, lon), 
                    (place_lat, place_lon)
                )
                
                places.append({
                    'id': element['id'],
                    'tipo': element['type'],
                    'nombre': element.get('tags', {}).get('name', 'Sin nombre'),
                    'direccion': element.get('tags', {}).get('addr:full', ''),
                    'lat': place_lat,
                    'lon': place_lon,
                    'tags': element.get('tags', {}),
                    'distancia': distance
                })
            
            return places
        except Exception as e:
            print(f"Error en Overpass API: {e}")
            return []
         

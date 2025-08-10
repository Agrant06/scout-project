import requests
import json
from typing import Dict, List, Any, Optional
from app import db
import os

class GooglePlacesService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY', 'your-google-places-api-key')
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_places(self, location: Dict[str, float], radius: int, 
                     place_type: Optional[str] = None, 
                     keyword: Optional[str] = None) -> Dict[str, Any]:
        """
        Buscar lugares cerca de una ubicación específica
        
        Args:
            location: Diccionario con latitud y longitud {'lat': float, 'lng': float}
            radius: Radio de búsqueda en metros
            place_type: Tipo de lugar (restaurant, store, etc.)
            keyword: Palabra clave para buscar
            
        Returns:
            Diccionario con resultados de la búsqueda
        """
        try:
            endpoint = f"{self.base_url}/nearbysearch/json"
            
            params = {
                'location': f"{location['lat']},{location['lng']}",
                'radius': radius,
                'key': self.api_key
            }
            
            if place_type:
                params['type'] = place_type
                
            if keyword:
                params['keyword'] = keyword
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'results': []
            }
    
    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de un lugar específico
        
        Args:
            place_id: ID del lugar de Google Places
            
        Returns:
            Diccionario con detalles del lugar
        """
        try:
            endpoint = f"{self.base_url}/details/json"
            
            params = {
                'place_id': place_id,
                'fields': 'name,rating,review,user_ratings_total,formatted_address,'
                        'geometry,website,formatted_phone_number,opening_hours,'
                        'price_level,photos,reviews',
                'key': self.api_key
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'result': {}
            }
    
    def get_place_photos(self, photo_reference: str, max_width: int = 400) -> str:
        """
        Obtener URL de una foto de un lugar
        
        Args:
            photo_reference: Referencia de la foto
            max_width: Ancho máximo de la foto
            
        Returns:
            URL de la foto
        """
        return f"{self.base_url}/photo?maxwidth={max_width}&photoreference={photo_reference}&key={self.api_key}"
    
    def text_search(self, query: str, location: Optional[Dict[str, float]] = None, 
                   radius: Optional[int] = None) -> Dict[str, Any]:
        """
        Buscar lugares por texto
        
        Args:
            query: Texto de búsqueda
            location: Ubicación central para la búsqueda
            radius: Radio de búsqueda en metros
            
        Returns:
            Diccionario con resultados de la búsqueda
        """
        try:
            endpoint = f"{self.base_url}/textsearch/json"
            
            params = {
                'query': query,
                'key': self.api_key
            }
            
            if location:
                params['location'] = f"{location['lat']},{location['lng']}"
                
            if radius:
                params['radius'] = radius
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'results': []
            }
    
    def calculate_business_score(self, place_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcular puntuación para un negocio basado en datos de Google Places
        
        Args:
            place_data: Datos del lugar de Google Places
            
        Returns:
            Diccionario con puntuaciones para diferentes aspectos
        """
        scores = {
            'google_maps_score': 0,
            'rating_score': 0,
            'reviews_score': 0,
            'photos_score': 0,
            'info_score': 0
        }
        
        result = place_data.get('result', {})
        
        # Puntuación por rating general (0-30 puntos)
        rating = result.get('rating', 0)
        if rating:
            scores['rating_score'] = min(30, rating * 6)  # 5 estrellas * 6 = 30 puntos
        
        # Puntuación por cantidad de reseñas (0-25 puntos)
        user_ratings_total = result.get('user_ratings_total', 0)
        if user_ratings_total > 0:
            scores['reviews_score'] = min(25, min(25, user_ratings_total / 10))
        
        # Puntuación por fotos (0-20 puntos)
        photos = result.get('photos', [])
        if photos:
            scores['photos_score'] = min(20, len(photos) * 2)
        
        # Puntuación por información completa (0-25 puntos)
        info_fields = [
            'formatted_phone_number',
            'website',
            'opening_hours',
            'formatted_address'
        ]
        complete_fields = sum(1 for field in info_fields if field in result and result[field])
        scores['info_score'] = min(25, complete_fields * 6.25)
        
        # Calcular puntuación total
        scores['google_maps_score'] = sum(scores.values()) - scores['google_maps_score']
        
        return scores
    
    def extract_inconsistencies(self, place_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extraer inconsistencias o problemas en los datos de un lugar
        
        Args:
            place_data: Datos del lugar de Google Places
            
        Returns:
            Lista de inconsistencias encontradas
        """
        inconsistencies = []
        result = place_data.get('result', {})
        
        # Verificar si tiene dirección
        if 'formatted_address' not in result or not result['formatted_address']:
            inconsistencies.append({
                'type': 'missing_address',
                'severity': 'high',
                'description': 'El negocio no tiene dirección registrada',
                'recommendation': 'Agregar la dirección completa del negocio'
            })
        
        # Verificar si tiene teléfono
        if 'formatted_phone_number' not in result or not result['formatted_phone_number']:
            inconsistencies.append({
                'type': 'missing_phone',
                'severity': 'medium',
                'description': 'El negocio no tiene teléfono registrado',
                'recommendation': 'Agregar un número de teléfono de contacto'
            })
        
        # Verificar si tiene sitio web
        if 'website' not in result or not result['website']:
            inconsistencies.append({
                'type': 'missing_website',
                'severity': 'medium',
                'description': 'El negocio no tiene sitio web',
                'recommendation': 'Crear un sitio web para el negocio'
            })
        
        # Verificar si tiene horarios de apertura
        if 'opening_hours' not in result or not result['opening_hours']:
            inconsistencies.append({
                'type': 'missing_hours',
                'severity': 'low',
                'description': 'El negocio no tiene horarios de apertura',
                'recommendation': 'Agregar horarios de apertura y cierre'
            })
        
        # Verificar rating bajo
        rating = result.get('rating', 0)
        if rating < 3.5:
            inconsistencies.append({
                'type': 'low_rating',
                'severity': 'medium',
                'description': f'El negocio tiene un rating bajo ({rating}/5)',
                'recommendation': 'Mejorar la calidad del servicio para aumentar el rating'
            })
        
        # Verificar pocas fotos
        photos = result.get('photos', [])
        if len(photos) < 3:
            inconsistencies.append({
                'type': 'few_photos',
                'severity': 'low',
                'description': f'El negocio tiene pocas fotos ({len(photos)})',
                'recommendation': 'Agregar más fotos del negocio y sus productos'
            })
        
        return inconsistencies
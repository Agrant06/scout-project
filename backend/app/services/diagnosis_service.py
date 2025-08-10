import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from .google_places_service import GooglePlacesService
from .website_analysis_service import WebsiteAnalysisService
from app import db
from app.models.business import Business
from app.models.diagnosis import Diagnosis
from app.models.recommendation import Recommendation

class DiagnosisService:
    def __init__(self):
        self.google_places_service = GooglePlacesService()
        self.website_service = WebsiteAnalysisService()
    
    def create_diagnosis(self, business_id: str, user_id: str) -> Dict[str, Any]:
        """
        Crear un diagnóstico completo para un negocio
        
        Args:
            business_id: ID del negocio a diagnosticar
            user_id: ID del usuario que solicita el diagnóstico
            
        Returns:
            Diccionario con resultados del diagnóstico
        """
        try:
            # Obtener información del negocio
            business = Business.query.get(business_id)
            if not business:
                return {
                    'status': 'error',
                    'error': 'Negocio no encontrado',
                    'diagnosis_id': None
                }
            
            # Realizar análisis de Google Places
            google_places_data = self._analyze_google_places(business)
            
            # Realizar análisis de sitio web
            website_data = self._analyze_website(business)
            
            # Calcular puntuaciones generales
            scores = self._calculate_overall_scores(google_places_data, website_data)
            
            # Extraer inconsistencias
            inconsistencies = self._extract_inconsistencies(google_places_data, website_data)
            
            # Crear diagnóstico en la base de datos
            diagnosis = Diagnosis(
                business_id=business_id,
                google_maps_score=scores['google_maps_score'],
                website_score=scores['website_score'],
                overall_score=scores['overall_score'],
                google_maps_data=json.dumps(google_places_data),
                website_data=json.dumps(website_data),
                inconsistencies=json.dumps(inconsistencies),
                user_id=user_id
            )
            
            db.session.add(diagnosis)
            db.session.commit()
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(
                diagnosis.id, google_places_data, website_data, inconsistencies
            )
            
            return {
                'status': 'success',
                'diagnosis_id': diagnosis.id,
                'scores': scores,
                'inconsistencies_count': len(inconsistencies),
                'recommendations_count': len(recommendations)
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'error': str(e),
                'diagnosis_id': None
            }
    
    def _analyze_google_places(self, business: Business) -> Dict[str, Any]:
        """Analizar presencia en Google Places"""
        if not business.google_places_id:
            return {
                'status': 'no_google_places_id',
                'data': {},
                'score': 0,
                'inconsistencies': []
            }
        
        try:
            # Obtener detalles del lugar
            place_details = self.google_places_service.get_place_details(business.google_places_id)
            
            if place_details.get('status') != 'OK':
                return {
                    'status': 'error',
                    'error': place_details.get('error_message', 'Error desconocido'),
                    'data': {},
                    'score': 0,
                    'inconsistencies': []
                }
            
            # Calcular puntuación
            scores = self.google_places_service.calculate_business_score(place_details)
            
            # Extraer inconsistencias
            inconsistencies = self.google_places_service.extract_inconsistencies(place_details)
            
            return {
                'status': 'success',
                'data': place_details,
                'score': scores['google_maps_score'],
                'inconsistencies': inconsistencies
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'data': {},
                'score': 0,
                'inconsistencies': []
            }
    
    def _analyze_website(self, business: Business) -> Dict[str, Any]:
        """Analizar sitio web del negocio"""
        if not business.website:
            return {
                'status': 'no_website',
                'data': {},
                'score': 0,
                'issues': []
            }
        
        try:
            # Analizar sitio web
            website_analysis = self.website_service.analyze_website(business.website)
            
            return {
                'status': 'success',
                'data': website_analysis,
                'score': website_analysis.get('score', 0),
                'issues': website_analysis.get('issues', [])
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'data': {},
                'score': 0,
                'issues': []
            }
    
    def _calculate_overall_scores(self, google_places_data: Dict[str, Any], 
                               website_data: Dict[str, Any]) -> Dict[str, float]:
        """Calcular puntuaciones generales"""
        google_maps_score = google_places_data.get('score', 0)
        website_score = website_data.get('score', 0)
        
        # Calcular puntuación general (60% Google Maps, 40% Website)
        overall_score = (google_maps_score * 0.6) + (website_score * 0.4)
        
        return {
            'google_maps_score': google_maps_score,
            'website_score': website_score,
            'overall_score': round(overall_score, 2)
        }
    
    def _extract_inconsistencies(self, google_places_data: Dict[str, Any], 
                               website_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extraer y consolidar inconsistencias"""
        inconsistencies = []
        
        # Agregar inconsistencias de Google Places
        google_inconsistencies = google_places_data.get('inconsistencies', [])
        for inconsistency in google_inconsistencies:
            inconsistencies.append({
                'source': 'google_places',
                'type': inconsistency.get('type'),
                'severity': inconsistency.get('severity'),
                'description': inconsistency.get('description'),
                'recommendation': inconsistency.get('recommendation')
            })
        
        # Agregar inconsistencias de sitio web
        website_issues = website_data.get('issues', [])
        for issue in website_issues:
            inconsistencies.append({
                'source': 'website',
                'type': issue.get('type'),
                'severity': issue.get('severity'),
                'description': issue.get('description'),
                'recommendation': issue.get('recommendation')
            })
        
        # Agregar inconsistencias generales
        if not google_places_data.get('data'):
            inconsistencies.append({
                'source': 'general',
                'type': 'no_google_places',
                'severity': 'high',
                'description': 'El negocio no está registrado en Google Places',
                'recommendation': 'Registrar el negocio en Google Business Profile'
            })
        
        if not website_data.get('data') and website_data.get('status') != 'no_website':
            inconsistencies.append({
                'source': 'general',
                'type': 'website_analysis_error',
                'severity': 'medium',
                'description': 'No se pudo analizar el sitio web',
                'recommendation': 'Verificar que el sitio web esté accesible'
            })
        
        return inconsistencies
    
    def _generate_recommendations(self, diagnosis_id: str, 
                                google_places_data: Dict[str, Any],
                                website_data: Dict[str, Any],
                                inconsistencies: List[Dict[str, Any]]) -> List[Recommendation]:
        """Generar recomendaciones basadas en el diagnóstico"""
        recommendations = []
        
        # Generar recomendaciones a partir de inconsistencias
        for inconsistency in inconsistencies:
            recommendation = Recommendation(
                diagnosis_id=diagnosis_id,
                title=self._generate_recommendation_title(inconsistency),
                description=inconsistency['description'],
                category=self._get_recommendation_category(inconsistency['source']),
                priority=self._get_recommendation_priority(inconsistency['severity']),
                difficulty=self._get_recommendation_difficulty(inconsistency),
                estimated_time=self._get_estimated_time(inconsistency['type']),
                user_id=inconsistencies[0].get('user_id', 'unknown')  # Esto debería ajustarse
            )
            
            recommendations.append(recommendation)
        
        # Guardar recomendaciones en la base de datos
        for recommendation in recommendations:
            db.session.add(recommendation)
        
        db.session.commit()
        
        return recommendations
    
    def _generate_recommendation_title(self, inconsistency: Dict[str, Any]) -> str:
        """Generar título para una recomendación"""
        type_mapping = {
            'missing_address': 'Agregar dirección a Google Places',
            'missing_phone': 'Agregar número de teléfono',
            'missing_website': 'Crear sitio web para el negocio',
            'missing_hours': 'Agregar horarios de apertura',
            'low_rating': 'Mejorar rating en Google Places',
            'few_photos': 'Agregar más fotos al perfil',
            'no_ssl': 'Implementar certificado SSL',
            'slow_load_time': 'Optimizar tiempo de carga del sitio web',
            'large_page_size': 'Reducir tamaño de la página web',
            'missing_title': 'Agregar título a la página principal',
            'missing_meta_description': 'Agregar meta descripción',
            'missing_h1': 'Agregar encabezado H1',
            'missing_viewport': 'Hacer el sitio web responsivo',
            'missing_contact_info': 'Agregar información de contacto',
            'no_google_places': 'Registrar en Google Business Profile',
            'website_analysis_error': 'Verificar accesibilidad del sitio web'
        }
        
        return type_mapping.get(inconsistency.get('type'), 'Mejorar presencia digital')
    
    def _get_recommendation_category(self, source: str) -> str:
        """Determinar categoría de la recomendación"""
        category_mapping = {
            'google_places': 'google_maps',
            'website': 'website',
            'general': 'general'
        }
        
        return category_mapping.get(source, 'general')
    
    def _get_recommendation_priority(self, severity: str) -> str:
        """Determinar prioridad de la recomendación"""
        priority_mapping = {
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        
        return priority_mapping.get(severity, 'medium')
    
    def _get_recommendation_difficulty(self, severity: str) -> str:
        """Determinar dificultad de la recomendación"""
        difficulty_mapping = {
            'high': 'hard',
            'medium': 'medium',
            'low': 'easy'
        }
        
        return difficulty_mapping.get(severity, 'medium')
    
    def _get_estimated_time(self, type: str) -> str:
        """Estimar tiempo para implementar la recomendación"""
        time_mapping = {
            'missing_address': '30 minutos',
            'missing_phone': '15 minutos',
            'missing_website': '2-3 días',
            'missing_hours': '15 minutos',
            'low_rating': '1-2 semanas',
            'few_photos': '1 hora',
            'no_ssl': '1-2 horas',
            'slow_load_time': '2-4 horas',
            'large_page_size': '2-3 horas',
            'missing_title': '10 minutos',
            'missing_meta_description': '15 minutos',
            'missing_h1': '10 minutos',
            'missing_viewport': '30 minutos',
            'missing_contact_info': '1 hora',
            'no_google_places': '1 hora',
            'website_analysis_error': '30 minutos'
        }
        
        return time_mapping.get(type, '1 hora')
    
    def batch_diagnosis(self, business_ids: List[str], user_id: str) -> Dict[str, Any]:
        """
        Realizar diagnóstico por lotes para múltiples negocios
        
        Args:
            business_ids: Lista de IDs de negocios a diagnosticar
            user_id: ID del usuario que solicita los diagnósticos
            
        Returns:
            Diccionario con resultados de los diagnósticos
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(business_ids)
        }
        
        for business_id in business_ids:
            try:
                diagnosis_result = self.create_diagnosis(business_id, user_id)
                if diagnosis_result['status'] == 'success':
                    results['successful'].append({
                        'business_id': business_id,
                        'diagnosis_id': diagnosis_result['diagnosis_id'],
                        'overall_score': diagnosis_result['scores']['overall_score']
                    })
                else:
                    results['failed'].append({
                        'business_id': business_id,
                        'error': diagnosis_result['error']
                    })
            except Exception as e:
                results['failed'].append({
                    'business_id': business_id,
                    'error': str(e)
                })
        
        return results
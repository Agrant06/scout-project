import requests
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import time

class WebsiteAnalysisService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 10
    
    def analyze_website(self, url: str) -> Dict[str, Any]:
        """
        Analizar un sitio web y retornar información relevante
        
        Args:
            url: URL del sitio web a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        if not url:
            return {
                'status': 'error',
                'error': 'URL no proporcionada',
                'score': 0,
                'issues': []
            }
        
        # Asegurarse de que la URL tenga protocolo
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        results = {
            'url': url,
            'status': 'success',
            'score': 0,
            'issues': [],
            'metadata': {},
            'performance': {},
            'content': {}
        }
        
        try:
            # Analizar metadatos básicos
            self._analyze_metadata(url, results)
            
            # Analizar rendimiento
            self._analyze_performance(url, results)
            
            # Analizar contenido
            self._analyze_content(url, results)
            
            # Calcular puntuación general
            results['score'] = self._calculate_website_score(results)
            
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            results['score'] = 0
        
        return results
    
    def _analyze_metadata(self, url: str, results: Dict[str, Any]):
        """Analizar metadatos del sitio web"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            
            # Extraer información básica
            results['metadata']['status_code'] = response.status_code
            results['metadata']['content_type'] = response.headers.get('content-type', '')
            results['metadata']['server'] = response.headers.get('server', '')
            results['metadata']['content_length'] = len(response.content)
            
            # Verificar si tiene certificado SSL
            if url.startswith('https://'):
                results['metadata']['has_ssl'] = True
            else:
                results['metadata']['has_ssl'] = False
                results['issues'].append({
                    'type': 'no_ssl',
                    'severity': 'medium',
                    'description': 'El sitio no usa HTTPS',
                    'recommendation': 'Implementar certificado SSL para mejorar seguridad'
                })
            
            # Verificar encabezados de seguridad
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            missing_security_headers = []
            for header in security_headers:
                if header not in response.headers:
                    missing_security_headers.append(header)
            
            if missing_security_headers:
                results['issues'].append({
                    'type': 'missing_security_headers',
                    'severity': 'low',
                    'description': f'Faltan encabezados de seguridad: {", ".join(missing_security_headers)}',
                    'recommendation': 'Implementar encabezados de seguridad adicionales'
                })
            
        except requests.exceptions.RequestException as e:
            results['status'] = 'error'
            results['error'] = f"No se pudo acceder al sitio: {str(e)}"
            results['score'] = 0
    
    def _analyze_performance(self, url: str, results: Dict[str, Any]):
        """Analizar rendimiento del sitio web"""
        try:
            # Medir tiempo de carga
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout)
            load_time = time.time() - start_time
            
            results['performance']['load_time'] = load_time
            
            # Evaluar tiempo de carga
            if load_time > 3:
                results['issues'].append({
                    'type': 'slow_load_time',
                    'severity': 'medium',
                    'description': f'El sitio tarda mucho en cargar ({load_time:.2f}s)',
                    'recommendation': 'Optimizar imágenes y minificar CSS/JS'
                })
            
            # Verificar tamaño de la página
            content_length = len(response.content)
            results['performance']['content_length'] = content_length
            
            if content_length > 2 * 1024 * 1024:  # > 2MB
                results['issues'].append({
                    'type': 'large_page_size',
                    'severity': 'medium',
                    'description': f'La página es muy pesada ({content_length / 1024 / 1024:.2f}MB)',
                    'recommendation': 'Optimizar imágenes y comprimir recursos'
                })
            
        except Exception as e:
            results['performance']['error'] = str(e)
    
    def _analyze_content(self, url: str, results: Dict[str, Any]):
        """Analizar contenido del sitio web"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            content = response.text.lower()
            
            # Verificar elementos importantes
            important_elements = {
                'title': '<title>',
                'meta_description': '<meta name="description"',
                'h1': '<h1',
                'viewport': 'viewport',
                'favicon': 'icon',
                'open_graph': 'og:',
                'twitter_card': 'twitter:card'
            }
            
            missing_elements = []
            found_elements = {}
            
            for element, tag in important_elements.items():
                if tag in content:
                    found_elements[element] = True
                else:
                    missing_elements.append(element)
            
            results['content']['missing_elements'] = missing_elements
            results['content']['found_elements'] = found_elements
            
            # Generar recomendaciones basadas en elementos faltantes
            if 'title' in missing_elements:
                results['issues'].append({
                    'type': 'missing_title',
                    'severity': 'high',
                    'description': 'La página no tiene título',
                    'recommendation': 'Agregar un título descriptivo a la página'
                })
            
            if 'meta_description' in missing_elements:
                results['issues'].append({
                    'type': 'missing_meta_description',
                    'severity': 'medium',
                    'description': 'La página no tiene meta descripción',
                    'recommendation': 'Agregar meta descripción para mejorar SEO'
                })
            
            if 'h1' in missing_elements:
                results['issues'].append({
                    'type': 'missing_h1',
                    'severity': 'medium',
                    'description': 'La página no tiene encabezado H1',
                    'recommendation': 'Agregar encabezado H1 con palabras clave principales'
                })
            
            if 'viewport' in missing_elements:
                results['issues'].append({
                    'type': 'missing_viewport',
                    'severity': 'high',
                    'description': 'La página no tiene meta viewport',
                    'recommendation': 'Agregar meta viewport para diseño responsivo'
                })
            
            # Verificar palabras clave importantes
            keywords = ['contacto', 'teléfono', 'dirección', 'whatsapp', 'email']
            found_keywords = []
            
            for keyword in keywords:
                if keyword in content:
                    found_keywords.append(keyword)
            
            results['content']['found_keywords'] = found_keywords
            
            # Verificar si tiene información de contacto
            if 'contacto' not in found_keywords and 'teléfono' not in found_keywords:
                results['issues'].append({
                    'type': 'missing_contact_info',
                    'severity': 'high',
                    'description': 'No se encontró información de contacto',
                    'recommendation': 'Agregar sección de contacto clara y visible'
                })
            
        except Exception as e:
            results['content']['error'] = str(e)
    
    def _calculate_website_score(self, results: Dict[str, Any]) -> float:
        """Calcular puntuación general del sitio web"""
        if results['status'] == 'error':
            return 0
        
        score = 100
        
        # Restar puntos por cada problema
        severity_penalties = {
            'high': 20,
            'medium': 10,
            'low': 5
        }
        
        for issue in results['issues']:
            severity = issue.get('severity', 'medium')
            score -= severity_penalties.get(severity, 10)
        
        # Penalizar por rendimiento lento
        load_time = results['performance'].get('load_time', 0)
        if load_time > 3:
            score -= min(20, (load_time - 3) * 5)
        
        # Penalizar por tamaño grande
        content_length = results['performance'].get('content_length', 0)
        if content_length > 2 * 1024 * 1024:  # > 2MB
            score -= min(15, (content_length - 2 * 1024 * 1024) / (1024 * 1024) * 5)
        
        # Asegurar que la puntuación esté entre 0 y 100
        return max(0, min(100, score))
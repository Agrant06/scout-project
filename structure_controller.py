import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class StructureController:
    def __init__(self, base_path="D:\\Paginas\\scout_project"):
        self.base_path = Path(base_path)
        self.log_file = self.base_path / "structure_analysis.log"
        self.structure_data = {
            "timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "analysis": {},
            "anomalies": [],
            "recommendations": [],
            "actions_taken": []
        }
        
    def log_message(self, message):
        """Añadir mensaje al log y a la consola"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def analyze_structure(self):
        """Analizar la estructura del proyecto"""
        self.log_message("Iniciando análisis de estructura del proyecto")
        
        # Analizar estructura general
        self.structure_data["analysis"]["general"] = self._analyze_directory(self.base_path)
        
        # Analizar backend en detalle
        backend_path = self.base_path / "backend"
        if backend_path.exists():
            self.structure_data["analysis"]["backend"] = self._analyze_directory(backend_path)
            self._analyze_backend_anomalies(backend_path)
        
        # Analizar frontend en detalle
        frontend_path = self.base_path / "frontend"
        if frontend_path.exists():
            self.structure_data["analysis"]["frontend"] = self._analyze_directory(frontend_path)
            self._analyze_frontend_anomalies(frontend_path)
        
        # Guardar análisis completo
        with open(self.base_path / "structure_analysis.json", "w", encoding="utf-8") as f:
            json.dump(self.structure_data, f, indent=2, ensure_ascii=False)
        
        self.log_message("Análisis completado y guardado en structure_analysis.json")
        
        return self.structure_data
    
    def _analyze_directory(self, directory_path):
        """Analizar un directorio y su contenido"""
        result = {
            "path": str(directory_path),
            "exists": directory_path.exists(),
            "directories": [],
            "files": [],
            "total_size": 0
        }
        
        if not directory_path.exists():
            return result
        
        for item in directory_path.iterdir():
            if item.is_dir():
                dir_info = {
                    "name": item.name,
                    "path": str(item),
                    "size": self._get_directory_size(item),
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                result["directories"].append(dir_info)
                result["total_size"] += dir_info["size"]
            else:
                file_info = {
                    "name": item.name,
                    "path": str(item),
                    "size": item.stat().st_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                result["files"].append(file_info)
                result["total_size"] += file_info["size"]
        
        return result
    
    def _get_directory_size(self, directory_path):
        """Calcular el tamaño total de un directorio"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        except (OSError, IOError):
            pass
        return total_size
    
    def _analyze_backend_anomalies(self, backend_path):
        """Analizar anomalías específicas del backend"""
        self.log_message(f"Analizando anomalías en backend: {backend_path}")
        
        # Verificar estructura esperada
        expected_structure = ["app", "instance", "migrations"]
        expected_app_structure = ["models", "routes", "services", "utils"]
        
        # Verificar carpetas esperadas
        for expected_dir in expected_structure:
            dir_path = backend_path / expected_dir
            if not dir_path.exists():
                anomaly = {
                    "type": "missing_directory",
                    "path": str(dir_path),
                    "description": f"Falta directorio esperado: {expected_dir}",
                    "severity": "high"
                }
                self.structure_data["anomalies"].append(anomaly)
                self.log_message(f"ANOMALÍA: {anomaly['description']}")
        
        # Verificar estructura de app
        app_path = backend_path / "app"
        if app_path.exists():
            for expected_dir in expected_app_structure:
                dir_path = app_path / expected_dir
                if not dir_path.exists():
                    anomaly = {
                        "type": "missing_directory",
                        "path": str(dir_path),
                        "description": f"Falta subdirectorio esperado en app: {expected_dir}",
                        "severity": "medium"
                    }
                    self.structure_data["anomalies"].append(anomaly)
                    self.log_message(f"ANOMALÍA: {anomaly['description']}")
        
        # Verificar archivos innecesarios en backend
        unnecessary_files = [
            "init_db.py", "init_db_fixed.py", "init_db_simple.py",
            "test_db.py", "fix_structure.py", "fix_structure_final.py",
            "simple_app.py", "minimal.py", "run.py.backup"
        ]
        
        for filename in unnecessary_files:
            file_path = backend_path / filename
            if file_path.exists():
                anomaly = {
                    "type": "unnecessary_file",
                    "path": str(file_path),
                    "description": f"Archivo innecesario en backend: {filename}",
                    "severity": "low"
                }
                self.structure_data["anomalies"].append(anomaly)
                self.log_message(f"ANOMALÍA: {anomaly['description']}")
        
        # Verificar carpetas que no deberían estar en backend
        unexpected_dirs = ["frontend", "docs", "scout_venv"]
        for dirname in unexpected_dirs:
            dir_path = backend_path / dirname
            if dir_path.exists():
                anomaly = {
                    "type": "unexpected_directory",
                    "path": str(dir_path),
                    "description": f"Directorio inesperado en backend: {dirname}",
                    "severity": "high"
                }
                self.structure_data["anomalies"].append(anomaly)
                self.log_message(f"ANOMALÍA: {anomaly['description']}")
    
    def _analyze_frontend_anomalies(self, frontend_path):
        """Analizar anomalías específicas del frontend"""
        self.log_message(f"Analizando anomalías en frontend: {frontend_path}")
        
        # Verificar si es un proyecto React válido
        package_json = frontend_path / "package.json"
        if not package_json.exists():
            anomaly = {
                "type": "missing_file",
                "path": str(package_json),
                "description": "No se encontró package.json en frontend",
                "severity": "high"
            }
            self.structure_data["anomalies"].append(anomaly)
            self.log_message(f"ANOMALÍA: {anomaly['description']}")
    
    def generate_recommendations(self):
        """Generar recomendaciones basadas en el análisis"""
        self.log_message("Generando recomendaciones...")
        
        # Recomendaciones para anomalías de backend
        backend_anomalies = [a for a in self.structure_data["anomalies"] if "backend" in a["path"]]
        if backend_anomalies:
            self.structure_data["recommendations"].append({
                "type": "backend_cleanup",
                "description": "Limpiar estructura de backend eliminando archivos innecesarios y moviendo carpetas incorrectas",
                "priority": "high"
            })
        
        # Recomendaciones para archivos faltantes
        missing_items = [a for a in self.structure_data["anomalies"] if a["type"] == "missing_directory" or a["type"] == "missing_file"]
        if missing_items:
            self.structure_data["recommendations"].append({
                "type": "create_missing",
                "description": "Crear directorios y archivos faltantes",
                "priority": "high"
            })
        
        # Recomendaciones para archivos innecesarios
        unnecessary_items = [a for a in self.structure_data["anomalies"] if a["type"] == "unnecessary_file"]
        if unnecessary_items:
            self.structure_data["recommendations"].append({
                "type": "remove_unnecessary",
                "description": "Eliminar archivos innecesarios",
                "priority": "medium"
            })
        
        # Guardar recomendaciones
        with open(self.base_path / "structure_analysis.json", "w", encoding="utf-8") as f:
            json.dump(self.structure_data, f, indent=2, ensure_ascii=False)
        
        self.log_message(f"Generadas {len(self.structure_data['recommendations'])} recomendaciones")
    
    def execute_cleanup(self):
        """Ejecutar limpieza basada en las recomendaciones"""
        self.log_message("Iniciando proceso de limpieza...")
        
        for recommendation in self.structure_data["recommendations"]:
            if recommendation["priority"] == "high":
                self.log_message(f"Ejecutando recomendación de alta prioridad: {recommendation['description']}")
                
                if recommendation["type"] == "backend_cleanup":
                    self._cleanup_backend()
                elif recommendation["type"] == "create_missing":
                    self._create_missing_items()
                elif recommendation["type"] == "remove_unnecessary":
                    self._remove_unnecessary_items()
        
        self.log_message("Proceso de limpieza completado")
    
    def _cleanup_backend(self):
        """Limpiar estructura de backend"""
        backend_path = self.base_path / "backend"
        
        # Mover carpetas que no deberían estar en backend
        unexpected_dirs = ["frontend", "docs", "scout_venv"]
        for dirname in unexpected_dirs:
            dir_path = backend_path / dirname
            if dir_path.exists():
                target_path = self.base_path / dirname
                if not target_path.exists():
                    self.log_message(f"Moviendo {dir_path} a {target_path}")
                    shutil.move(str(dir_path), str(target_path))
                    self.structure_data["actions_taken"].append(f"Moved {dir_path} to {target_path}")
                else:
                    self.log_message(f"El destino {target_path} ya existe, fusionando contenido...")
                    # Fusionar contenido
                    for item in dir_path.iterdir():
                        target_item = target_path / item.name
                        if not target_item.exists():
                            shutil.move(str(item), str(target_item))
                            self.structure_data["actions_taken"].append(f"Moved {item} to {target_item}")
        
        # Eliminar archivos innecesarios
        unnecessary_files = [
            "init_db.py", "init_db_fixed.py", "init_db_simple.py",
            "test_db.py", "fix_structure.py", "fix_structure_final.py",
            "simple_app.py", "minimal.py", "run.py.backup"
        ]
        
        for filename in unnecessary_files:
            file_path = backend_path / filename
            if file_path.exists():
                self.log_message(f"Eliminando archivo innecesario: {file_path}")
                file_path.unlink()
                self.structure_data["actions_taken"].append(f"Deleted {file_path}")
        
        # Eliminar carpetas vacías
        self._remove_empty_directories(backend_path)
    
    def _create_missing_items(self):
        """Crear directorios y archivos faltantes"""
        backend_path = self.base_path / "backend"
        
        # Crear estructura esperada
        expected_structure = {
            "app": {
                "models": {"__init__.py": ""},
                "routes": {"__init__.py": ""},
                "services": {"__init__.py": ""},
                "utils": {"__init__.py": ""}
            },
            "instance": {},
            "migrations": {}
        }
        
        self._create_structure(backend_path, expected_structure)
    
    def _create_structure(self, base_path, structure):
        """Crear estructura de directorios y archivos"""
        for name, content in structure.items():
            path = base_path / name
            if isinstance(content, dict):
                if not path.exists():
                    self.log_message(f"Creando directorio: {path}")
                    path.mkdir(parents=True, exist_ok=True)
                    self.structure_data["actions_taken"].append(f"Created directory {path}")
                self._create_structure(path, content)
            else:
                if not path.exists():
                    self.log_message(f"Creando archivo: {path}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.structure_data["actions_taken"].append(f"Created file {path}")
    
    def _remove_unnecessary_items(self):
        """Eliminar archivos innecesarios"""
        backend_path = self.base_path / "backend"
        
        unnecessary_files = [
            "init_db.py", "init_db_fixed.py", "init_db_simple.py",
            "test_db.py", "fix_structure.py", "fix_structure_final.py",
            "simple_app.py", "minimal.py", "run.py.backup"
        ]
        
        for filename in unnecessary_files:
            file_path = backend_path / filename
            if file_path.exists():
                self.log_message(f"Eliminando archivo innecesario: {file_path}")
                file_path.unlink()
                self.structure_data["actions_taken"].append(f"Deleted {file_path}")
    
    def _remove_empty_directories(self, directory_path):
        """Eliminar directorios vacíos recursivamente"""
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.log_message(f"Eliminado directorio vacío: {dir_path}")
                        self.structure_data["actions_taken"].append(f"Removed empty directory {dir_path}")
                except OSError:
                    pass
    
    def save_final_state(self):
        """Guardar el estado final después de las modificaciones"""
        self.log_message("Guardando estado final de la estructura...")
        
        final_analysis = {
            "timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "analysis": self._analyze_directory(self.base_path),
            "actions_taken": self.structure_data["actions_taken"]
        }
        
        with open(self.base_path / "final_structure.json", "w", encoding="utf-8") as f:
            json.dump(final_analysis, f, indent=2, ensure_ascii=False)
        
        self.log_message("Estado final guardado en final_structure.json")

if __name__ == "__main__":
    controller = StructureController()
    
    # Analizar estructura actual
    analysis = controller.analyze_structure()
    
    # Generar recomendaciones
    controller.generate_recommendations()
    
    # Ejecutar limpieza
    controller.execute_cleanup()
    
    # Guardar estado final
    controller.save_final_state()
    
    print("\nProceso completado. Revisa los archivos:")
    print("- structure_analysis.log: Registro detallado del proceso")
    print("- structure_analysis.json: Análisis completo de la estructura")
    print("- final_structure.json: Estado final después de las modificaciones")
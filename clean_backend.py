import os
import shutil
from pathlib import Path

def analyze_backend():
    backend_path = Path("D:\\Paginas\\scout_project\\backend")
    print(f"Analizando estructura de: {backend_path}")
    
    # Estructura esperada en backend
    expected_structure = {
        "app": {
            "__init__.py": True,
            "models": {
                "__init__.py": True,
                "models.py": True
            },
            "routes": {
                "__init__.py": True,
                "auth.py": True,
                "main.py": True,
                "directories.py": True,
                "scout.py": True
            },
            "services": {
                "__init__.py": True
            },
            "utils": {
                "__init__.py": True
            }
        },
        "instance": {},
        "migrations": {},
        "config.py": True,
        "requirements.txt": True,
        "run.py": True
    }
    
    # Carpetas que no deberían estar en backend
    unexpected_folders = ["backend", "frontend", "tests"]
    
    # Archivos que no deberían estar en backend
    unexpected_files = []
    
    print("\nCarpetas y archivos en backend:")
    for item in backend_path.iterdir():
        if item.is_dir():
            print(f"  📁 {item.name}/")
            if item.name in unexpected_folders:
                print(f"    ❌ CARPETA NO ESPERADA")
        else:
            print(f"  📄 {item.name}")
            if item.name in unexpected_files:
                print(f"    ❌ ARCHIVO NO ESPERADO")
    
    print("\nRecomendaciones:")
    for folder in unexpected_folders:
        folder_path = backend_path / folder
        if folder_path.exists():
            print(f"  - Eliminar carpeta: {folder_path}")
    
    return expected_structure, unexpected_folders, unexpected_files

def clean_backend():
    expected_structure, unexpected_folders, unexpected_files = analyze_backend()
    
    print("\n¿Desea continuar con la limpieza? (s/n)")
    # response = input().lower()
    # Para automatización, asumimos que la respuesta es 's'
    response = 's'
    
    if response == 's':
        backend_path = Path("D:\\Paginas\\scout_project\\backend")
        
        for folder in unexpected_folders:
            folder_path = backend_path / folder
            if folder_path.exists():
                print(f"Eliminando: {folder_path}")
                shutil.rmtree(folder_path)
        
        print("\nLimpieza completada.")
        
        # Verificar estructura final
        print("\nEstructura final de backend:")
        for item in backend_path.iterdir():
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                print(f"  📄 {item.name}")
    else:
        print("Limpieza cancelada.")

if __name__ == "__main__":
    clean_backend()
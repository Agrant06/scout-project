@echo off
echo Configurando Git para el proyecto Scout...

echo Paso 1: Creando .gitignore limpio...
echo # Python > .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo MANIFEST >> .gitignore
echo. >> .gitignore
echo # Virtual Environment >> .gitignore
echo venv/ >> .gitignore
echo env/ >> .gitignore
echo ENV/ >> .gitignore
echo env.bak/ >> .gitignore
echo venv.bak/ >> .gitignore
echo scout_venv/ >> .gitignore
echo. >> .gitignore
echo # IDE >> .gitignore
echo .idea/ >> .gitignore
echo .vscode/ >> .gitignore
echo *.swp >> .gitignore
echo *.swo >> .gitignore
echo. >> .gitignore
echo # Database >> .gitignore
echo *.db >> .gitignore
echo *.sqlite3 >> .gitignore
echo backend/instance/*.db >> .gitignore
echo. >> .gitignore
echo # Logs >> .gitignore
echo *.log >> .gitignore
echo. >> .gitignore
echo # Environment variables >> .gitignore
echo .env >> .gitignore
echo .env.local >> .gitignore
echo. >> .gitignore
echo # OS generated files >> .gitignore
echo .DS_Store >> .gitignore
echo .DS_Store? >> .gitignore
echo ._* >> .gitignore
echo .Spotlight-V100 >> .gitignore
echo .Trashes >> .gitignore
echo ehthumbs.db >> .gitignore
echo Thumbs.db >> .gitignore
echo. >> .gitignore
echo # Node.js >> .gitignore
echo frontend/node_modules/ >> .gitignore
echo. >> .gitignore
echo # Documentation >> .gitignore
echo 1_documentacion_instrucciones/ >> .gitignore
echo. >> .gitignore
echo # Temporary files >> .gitignore
echo token_response.json >> .gitignore

echo Paso 2: Limpiando el cach  de Git...
git rm -r --cached .

echo Paso 3: Agregando archivos al repositorio...
git add .gitignore backend/ frontend/

echo Paso 4: Haciendo commit inicial...
git commit -m "Initial commit: Backend structure with Flask, SQLite, and API endpoints"

echo Paso 5: Conectando con GitHub...
git remote add origin https://github.com/Agrant06/scout-project.git
echo Paso 6: Subiendo a GitHub...
git push -u origin master

echo Proceso completado.
pause



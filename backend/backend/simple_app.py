from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Aplicación simple funcionando"

@app.route('/test')
def test():
    return "Ruta de prueba funcionando"

if __name__ == '__main__':
    app.run(debug=True)
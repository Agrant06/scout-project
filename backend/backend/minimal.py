from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Home</h1>"

@app.route('/auth/login')
def login():
    return "<h1>Login</h1>"

@app.route('/api/auth/login')
def api_login():
    return "<h1>API Login</h1>"

if __name__ == '__main__':
    app.run(debug=True)
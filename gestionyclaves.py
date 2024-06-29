from flask import Flask, request, render_template_string, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

# Función para agregar un usuario
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?, ?)",
              (username, generate_password_hash(password)))
    conn.commit()
    conn.close()

# Agregar usuarios (nombres de los integrantes)
add_user('Juan Rodriguez', 'Duoc2023')
add_user('Alexis Riveros', 'Duoc2024')

# Ruta principal
@app.route('/')
def home():
    return render_template_string('''
        <h1>Bienvenido</h1>
        <a href="{{ url_for('login') }}">Iniciar sesión</a>
    ''')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        user = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            return f'Bienvenido, {username}!'
        else:
            return 'Usuario o contraseña incorrectos'
    return render_template_string('''
        <h1>Iniciar sesión</h1>
        <form method="post">
            <input type="text" name="username" placeholder="Usuario" required><br>
            <input type="password" name="password" placeholder="Contraseña" required><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    ''')

if __name__ == '__main__':
    app.run(port=5800)

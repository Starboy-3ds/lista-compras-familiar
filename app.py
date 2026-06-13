from flask import Flask, render_template, request, redirect, url_for, session
import os
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_2026'

# Configuración Supabase
SUPABASE_URL = 'https://bmhqtkrcvofiqlzkyvxp.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtaHF0a3Jjdm9maXFsemt5dnhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzNjg3OTEsImV4cCI6MjA5Njk0NDc5MX0.m1W-ICY-iBECVTpvJ_Clcgk9dltKhsb3ModTpW1fm68'

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

# Configuración de usuarios
USUARIOS = {
    'Brandon': 'todosjuntos',
    'Yamibel': 'todosjuntos',
    'Bienvenido': 'todosjuntos',
    'Yamila': 'todosjuntos'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def capitalizar_texto(texto):
    if not texto:
        return texto
    texto = texto.strip()
    palabras = texto.split()
    palabras_capitalizadas = []
    for palabra in palabras:
        if palabra:
            palabra_capitalizada = palabra[0].upper() + palabra[1:].lower()
            palabras_capitalizadas.append(palabra_capitalizada)
    return ' '.join(palabras_capitalizadas)

def normalizar_texto(texto):
    return texto.lower().strip()

def cargar_listas():
    r_jumbo = requests.get(f'{SUPABASE_URL}/rest/v1/Jumbo?select=id,producto', headers=HEADERS)
    r_compres = requests.get(f'{SUPABASE_URL}/rest/v1/Compres?select=id,producto', headers=HEADERS)
    listajumbo = r_jumbo.json() if r_jumbo.status_code == 200 else []
    listacompres = r_compres.json() if r_compres.status_code == 200 else []
    return listajumbo, listacompres

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USUARIOS and USUARIOS[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    listajumbo, listacompres = cargar_listas()
    return render_template('index.html',
                         listajumbo=listajumbo,
                         listacompres=listacompres,
                         mensaje=session.pop('mensaje', None),
                         usuario=session.get('user'))

@app.route('/agregar_jumbo', methods=['POST'])
@login_required
def agregar_jumbo():
    elemento = request.form.get('elemento')
    if elemento:
        elemento = capitalizar_texto(elemento.strip())
        requests.post(f'{SUPABASE_URL}/rest/v1/Jumbo', headers=HEADERS, json={'producto': elemento})
        session['mensaje'] = f'✅ Agregado a JUMBO 🟥: {elemento}'
    return redirect(url_for('index'))

@app.route('/agregar_compres', methods=['POST'])
@login_required
def agregar_compres():
    elemento = request.form.get('elemento')
    if elemento:
        elemento = capitalizar_texto(elemento.strip())
        requests.post(f'{SUPABASE_URL}/rest/v1/Compres', headers=HEADERS, json={'producto': elemento})
        session['mensaje'] = f'✅ Agregado a COMPRES 🟨: {elemento}'
    return redirect(url_for('index'))

@app.route('/borrar', methods=['POST'])
@login_required
def borrar():
    lista = request.form.get('lista')
    elemento = request.form.get('elemento')

    if not elemento:
        session['mensaje'] = '❌ Debes escribir un elemento para borrar'
        return redirect(url_for('index'))

    tabla = 'Jumbo' if lista == 'jumbo' else 'Compres'
    nombre_tienda = 'JUMBO 🟥' if lista == 'jumbo' else 'COMPRES 🟨'

    listajumbo, listacompres = cargar_listas()
    lista_actual = listajumbo if lista == 'jumbo' else listacompres

    encontrado = None
    for item in lista_actual:
        if normalizar_texto(item['producto']) == normalizar_texto(elemento):
            encontrado = item
            break

    if encontrado:
        requests.delete(f'{SUPABASE_URL}/rest/v1/{tabla}?id=eq.{encontrado["id"]}', headers=HEADERS)
        session['mensaje'] = f'✅ "{encontrado["producto"]}" borrado de {nombre_tienda}'
    else:
        session['mensaje'] = f'❌ "{elemento}" no está en la lista'

    return redirect(url_for('index'))

@app.route('/comprar', methods=['POST'])
@login_required
def comprar():
    lista = request.form.get('lista')
    indices = request.form.getlist('indices')

    if not indices:
        session['mensaje'] = '❌ No seleccionaste ningún producto'
        return redirect(url_for('index'))

    listajumbo, listacompres = cargar_listas()
    lista_actual = listajumbo if lista == 'jumbo' else listacompres
    nombre_tienda = 'JUMBO 🟥' if lista == 'jumbo' else 'COMPRES 🟨'
    tabla = 'Jumbo' if lista == 'jumbo' else 'Compres'

    comprados = []
    for idx in indices:
        idx = int(idx)
        if 0 <= idx < len(lista_actual):
            item = lista_actual[idx]
            requests.delete(f'{SUPABASE_URL}/rest/v1/{tabla}?id=eq.{item["id"]}', headers=HEADERS)
            comprados.append(item['producto'])

    if comprados:
        session['mensaje'] = f'✅ Comprados de {nombre_tienda}: {", ".join(comprados)}'

    return redirect(url_for('index'))

@app.route('/vaciar', methods=['POST'])
@login_required
def vaciar():
    lista = request.form.get('lista')
    tabla = 'Jumbo' if lista == 'jumbo' else 'Compres'
    nombre_tienda = 'JUMBO 🟥' if lista == 'jumbo' else 'COMPRES 🟨'

    requests.delete(f'{SUPABASE_URL}/rest/v1/{tabla}?id=gt.0', headers=HEADERS)
    session['mensaje'] = f'🧹 Lista de {nombre_tienda} vaciada'

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
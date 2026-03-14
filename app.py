from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

ARCHIVO_JUMBO = 'lista_jumbo.json'
ARCHIVO_COMPRES = 'lista_compres.json'

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
    if os.path.exists(ARCHIVO_JUMBO):
        with open(ARCHIVO_JUMBO, 'r') as f:
            listajumbo = json.load(f)
    else:
        listajumbo = []
    
    if os.path.exists(ARCHIVO_COMPRES):
        with open(ARCHIVO_COMPRES, 'r') as f:
            listacompres = json.load(f)
    else:
        listacompres = []
    
    return listajumbo, listacompres

def guardar_listas(listajumbo, listacompres):
    with open(ARCHIVO_JUMBO, 'w') as f:
        json.dump(listajumbo, f, indent=2)
    with open(ARCHIVO_COMPRES, 'w') as f:
        json.dump(listacompres, f, indent=2)

@app.route('/')
def index():
    listajumbo, listacompres = cargar_listas()
    return render_template('index.html', 
                         listajumbo=listajumbo, 
                         listacompres=listacompres,
                         mensaje=session.pop('mensaje', None))

@app.route('/agregar', methods=['POST'])
def agregar():
    lista = request.form.get('lista')
    elementos_texto = request.form.get('elementos')
    
    elementos = [capitalizar_texto(e.strip()) for e in elementos_texto.split(',') if e.strip()]
    
    listajumbo, listacompres = cargar_listas()
    
    if lista == 'jumbo':
        listajumbo.extend(elementos)
        session['mensaje'] = f'✅ Agregados a JUMBO 🟥: {", ".join(elementos)}'
    elif lista == 'compres':
        listacompres.extend(elementos)
        session['mensaje'] = f'✅ Agregados a COMPRES 🟨: {", ".join(elementos)}'
    
    guardar_listas(listajumbo, listacompres)
    return redirect(url_for('index'))

@app.route('/borrar', methods=['POST'])
def borrar():
    lista = request.form.get('lista')
    elemento = request.form.get('elemento')
    
    listajumbo, listacompres = cargar_listas()
    
    if lista == 'jumbo':
        encontrado = None
        for item in listajumbo:
            if normalizar_texto(item) == normalizar_texto(elemento):
                encontrado = item
                break
        if encontrado:
            listajumbo.remove(encontrado)
            session['mensaje'] = f'✅ "{encontrado}" borrado de JUMBO 🟥'
    
    elif lista == 'compres':
        encontrado = None
        for item in listacompres:
            if normalizar_texto(item) == normalizar_texto(elemento):
                encontrado = item
                break
        if encontrado:
            listacompres.remove(encontrado)
            session['mensaje'] = f'✅ "{encontrado}" borrado de COMPRES 🟨'
    
    guardar_listas(listajumbo, listacompres)
    return redirect(url_for('index'))

@app.route('/comprar', methods=['POST'])
def comprar():
    lista = request.form.get('lista')
    indices = request.form.getlist('indices')
    
    listajumbo, listacompres = cargar_listas()
    
    if lista == 'jumbo':
        indices_ordenados = sorted([int(i) for i in indices], reverse=True)
        comprados = []
        for idx in indices_ordenados:
            if 0 <= idx < len(listajumbo):
                comprados.append(listajumbo[idx])
                listajumbo.pop(idx)
        if comprados:
            session['mensaje'] = f'✅ Comprados de JUMBO 🟥: {", ".join(comprados)}'
    
    elif lista == 'compres':
        indices_ordenados = sorted([int(i) for i in indices], reverse=True)
        comprados = []
        for idx in indices_ordenados:
            if 0 <= idx < len(listacompres):
                comprados.append(listacompres[idx])
                listacompres.pop(idx)
        if comprados:
            session['mensaje'] = f'✅ Comprados de COMPRES 🟨: {", ".join(comprados)}'
    
    guardar_listas(listajumbo, listacompres)
    return redirect(url_for('index'))

@app.route('/vaciar', methods=['POST'])
def vaciar():
    lista = request.form.get('lista')
    
    listajumbo, listacompres = cargar_listas()
    
    if lista == 'jumbo':
        listajumbo = []
        session['mensaje'] = '🧹 Lista de JUMBO 🟥 vaciada'
    elif lista == 'compres':
        listacompres = []
        session['mensaje'] = '🧹 Lista de COMPRES 🟨 vaciada'
    
    guardar_listas(listajumbo, listacompres)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
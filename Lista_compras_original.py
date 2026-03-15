import json
import os

# Archivos para guardar los datos
ARCHIVO_JUMBO = 'lista_jumbo.json'
ARCHIVO_COMPRES = 'lista_compres.json'
ARCHIVO_HISTORIAL = 'historial_compras.json'

# Funciones de formato
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

def buscar_elemento(lista, elemento_buscar):
    elemento_normalizado = normalizar_texto(elemento_buscar)
    for item in lista:
        if normalizar_texto(item) == elemento_normalizado:
            return item
    return None

def capitalizar_lista(lista):
    return [capitalizar_texto(item) for item in lista]

# Cargar listas
def cargar_listas():
    global listajumbo, listacompres, historial
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
    
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, 'r') as f:
            historial = json.load(f)
    else:
        historial = []
    
    # Capitalizar listas existentes
    listajumbo = capitalizar_lista(listajumbo)
    listacompres = capitalizar_lista(listacompres)

def guardar_listas():
    with open(ARCHIVO_JUMBO, 'w') as f:
        json.dump(listajumbo, f, indent=2)
    with open(ARCHIVO_COMPRES, 'w') as f:
        json.dump(listacompres, f, indent=2)
    with open(ARCHIVO_HISTORIAL, 'w') as f:
        json.dump(historial, f, indent=2)
    print("💾 Listas guardadas")

def eliminar_duplicados(lista):
    unicos = {}
    for item in lista:
        unicos[normalizar_texto(item)] = item
    return list(unicos.values())

def marcar_comprados():
    global listajumbo, listacompres, historial
    print('\n' + '=' * 60)
    print('✅ MARCAR PRODUCTOS COMPRADOS')
    print('=' * 60)
    
    print('\n🟥 JUMBO:')
    if listajumbo:
        for i, item in enumerate(listajumbo, 1):
            print(f'   {i}. {item}')
        
        seleccion = input('\nNúmeros a marcar (separados por comas): ')
        if seleccion.strip():
            indices = [int(x.strip()) for x in seleccion.split(',') if x.strip().isdigit()]
            indices.sort(reverse=True)
            
            comprados = []
            for idx in indices:
                if 1 <= idx <= len(listajumbo):
                    producto = listajumbo[idx-1]
                    comprados.append(producto)
                    listajumbo.pop(idx-1)
            
            if comprados:
                historial.append({
                    "fecha": "Ahora",
                    "tienda": "JUMBO",
                    "productos": comprados
                })
                print(f'✅ Comprados: {comprados}')
    else:
        print('   (Vacía)')
    
    print('\n🟨 COMPRES:')
    if listacompres:
        for i, item in enumerate(listacompres, 1):
            print(f'   {i}. {item}')
        
        seleccion = input('\nNúmeros a marcar (separados por comas): ')
        if seleccion.strip():
            indices = [int(x.strip()) for x in seleccion.split(',') if x.strip().isdigit()]
            indices.sort(reverse=True)
            
            comprados = []
            for idx in indices:
                if 1 <= idx <= len(listacompres):
                    producto = listacompres[idx-1]
                    comprados.append(producto)
                    listacompres.pop(idx-1)
            
            if comprados:
                historial.append({
                    "fecha": "Ahora",
                    "tienda": "COMPRES",
                    "productos": comprados
                })
                print(f'✅ Comprados: {comprados}')
    else:
        print('   (Vacía)')
    
    guardar_listas()

def clasificar_elementos(elementos):
    jumbo = []
    compres = []
    ambos = []
    
    print('\n📦 CLASIFICACIÓN:')
    for elem in elementos:
        print(f'\nProducto: "{elem}"')
        print('  [J] JUMBO  [C] COMPRES  [A] Ambos  [X] Descartar')
        while True:
            op = input('👉 Opción: ').upper()
            if op == 'J':
                jumbo.append(elem)
                break
            elif op == 'C':
                compres.append(elem)
                break
            elif op == 'A':
                ambos.append(elem)
                break
            elif op == 'X':
                break
            else:
                print('Opción no válida')
    
    if ambos:
        print('\n📦 Productos para AMBAS:')
        for e in ambos:
            print(f'   • {e}')
        print('\n¿Dónde agregarlos?')
        print('  1. Solo JUMBO')
        print('  2. Solo COMPRES')
        print('  3. Ambas')
        op = input('Opción: ')
        if op == '1':
            jumbo.extend(ambos)
        elif op == '2':
            compres.extend(ambos)
        elif op == '3':
            jumbo.extend(ambos)
            compres.extend(ambos)
    
    return jumbo, compres

# Cargar listas al iniciar
cargar_listas()

while True:
    print('')
    print('=' * 60)
    print('🏠 LISTA DE COMPRAS FAMILIAR (CONSOLA) 🏠')
    print('=' * 60)
    print('')
    print('📋 OPCIONES:')
    print('  1. 📝 INGRESO RÁPIDO (clasificar)')
    print('  2. 🟥 Añadir a JUMBO')
    print('  3. 🟨 Añadir a COMPRES')
    print('  4. 📋 Ver listas')
    print('  5. 🟥 Ver solo JUMBO')
    print('  6. 🟨 Ver solo COMPRES')
    print('  7. ✅ Marcar comprados')
    print('  8. 📊 Ver historial')
    print('  9. 🗑️ Borrar elementos')
    print('  10. 🧹 Eliminar duplicados')
    print('  11. ✏️ Editar elemento')
    print('  12. 🔄 Ver contador')
    print('  13. 🚪 Salir')
    print('')
    
    opcion = input('👉 Opción: ')
    
    if opcion == '1':  # INGRESO RÁPIDO
        print('\n📝 Ingrese productos (separados por comas):')
        entrada = input('✏️: ')
        elementos = [capitalizar_texto(e.strip()) for e in entrada.split(',') if e.strip()]
        if elementos:
            j, c = clasificar_elementos(elementos)
            if j:
                listajumbo.extend(j)
                print(f'✅ Agregados a JUMBO: {j}')
            if c:
                listacompres.extend(c)
                print(f'✅ Agregados a COMPRES: {c}')
            guardar_listas()
    
    elif opcion == '2':  # AÑADIR JUMBO
        entrada = input('✏️ Elementos (separados por comas): ')
        elementos = [capitalizar_texto(e.strip()) for e in entrada.split(',') if e.strip()]
        if elementos:
            listajumbo.extend(elementos)
            print(f'✅ Agregados: {elementos}')
            guardar_listas()
    
    elif opcion == '3':  # AÑADIR COMPRES
        entrada = input('✏️ Elementos (separados por comas): ')
        elementos = [capitalizar_texto(e.strip()) for e in entrada.split(',') if e.strip()]
        if elementos:
            listacompres.extend(elementos)
            print(f'✅ Agregados: {elementos}')
            guardar_listas()
    
    elif opcion == '4':  # VER TODO
        print('\n📋 LISTAS:')
        print(f'JUMBO 🟥: {listajumbo}')
        print(f'COMPRES 🟨: {listacompres}')
    
    elif opcion == '5':  # VER JUMBO
        print(f'\n🟥 JUMBO: {listajumbo}')
    
    elif opcion == '6':  # VER COMPRES
        print(f'\n🟨 COMPRES: {listacompres}')
    
    elif opcion == '7':  # MARCAR COMPRADOS
        marcar_comprados()
    
    elif opcion == '8':  # HISTORIAL
        print('\n📜 HISTORIAL:')
        if historial:
            for i, reg in enumerate(historial[-10:], 1):
                print(f'{i}. {reg["tienda"]}: {reg["productos"]}')
        else:
            print('No hay historial')
    
    elif opcion == '9':  # BORRAR
        print('\n🗑️ LISTAS:')
        print('  1. JUMBO')
        print('  2. COMPRES')
        l = input('Lista: ')
        
        if l == '1' and listajumbo:
            print(f'JUMBO: {listajumbo}')
            e = input('Elemento: ')
            encontrado = buscar_elemento(listajumbo, e)
            if encontrado:
                listajumbo.remove(encontrado)
                print(f'✅ "{encontrado}" borrado')
                guardar_listas()
        elif l == '2' and listacompres:
            print(f'COMPRES: {listacompres}')
            e = input('Elemento: ')
            encontrado = buscar_elemento(listacompres, e)
            if encontrado:
                listacompres.remove(encontrado)
                print(f'✅ "{encontrado}" borrado')
                guardar_listas()
    
    elif opcion == '10':  # DUPLICADOS
        antes_j = len(listajumbo)
        antes_c = len(listacompres)
        listajumbo = eliminar_duplicados(listajumbo)
        listacompres = eliminar_duplicados(listacompres)
        print(f'JUMBO: {antes_j - len(listajumbo)} eliminados')
        print(f'COMPRES: {antes_c - len(listacompres)} eliminados')
        guardar_listas()
    
    elif opcion == '11':  # EDITAR
        print('\n✏️ EDITAR:')
        print('  1. JUMBO')
        print('  2. COMPRES')
        l = input('Lista: ')
        
        if l == '1' and listajumbo:
            print(f'JUMBO: {listajumbo}')
            v = input('Elemento a editar: ')
            e = buscar_elemento(listajumbo, v)
            if e:
                n = input('Nuevo valor: ')
                n = capitalizar_texto(n)
                idx = listajumbo.index(e)
                listajumbo[idx] = n
                print(f'✅ "{e}" → "{n}"')
                guardar_listas()
        elif l == '2' and listacompres:
            print(f'COMPRES: {listacompres}')
            v = input('Elemento a editar: ')
            e = buscar_elemento(listacompres, v)
            if e:
                n = input('Nuevo valor: ')
                n = capitalizar_texto(n)
                idx = listacompres.index(e)
                listacompres[idx] = n
                print(f'✅ "{e}" → "{n}"')
                guardar_listas()
    
    elif opcion == '12':  # CONTADOR
        total = len(listajumbo) + len(listacompres)
        print(f'\n📊 TOTAL: {total}')
        print(f'JUMBO: {len(listajumbo)}')
        print(f'COMPRES: {len(listacompres)}')
    
    elif opcion == '13':  # SALIR
        print('\n👋 ¡Hasta luego!')
        break
    
    else:
        print('❌ Opción no válida')
    
    input('\nPresione Enter para continuar...')
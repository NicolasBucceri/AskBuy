from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone

import firebase_config
from firebase_config import get_db
import dynamic_tables

# Crear la app Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Usar Firestore correctamente
db = get_db()

# 🚀 Test de conexión
try:
    test_ref = db.collection("test").document("prueba").get()
    print("✅ Conexión a Firestore exitosa")
except Exception as e:
    print(f"⚠️ Error al conectar con Firestore: {e}")
    
    

# 🚀 Ruta para generar y guardar tablas dinámicas
@app.route('/api/product/<product_id>/generar_tablas', methods=['POST'])
def generar_y_guardar_tablas(product_id):
    """Genera tablas dinámicas según la categoría del producto."""
    
    data = request.json
    categoria = data.get("categoria", "").strip().lower()

    if not categoria:
        return jsonify({"error": "Se requiere la categoría"}), 400

    resultado = dynamic_tables.generar_tablas_dinamicas(product_id, categoria)

    return jsonify(resultado), 201

# 🚀 Obtener todos los productos
@app.route('/api/products', methods=['GET'])
def get_products():
    products_ref = db.collection('productos').stream()
    products_list = [{**product.to_dict(), "id": product.id} for product in products_ref]
    return jsonify(products_list)

# 🚀 Obtener un producto por ID
@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product_ref = db.collection('productos').document(product_id)
    product = product_ref.get()
    if product.exists:
        return jsonify(product.to_dict())
    return jsonify({"error": "Producto no encontrado"}), 404

# 🚀 Agregar un producto
@app.route('/api/products', methods=['POST'])
def add_product():
    if not request.json:
        return jsonify({"error": "No data provided"}), 400
    product_ref = db.collection('productos').add(request.json)
    return jsonify({"id": product_ref[1].id}), 201

# 🚀 Obtener todas las categorías
@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    categorias_ref = db.collection('categorias').stream()
    categorias_list = [categoria.to_dict()['nombre'] for categoria in categorias_ref]
    return jsonify(categorias_list)

# 🚀 Agregar una nueva categoría
@app.route('/api/categorias', methods=['POST'])
def add_categoria():
    data = request.json
    if 'nombre' not in data or not data['nombre'].strip():
        return jsonify({"error": "El nombre de la categoría es obligatorio"}), 400

    nueva_categoria = {"nombre": data['nombre'].strip()}
    db.collection('categorias').add(nueva_categoria)
    return jsonify({"message": "Categoría agregada exitosamente"}), 201

# 🚀 Eliminar una categoría por nombre
@app.route('/api/categorias/<nombre_categoria>', methods=['DELETE'])
def delete_categoria(nombre_categoria):
    categorias_ref = db.collection('categorias')
    query = categorias_ref.where('nombre', '==', nombre_categoria).stream()

    deleted = False
    for doc in query:
        doc.reference.delete()
        deleted = True

    if deleted:
        return jsonify({"message": "Categoría eliminada"}), 200
    return jsonify({"error": "Categoría no encontrada"}), 404

# 🚀 Actualizar categoría
@app.route('/api/categorias/<nombre_categoria>', methods=['PUT'])
def update_categoria(nombre_categoria):
    data = request.json
    if 'nombre' not in data or not data['nombre'].strip():
        return jsonify({"error": "El nuevo nombre es obligatorio"}), 400

    categorias_ref = db.collection('categorias')
    query = categorias_ref.where('nombre', '==', nombre_categoria).stream()

    updated = False
    for doc in query:
        doc.reference.update({"nombre": data['nombre'].strip()})
        updated = True

    if updated:
        return jsonify({"message": "Categoría actualizada"}), 200
    else:
        return jsonify({"error": "Categoría no encontrada"}), 404

# 🚀 Obtener todas las etiquetas
@app.route('/api/etiquetas', methods=['GET'])
def get_etiquetas():
    etiquetas_ref = db.collection('etiquetas').stream()
    etiquetas_list = [{"id": etiqueta.id, "nombre": etiqueta.to_dict()['nombre']} for etiqueta in etiquetas_ref]
    return jsonify(etiquetas_list)

# 🚀 Agregar una nueva etiqueta
@app.route('/api/etiquetas', methods=['POST'])
def add_etiqueta():
    data = request.json
    if 'nombre' not in data or not data['nombre'].strip():
        return jsonify({"error": "El nombre de la etiqueta es obligatorio"}), 400

    nueva_etiqueta = {"nombre": data['nombre'].strip()}
    doc_ref = db.collection('etiquetas').add(nueva_etiqueta)
    
    return jsonify({"id": doc_ref[1].id, "nombre": data['nombre'].strip()}), 201

# 🚀 Eliminar una etiqueta por ID
@app.route('/api/etiquetas/<etiqueta_id>', methods=['DELETE'])
def delete_etiqueta(etiqueta_id):
    etiqueta_ref = db.collection('etiquetas').document(etiqueta_id)
    if etiqueta_ref.get().exists:
        etiqueta_ref.delete()
        return jsonify({"message": "Etiqueta eliminada"}), 200
    return jsonify({"error": "Etiqueta no encontrada"}), 404

# 🚀 Editar etiqueta
@app.route('/api/etiquetas/<etiqueta_id>', methods=['PUT'])
def update_etiqueta(etiqueta_id):
    data = request.json
    if 'nombre' not in data or not data['nombre'].strip():
        return jsonify({"error": "El nuevo nombre es obligatorio"}), 400

    etiqueta_ref = db.collection('etiquetas').document(etiqueta_id)
    if etiqueta_ref.get().exists:
        etiqueta_ref.update({"nombre": data['nombre'].strip()})
        return jsonify({"message": "Etiqueta actualizada"}), 200
    return jsonify({"error": "Etiqueta no encontrada"}), 404

# 🚀 Agregar una nueva tabla dinámica
@app.route('/api/tablas-dinamicas', methods=['POST'])
def add_tabla_dinamica():
    """Guarda una nueva tabla dinámica en Firestore."""
    data = request.json
    if not data.get("titulo") or not data.get("categoria") or not data.get("subtablas"):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Crear la referencia en Firestore
    nueva_tabla_ref = db.collection('tablas_dinamicas').add(data)

    return jsonify({"id": nueva_tabla_ref[1].id, **data}), 201

# 🚀 Obtener todas las tablas dinámicas
@app.route('/api/tablas-dinamicas', methods=['GET'])
def get_tablas_dinamicas():
    """Retorna todas las tablas dinámicas disponibles en Firestore."""
    tablas_ref = db.collection('tablas_dinamicas').stream()
    tablas_list = [{**tabla.to_dict(), "id": tabla.id} for tabla in tablas_ref]
    
    return jsonify(tablas_list)

# 🚀 Obtener una tabla dinámica por ID
@app.route('/api/tablas-dinamicas/<tabla_id>', methods=['GET'])
def get_tabla_dinamica(tabla_id):
    """Retorna una tabla dinámica específica por su ID."""
    tabla_ref = db.collection('tablas_dinamicas').document(tabla_id).get()
    
    if not tabla_ref.exists:
        return jsonify({"error": "Tabla no encontrada"}), 404
    
    return jsonify({**tabla_ref.to_dict(), "id": tabla_id})

# 🚀 Actualizar una tabla dinámica
@app.route('/api/tablas-dinamicas/<tabla_id>', methods=['PUT'])
def update_tabla_dinamica(tabla_id):
    """Actualiza una tabla dinámica existente."""
    data = request.json
    if not data.get("titulo") or not data.get("categoria") or not data.get("subtablas"):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    tabla_ref = db.collection('tablas_dinamicas').document(tabla_id)
    
    if not tabla_ref.get().exists:
        return jsonify({"error": "Tabla no encontrada"}), 404

    tabla_ref.update(data)
    return jsonify({"message": "Tabla actualizada correctamente"})

# 🚀 Eliminar una tabla dinámica
@app.route('/api/tablas-dinamicas/<tabla_id>', methods=['DELETE'])
def delete_tabla_dinamica(tabla_id):
    """Elimina una tabla dinámica por su ID."""
    tabla_ref = db.collection('tablas_dinamicas').document(tabla_id)
    
    if not tabla_ref.get().exists:
        return jsonify({"error": "Tabla no encontrada"}), 404
    
    tabla_ref.delete()
    return jsonify({"message": "Tabla eliminada correctamente"})

@app.route('/api/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product_ref = db.collection('productos').document(product_id)
    if not product_ref.get().exists:
        return jsonify({"error": "Producto no encontrado"}), 404

    product_ref.delete()
    return jsonify({"message": "Producto eliminado correctamente"}), 200

# 🚀 Actualizar un producto completo por ID (versión PRO)
@app.route('/api/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza los datos de un producto existente en Firestore."""
    data = request.json

    # Validación básica
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    product_ref = db.collection('productos').document(product_id)
    producto_actual = product_ref.get()

    if not producto_actual.exists:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Campos válidos que se pueden actualizar
    campos_validos = {
    'nombre', 'precio', 'descuento', 'tipoDescuento',
    'porcentajeDescuento', 'montoDescuento', 'fechaVencimientoDescuento',
    'fechaYHoraVencimiento',
    'modelos', 'descripcion', 'categoria', 'etiquetas', 'stockDisponible',
    'imagen', 'imagenCarrusel', 'marca'
    }

    # Filtrar solo los campos válidos
    datos_filtrados = {k: v for k, v in data.items() if k in campos_validos}

    try:
        product_ref.update(datos_filtrados)
        return jsonify({"message": "✅ Producto actualizado correctamente"}), 200
    except Exception as e:
        print("❌ Error al actualizar producto:", e)
        return jsonify({"error": "Error al actualizar producto"}), 500
    
@app.route('/api/desactivar-descuentos-vencidos', methods=['POST'])
def desactivar_descuentos_vencidos():
    productos_ref = db.collection('productos').stream()
    ahora = datetime.now(timezone.utc)

    actualizados = 0
    for doc in productos_ref:
        producto = doc.to_dict()
        cambios = {}

        # Desactivar descuento en producto base
        fecha_venc = producto.get('fechaYHoraVencimiento')
        if producto.get('descuento') and fecha_venc:
            try:
                vencimiento = datetime.fromisoformat(fecha_venc)
                if vencimiento.tzinfo is None:
                    vencimiento = vencimiento.replace(tzinfo=timezone.utc)

                if vencimiento < ahora:
                    cambios.update({
                        'descuento': False,
                        'porcentajeDescuento': 0,
                        'montoDescuento': 0,
                        'tipoDescuento': None
                    })
            except Exception as e:
                print("❌ Fecha inválida en producto:", doc.id, e)

        # Desactivar descuento en modelos
        modelos = producto.get('modelos', [])
        modelos_actualizados = False
        for modelo in modelos:
            fecha_mod = modelo.get('fechaYHoraVencimiento')
            if modelo.get('descuento') and fecha_mod:
                try:
                    vencimiento_mod = datetime.fromisoformat(fecha_mod)
                    if vencimiento_mod.tzinfo is None:
                        vencimiento_mod = vencimiento_mod.replace(tzinfo=timezone.utc)

                    if vencimiento_mod < ahora:
                        modelo['descuento'] = False
                        modelo['porcentajeDescuento'] = 0
                        modelo['montoDescuento'] = 0
                        modelo['tipoDescuento'] = None
                        modelos_actualizados = True
                except Exception as e:
                    print("❌ Fecha inválida en modelo:", doc.id, e)

        if modelos_actualizados:
            cambios['modelos'] = modelos

        if cambios:
            doc.reference.update(cambios)
            actualizados += 1

    return jsonify({"message": f"{actualizados} descuentos desactivados"}), 200

@app.route('/api/product/<product_id>/modelo/<int:modelo_index>', methods=['DELETE'])
def delete_modelo(product_id, modelo_index):
    product_ref = db.collection('productos').document(product_id)
    product_doc = product_ref.get()

    if not product_doc.exists:
        return jsonify({"error": "Producto no encontrado"}), 404

    producto = product_doc.to_dict()
    modelos = producto.get('modelos', [])

    if modelo_index < 0 or modelo_index >= len(modelos):
        return jsonify({"error": "Índice de modelo inválido"}), 400

    # Eliminar el modelo
    modelos.pop(modelo_index)

    # Guardar la lista actualizada
    product_ref.update({'modelos': modelos})

    return jsonify({"message": "Modelo eliminado correctamente"}), 200

@app.route('/api/product/<product_id>/modelo-id/<modelo_id>', methods=['DELETE'])
def delete_modelo_por_id(product_id, modelo_id):
    product_ref = db.collection('productos').document(product_id)
    product_doc = product_ref.get()

    if not product_doc.exists:
        return jsonify({"error": "Producto no encontrado"}), 404

    producto = product_doc.to_dict()
    modelos = producto.get('modelos', [])

    nuevos_modelos = [m for m in modelos if str(m.get("id")) != str(modelo_id)]

    if len(nuevos_modelos) == len(modelos):
        return jsonify({"error": "Modelo no encontrado"}), 404

    product_ref.update({'modelos': nuevos_modelos})

    return jsonify({"message": "Modelo eliminado correctamente"}), 200
   
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # Guardar en Firestore
    db.collection('usuarios').add({
        "username": username,
        "email": email,
        "password": password  # ⚠️ No recomendado en texto plano
    })

    return jsonify({"message": "Usuario registrado correctamente"}), 201

from firebase_admin import auth  # Asegurate de tener esto al principio

# ✅ Obtener todos los usuarios desde Firestore (NO desde Firebase Auth)
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios_ref = db.collection('usuarios').stream()
        usuarios = []

        for doc in usuarios_ref:
            data = doc.to_dict()
            data['id'] = doc.id
            usuarios.append(data)

        return jsonify(usuarios), 200
    except Exception as e:
        print("❌ Error al obtener usuarios:", e)
        return jsonify({'error': 'Error al obtener usuarios'}), 500


# ✅ Actualizar cualquier campo de un usuario (nombre, dirección, etc.)
@app.route('/api/usuarios/<uid>', methods=['PUT'])
def actualizar_usuario(uid):
    data = request.json
    if not data:
        return jsonify({"error": "No se recibió información"}), 400

    try:
        user_ref = db.collection('usuarios').document(uid)
        user_ref.update(data)
        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except Exception as e:
        print("❌ Error al actualizar usuario:", e)
        return jsonify({"error": "Error al actualizar usuario"}), 500


# ✅ Ruta específica para cambiar el rol (más controlada y con validación)
@app.route('/api/usuarios/<id>/rol', methods=['PUT'])
def actualizar_rol(id):
    data = request.get_json()
    nuevo_rol = data.get('rol', '').strip().lower()

    if nuevo_rol not in ['admin', 'moderador', 'usuario']:
        return jsonify({'error': 'Rol inválido'}), 400

    usuario_ref = db.collection('usuarios').document(id)

    try:
        if not usuario_ref.get().exists:
            print("❌ Usuario no encontrado en Firestore")
            return jsonify({'error': 'Usuario no encontrado'}), 404

        usuario_ref.update({'rol': nuevo_rol})
        actualizado = usuario_ref.get().to_dict()
        print(f"📦 Rol actualizado: {actualizado}")

        return jsonify({'mensaje': f'Rol actualizado a {nuevo_rol}'}), 200

    except Exception as e:
        print(f"💥 Error al actualizar el rol: {e}")
        return jsonify({'error': 'Error del servidor'}), 500


# ✅ Obtener usuario por email (para login)
@app.route('/api/usuarios/by-email', methods=['GET'])
def obtener_usuario_por_email():
    email = request.args.get('email')
    print(f"🛬 Email recibido: {email}")

    if not email:
        return jsonify({'error': 'Falta el email'}), 400

    try:
        query = db.collection('usuarios').where('email', '==', email).limit(1).stream()

        for doc in query:
            usuario = doc.to_dict()
            usuario['id'] = doc.id
            print(f"✅ Usuario encontrado: {usuario}")
            return jsonify(usuario), 200

        print("❌ Usuario no encontrado")
        return jsonify({'error': 'Usuario no encontrado'}), 404

    except Exception as e:
        print(f"💥 Error al buscar por email: {e}")
        return jsonify({'error': 'Error del servidor'}), 500
    
from datetime import datetime, timezone

def desactivar_descuentos_vencidos():
    productos = db.collection('productos').stream()
    ahora = datetime.now(timezone.utc)
    actualizados = 0

    for doc in productos:
        producto = doc.to_dict()
        cambios = {}

        # 🟡 Producto base
        fecha_venc = producto.get('fechaYHoraVencimiento')
        if producto.get('descuento') and fecha_venc:
            try:
                vencimiento = datetime.fromisoformat(fecha_venc)
                if vencimiento.tzinfo is None:
                    vencimiento = vencimiento.replace(tzinfo=timezone.utc)

                if vencimiento < ahora:
                    cambios.update({
                        'descuento': False,
                        'porcentajeDescuento': 0,
                        'montoDescuento': 0,
                        'tipoDescuento': None,
                        'fechaYHoraVencimiento': None
                    })
            except Exception as e:
                print(f"❌ Error en producto {doc.id}: {e}")

        # 🟡 Modelos (si tiene)
        modelos = producto.get('modelos', [])
        modelos_actualizados = False
        for modelo in modelos:
            fecha_mod = modelo.get('fechaYHoraVencimiento')
            if modelo.get('descuento') and fecha_mod:
                try:
                    vencimiento_mod = datetime.fromisoformat(fecha_mod)
                    if vencimiento_mod.tzinfo is None:
                        vencimiento_mod = vencimiento_mod.replace(tzinfo=timezone.utc)

                    if vencimiento_mod < ahora:
                        modelo['descuento'] = False
                        modelo['porcentajeDescuento'] = 0
                        modelo['montoDescuento'] = 0
                        modelo['tipoDescuento'] = None
                        modelo['fechaYHoraVencimiento'] = None
                        modelos_actualizados = True
                except Exception as e:
                    print(f"❌ Error en modelo de {doc.id}: {e}")

        if modelos_actualizados:
            cambios['modelos'] = modelos

        if cambios:
            doc.reference.update(cambios)
            actualizados += 1

    print(f"✅ Descuentos vencidos desactivados: {actualizados}")

@app.route('/api/carruseles', methods=['GET'])
def get_carruseles():
    carruseles_ref = db.collection('carruselesHome').stream()
    carruseles = [{**doc.to_dict(), 'id': doc.id} for doc in carruseles_ref]
    return jsonify(carruseles), 200

@app.route('/api/carruseles', methods=['POST'])
def crear_carrusel():
    data = request.json
    if not data.get('nombre') or not isinstance(data.get('productos'), list):
        return jsonify({"error": "Faltan datos"}), 400

    doc_ref = db.collection('carruseles').add(data)
    return jsonify({"id": doc_ref[1].id}), 201

@app.route('/api/carruseles/<carrusel_id>', methods=['PUT'])
def actualizar_carrusel(carrusel_id):
    data = request.json
    carrusel_ref = db.collection('carruseles').document(carrusel_id)

    if not carrusel_ref.get().exists:
        return jsonify({"error": "Carrusel no encontrado"}), 404

    carrusel_ref.update(data)
    return jsonify({"message": "Carrusel actualizado"}), 200

@app.route('/api/carruseles/<carrusel_id>', methods=['DELETE'])
def eliminar_carrusel(carrusel_id):
    carrusel_ref = db.collection('carruseles').document(carrusel_id)

    if not carrusel_ref.get().exists:
        return jsonify({"error": "Carrusel no encontrado"}), 404

    carrusel_ref.delete()
    return jsonify({"message": "Carrusel eliminado"}), 200



# 🚀 Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)

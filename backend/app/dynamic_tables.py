from firebase_config import get_db  # Usamos la función que devuelve el cliente Firestore

def generar_tablas_dinamicas(product_id, categoria):
    db = get_db()  # Nos aseguramos que Firebase ya fue inicializado
    print(f"📢 Generando tablas dinámicas para {product_id} en la categoría {categoria}")

    categorias_map = {
        "mouses": "mouse",
        "teclados": "teclado",
        "monitores": "monitor",
        "auriculares": "auricular",
        "laptops": "laptop"
    }

    categoria_normalizada = categorias_map.get(categoria.lower(), categoria.lower())

    tablas_por_categoria = {
        "mouse": {
            "product_id": product_id,
            "Características Generales": {
                "Marca": "",
                "Línea": "",
                "Modelo": "",
                "Color": "",
            },
            "Sensor": {
                "Tipo de Sensor": "",
                "Resolución del Sensor": "",
            },
            "Tecnología": {
                "Con Bluetooth": "No",
                "Con Interruptor de Ahorro de Energía": "No",
            },
        },
        "teclado": {
            "product_id": product_id,
            "Características Generales": {
                "Marca": "",
                "Línea": "",
                "Modelo": "",
                "Color": "",
            },
            "Switches": {
                "Tipo de Switch": "",
                "Retroiluminación": "No",
                "Formato": "",
            },
            "Conectividad": {
                "Inalámbrico": "No",
                "Bluetooth": "No",
            },
        },
        "monitor": {
            "product_id": product_id,
            "Características Generales": {
                "Marca": "",
                "Tamaño de Pantalla": "",
                "Resolución": "",
                "Frecuencia de Refresco": "",
            },
            "Conectividad": {
                "HDMI": "Sí",
                "DisplayPort": "Sí",
                "VGA": "No",
            },
        }
    }

    if categoria_normalizada not in tablas_por_categoria:
        print(f"⚠️ Categoría '{categoria}' no está definida para generar tablas.")
        return {"error": f"Categoría '{categoria}' no tiene una tabla definida"}

    tabla = tablas_por_categoria[categoria_normalizada]

    db.collection("tablas_dinamicas").document(product_id).set(tabla)
    print(f"✅ Tabla guardada en 'tablas_dinamicas' para {product_id} en la categoría {categoria_normalizada}")

    return tabla

from flask import Blueprint, request, jsonify
import mercadopago
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

mercado_pago = Blueprint('mercado_pago', __name__)

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise RuntimeError("⚠️ MP_ACCESS_TOKEN no está definido en el archivo .env")

sdk = mercadopago.SDK(ACCESS_TOKEN)

@mercado_pago.route("/crear-preferencia", methods=["POST"])
def crear_preferencia():
    try:
        data = request.get_json() or {}
        print("📥 Datos recibidos del frontend:", data)

        nombre = data.get("nombre")
        cantidad = data.get("cantidad")
        precio = data.get("precio")
        imagen = data.get("imagen", "")

        print("➡️ Nombre:", nombre)
        print("➡️ Cantidad:", cantidad)
        print("➡️ Precio:", precio)
        print("➡️ Imagen:", imagen)

        if not all([nombre, cantidad, precio]):
            print("❌ Faltan campos obligatorios")
            return jsonify({"error": "Faltan campos obligatorios: nombre, cantidad, precio"}), 400

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except (ValueError, TypeError) as parse_error:
            print(f"❌ Error de conversión de cantidad/precio: {parse_error}")
            return jsonify({"error": "Cantidad o precio inválidos"}), 400

        # ⚠️ IMPORTANTE: este mail debe ser de un usuario de test DISTINTO al del ACCESS_TOKEN
        preference_data = {
            "items": [
                {
                    "title": nombre,
                    "quantity": cantidad,
                    "unit_price": precio,
                    "currency_id": "ARS",
                    "picture_url": imagen
                }
            ],
            "payer": {
                "email": "test_user_1545267392@testuser.com"  # Test user comprador (no loguees este user)
            },
            "back_urls": {
                "success": "http://localhost:5173/success",
                "failure": "http://localhost:5173/failure",
                "pending": "http://localhost:5173/pending"
            },
            #"auto_return": "approved"  # ✅ Te redirige automáticamente si se aprueba
        }

        # Crear la preferencia
        preference = sdk.preference().create(preference_data)
        print("✅ Preferencia generada:", preference.get("response"))

        response_data = preference.get("response", {})
        sandbox_point = response_data.get("sandbox_init_point")
        init_point = response_data.get("init_point")

        if not sandbox_point:
            print("❌ No se generó el link sandbox")
            return jsonify({"error": "No se pudo generar el link de pago"}), 500

        # Mostralo en consola para test
        print("🔗 Sandbox Init Point:", sandbox_point)

        return jsonify({
            "init_point": init_point,
            "sandbox_init_point": sandbox_point,
            "modo": "sandbox"
        })

    except Exception as e:
        print("💥 Error inesperado al crear preferencia:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# import firebase_admin
# from firebase_admin import credentials, firestore

# if not firebase_admin._apps:
#     cred = credentials.Certificate("backend/app/firebase-key.json")
#     firebase_admin.initialize_app(cred)

# def get_db():
#     return firestore.client()

import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Cargar variables del .env
load_dotenv()

# Leer ruta del JSON desde la variable de entorno
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print("🔐 Ruta de la credencial:", cred_path)  # Esto te ayuda a debuggear

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def get_db():
    return firestore.client()

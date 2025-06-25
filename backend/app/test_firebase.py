import firebase_admin
from firebase_admin import credentials, firestore

# Verificar si Firebase ya está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate("backend/app/askbuy-5b2b6-firebase-adminsdk-fbsvc-c0dab3a608.json")
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Intentar escribir un dato de prueba
doc_ref = db.collection("test").document("prueba")
doc_ref.set({"mensaje": "Conexión exitosa"})

print("✅ Conexión a Firebase y escritura de prueba realizada correctamente.")

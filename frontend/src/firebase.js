import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore' // ✅ lo necesitás

const firebaseConfig = {
  apiKey: "AIzaSyDDjp3oYaZx-yAH_1OMTUGwh6Chq0Tt9Rk",
  authDomain: "askbuy-5b2b6.firebaseapp.com",
  projectId: "askbuy-5b2b6",
  storageBucket: "askbuy-5b2b6.firebasestorage.app",
  messagingSenderId: "947312593308",
  appId: "1:947312593308:web:874ffc3515540465322059",
  measurementId: "G-979L7LLH1J"
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
const db = getFirestore(app) // ✅ ¡esto es esencial!

export { auth, db } // ✅ ahora funciona sin errores

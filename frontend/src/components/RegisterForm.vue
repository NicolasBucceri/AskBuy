<template>
  <!-- Toast personalizado -->
  <teleport to="body">
    <div class="noti-container" v-show="mostrarToast" aria-live="polite">
      <div :class="['noti-toast', toastTipo]">
        <i class="icono" :class="iconoToast"></i>
        <div class="contenido">
          <span class="titulo">{{ toastTitulo }}</span>
          <span class="tiempo">Ahora</span>
          <p class="mensaje">{{ toastMensaje }}</p>
        </div>
        <button class="btn-cerrar" @click="cerrarToast" aria-label="Cerrar notificación">&times;</button>
      </div>
    </div>
  </teleport>

  <form class="formularioRegistro" @submit.prevent="registrar">
    <h2 class="tituloPrincipal">Crear cuenta</h2>

    <div class="campoEntrada">
      <i class="fa-solid fa-user"></i>
      <input v-model="username" type="text" placeholder="Usuario" maxlength="20" />
    </div>

    <div class="campoEntrada">
      <i class="fas fa-envelope"></i>
      <input v-model="email" type="email" placeholder="Correo electrónico" />
    </div>

    <div class="campoEntrada" style="position: relative;">
      <i class="fas fa-lock"></i>
      <input :type="tipoPassword" v-model="password" placeholder="Contraseña" autocomplete="new-password"
        class="inputConIcono" />
      <button type="button" @click="togglePassword" class="verContraseniaBtn"
        style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer;"
        aria-label="Mostrar/Ocultar contraseña">
        <i :class="tipoPassword === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
      </button>
    </div>

    <!-- Requisitos en vivo -->
    <ul class="requisitosPassword" v-if="password">
      <li :class="{ cumplido: password.length >= 8 }">
        <i class="fas" :class="password.length >= 8 ? 'fa-check-circle' : 'fa-times-circle'"></i>
        Al menos 8 caracteres
      </li>
      <li :class="{ cumplido: /[A-Z]/.test(password) }">
        <i class="fas" :class="/[A-Z]/.test(password) ? 'fa-check-circle' : 'fa-times-circle'"></i>
        Una letra mayúscula
      </li>
      <li :class="{ cumplido: /\d/.test(password) }">
        <i class="fas" :class="/\d/.test(password) ? 'fa-check-circle' : 'fa-times-circle'"></i>
        Un número
      </li>
    </ul>



    <input type="submit" :value="cargando ? 'Registrando...' : 'Registrarse'" :disabled="cargando" class="btnForm" />

    <p class="socialTexto">O registrate con una red social</p>
    <div class="socialMedia">
      <!-- Google -->
      <a href="#" class="socialIcon" @click.prevent="loginConGoogle" title="Iniciar sesión con Google">
        <i class="fab fa-google"></i>
      </a>

      <!-- Microsoft -->
      <a href="#" class="socialIcon" @click.prevent="loginConMicrosoft" title="Iniciar sesión con Microsoft">
        <i class="fab fa-microsoft"></i>
      </a>

      <!-- Facebook -->
      <a href="#" class="socialIcon" @click.prevent="loginConFacebook" title="Iniciar sesión con Facebook">
        <i class="fab fa-facebook"></i>
      </a>
    </div>

    <p class="textoCuenta">¿Ya tenés una cuenta? <a href="#" id="btnIniciarSeccion2">Iniciar sesión</a></p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { auth } from '../firebase'
import {
  createUserWithEmailAndPassword,
  updateProfile,
  sendEmailVerification // 👈 Agregado
} from 'firebase/auth'
import { useRouter } from 'vue-router'
import { db } from '../firebase'
import { doc, setDoc, serverTimestamp } from 'firebase/firestore'

const username = ref('')
const email = ref('')
const password = ref('')
const cargando = ref(false)

const mostrarToast = ref(false)
const toastTitulo = ref('')
const toastMensaje = ref('')
const toastTipo = ref('info')
const iconoToast = ref('fas fa-info-circle')
let timeoutToast = null

const mostrarToastCustom = (titulo, mensaje, tipo = 'info') => {
  toastTitulo.value = titulo
  toastMensaje.value = mensaje
  toastTipo.value = tipo
  iconoToast.value =
    tipo === 'success' ? 'fas fa-check-circle' :
    tipo === 'error' ? 'fas fa-times-circle' :
    'fas fa-info-circle'

  mostrarToast.value = true
  clearTimeout(timeoutToast)
  timeoutToast = setTimeout(() => {
    mostrarToast.value = false
  }, 4000)
}

const router = useRouter()
const tipoPassword = ref('password')
const togglePassword = () => {
  tipoPassword.value = tipoPassword.value === 'password' ? 'text' : 'password'
}
const cerrarToast = () => {
  mostrarToast.value = false
}

// ✅ Dominios válidos permitidos
const dominiosValidos = [
  'gmail.com',
  'hotmail.com',
  'hotmail.com.ar',
  'outlook.com',
  'yahoo.com',
  'yahoo.com.ar',
  'gmail.com.ar'
]

const registrar = async () => {
  if (username.value.length > 20) {
    mostrarToastCustom('Nombre muy largo', '⚠️ El nombre debe tener como máximo 20 caracteres.', 'info')
    return
  }

  if (!/^[a-zA-Z0-9\s]+$/.test(username.value)) {
    mostrarToastCustom('Nombre inválido', 'Solo letras, números y espacios.', 'info')
    return
  }

  if (!username.value || !email.value || !password.value) {
    mostrarToastCustom('Campos incompletos', '⚠️ Completá todos los campos.', 'info')
    return
  }

  const validarPassword = (pass) => {
    if (pass.length < 8) return 'Debe tener al menos 8 caracteres.'
    if (!/[A-Z]/.test(pass)) return 'Debe incluir al menos una letra mayúscula.'
    if (!/\d/.test(pass)) return 'Debe incluir al menos un número.'
    return true
  }

  cargando.value = true

  const dominio = email.value.split('@')[1]?.toLowerCase()
  if (!dominiosValidos.includes(dominio)) {
    mostrarToastCustom(
      'Dominio no permitido',
      '⚠️ Usá un correo con un dominio conocido como @gmail.com o @hotmail.com.',
      'info'
    )
    cargando.value = false
    return
  }

  const validacion = validarPassword(password.value)
  if (validacion !== true) {
    mostrarToastCustom('Contraseña insegura', `🔐 ${validacion}`, 'info')
    cargando.value = false
    return
  }

  try {
    const cred = await createUserWithEmailAndPassword(auth, email.value, password.value)
    await updateProfile(cred.user, { displayName: username.value })
    await cred.user.reload()

    // ✅ Enviar mail de verificación
    await sendEmailVerification(cred.user)
    mostrarToastCustom('Verificación enviada', '📩 Revisa tu correo para confirmar la cuenta.', 'info')

    const rolAsignado = email.value === 'admin@askbuy.com' ? 'admin' : 'usuario'

    await setDoc(doc(db, 'usuarios', cred.user.uid), {
      nombre: username.value,
      email: email.value,
      rol: rolAsignado,
      fechaRegistro: serverTimestamp()
    })

    mostrarToastCustom('Registro exitoso', `🙌 Bienvenido ${auth.currentUser.displayName}`, 'success')

    setTimeout(() => {
      localStorage.setItem("registroRecienHecho", "true")
      router.push('/').then(() => {
        window.location.reload()
      })
    }, 500)

    username.value = ''
    email.value = ''
    password.value = ''
  } catch (err) {
    let mensaje = ''
    switch (err.code) {
      case 'auth/email-already-in-use':
        mensaje = '📧 Ese correo ya está en uso.'
        break
      case 'auth/invalid-email':
        mensaje = '📧 Correo no válido.'
        break
      case 'auth/weak-password':
        mensaje = '🔒 La contraseña debe tener al menos 6 caracteres.'
        break
      default:
        mensaje = '❌ Error: ' + err.message
    }
    mostrarToastCustom('Error al registrarse', mensaje, 'error')
  } finally {
    cargando.value = false
  }
}
</script>





<style scoped>
.noti-container {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 999999 !important;
}

.noti-toast {
  background-color: #212529;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  min-width: 280px;
  max-width: 350px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  gap: 12px;
  animation: slideIn 0.3s ease-out;
}

.noti-toast.success {
  border-left: 5px solid #28a745;
}

.noti-toast.error {
  border-left: 5px solid #dc3545;
}

.noti-toast.info {
  border-left: 5px solid #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.icono {
  margin-top: 2px;
  font-size: 1.2rem;
}

.contenido {
  flex: 1;
}

.titulo {
  display: block;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  /* ajustá según necesites */
}


.tiempo {
  font-size: 0.75rem;
  color: #ccc;
}

.mensaje {
  margin: 0.2rem 0 0;
  font-size: 0.9rem;
}

.btn-cerrar {
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.requisitosPassword {
  list-style: none;
  margin: 10px 0 20px;
  padding: 0 0 0 1.5rem;
  font-size: 0.9rem;
  color: #ccc;
  transition: all 0.3s ease;
}

.requisitosPassword li {
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #aaa;
}

.requisitosPassword li i {
  font-size: 0.9rem;
}

.requisitosPassword li.cumplido {
  color: #28a745;
}

.requisitosPassword li.cumplido i {
  color: #28a745;
}

</style>

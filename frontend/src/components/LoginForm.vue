<!-- LoginForm -->

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

  <form class="formularioIniciarSeccion" @submit.prevent="login">
    <h2 class="tituloPrincipal">Iniciar sesión</h2>

    <div class="campoEntrada">
      <i class="fa-solid fa-user"></i>
      <input v-model="email" type="email" placeholder="Correo electrónico" autocomplete="email" />
    </div>

    <div class="campoEntrada" style="position: relative;">
      <i class="fas fa-lock"></i>
      <input :type="tipoPassword" v-model="password" placeholder="Contraseña" autocomplete="current-password"
        class="inputConIcono" />
      <button type="button" @click="togglePassword" class="verContraseniaBtn"
        style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer;"
        aria-label="Mostrar/Ocultar contraseña">
        <i :class="tipoPassword === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
      </button>
    </div>

    <input :disabled="cargando" :value="cargando ? 'Ingresando...' : 'Ingresar'" class="btnForm" type="submit" />

    <p class="socialTexto">O iniciá sesión con una red social</p>
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


    <p class="textoCuenta">¿No tenés cuenta? <a href="#" id="btnRegistrarse2">Crear cuenta</a></p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import {
  GoogleAuthProvider,
  signInWithPopup,
  setPersistence,
  browserLocalPersistence,
  signInWithEmailAndPassword
} from 'firebase/auth'
import { auth } from '../firebase'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const email = ref('')
const password = ref('')
const tipoPassword = ref('password')
const cargando = ref(false)

const togglePassword = () => {
  tipoPassword.value = tipoPassword.value === 'password' ? 'text' : 'password'
}

// Toast personalizado
const mostrarToast = ref(false)
const toastTitulo = ref('')
const toastMensaje = ref('')
const toastTipo = ref('info') // success, error, info
const iconoToast = ref('fas fa-info-circle')
let timeoutToast = null

const mostrarToastCustom = (titulo, mensaje, tipo = 'info') => {
  toastTitulo.value = titulo
  toastMensaje.value = mensaje
  toastTipo.value = tipo
  iconoToast.value =
    tipo === 'success' ? 'fas fa-check-circle'
      : tipo === 'error' ? 'fas fa-times-circle'
        : 'fas fa-info-circle'

  mostrarToast.value = true

  clearTimeout(timeoutToast)
  timeoutToast = setTimeout(() => {
    mostrarToast.value = false
  }, 4000)
}

const cerrarToast = () => {
  mostrarToast.value = false
}

// Guardar en localStorage solo si es un objeto válido
const guardarUsuarioEnLocalStorage = (usuario) => {
  if (usuario && typeof usuario === 'object' && !Array.isArray(usuario)) {
    localStorage.setItem('usuarioActual', JSON.stringify(usuario))
    console.log('✅ Usuario guardado:', usuario)
  } else {
    console.warn('❌ No se guardó usuarioActual porque vino mal:', usuario)
  }
console.log('ROL del usuario:', usuario.rol)

}

// LOGIN con email/contraseña
const login = async () => {
  if (!email.value && !password.value) {
    mostrarToastCustom('Campos vacíos', '⚠️ Completá todos los campos.', 'info')
    return
  }
  if (!email.value) {
    mostrarToastCustom('Falta correo', '📧 Ingresá tu correo.', 'info')
    return
  }
  if (!password.value) {
    mostrarToastCustom('Falta contraseña', '🔒 Ingresá tu contraseña.', 'info')
    return
  }

  cargando.value = true
  try {
    await signInWithEmailAndPassword(auth, email.value, password.value)
    const usuarioFirebase = auth.currentUser
    console.log('📧 Email recibido de Firebase:', usuarioFirebase.email)

    // Consultar a tu backend
    const res = await axios.get(`http://localhost:5000/api/usuarios/by-email?email=${usuarioFirebase.email}`)
    console.log('📦 Respuesta del backend:', res.data)


    const usuarioCompleto = res.data

    guardarUsuarioEnLocalStorage(usuarioCompleto)

    mostrarToastCustom('Login exitoso', '🔥 Iniciaste sesión como un campeón!', 'success')
    router.push('/')
  } catch (err) {
    let mensaje = ''
    switch (err.code) {
      case 'auth/invalid-email':
        mensaje = '📧 El correo no es válido.'
        break
      case 'auth/user-not-found':
        mensaje = '😕 No existe una cuenta con ese correo.'
        break
      case 'auth/wrong-password':
        mensaje = '🔒 Contraseña incorrecta.'
        break
      case 'auth/missing-password':
        mensaje = '⚠️ Ingresá una contraseña.'
        break
      default:
        mensaje = '❌ Ocurrió un error: ' + err.message
    }
    mostrarToastCustom('Error al iniciar sesión', mensaje, 'error')
  } finally {
    cargando.value = false
  }
}

// LOGIN con Google
const loginConGoogle = async () => {
  cargando.value = true
  try {
    await setPersistence(auth, browserLocalPersistence)
    const provider = new GoogleAuthProvider()
    const result = await signInWithPopup(auth, provider)

    // Consultar a tu backend para traer info completa del usuario
    const res = await axios.get(`http://localhost:5000/api/usuarios/by-email?email=${result.user.email}`)
    const usuarioCompleto = res.data

    guardarUsuarioEnLocalStorage(usuarioCompleto)

    mostrarToastCustom('Login con Google', `🙌 Bienvenido ${result.user.displayName}`, 'success')
    router.push('/home')
  } catch (err) {
    mostrarToastCustom('Error al iniciar con Google', '❌ Ocurrió un error al iniciar sesión.', 'error')
    console.log(err)
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
</style>
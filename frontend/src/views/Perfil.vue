<template>
  <div class="perfil-container">
    <!-- 🔘 Botón hamburguesa solo en mobile, ubicado arriba del layout -->
      <button class="btn-hamburguesa" v-if="windowWidth < 768 && estaArriba" @click="toggleSidebarMobile">
        <i class="fas fa-bars"></i>
      </button>


    <!-- 🖥 Sidebar para desktop -->
    <SidebarPerfil v-if="windowWidth >= 768" :seccionActiva="seccionActiva"
      @update:seccionActiva="seccionActiva = $event" @cerrarSesion="cerrarSesion" />

    <!-- 📱 Sidebar modal para mobile -->
<transition name="slide-sidebar">
  <div class="sidebar-overlay" v-if="mostrarSidebarMobile && windowWidth < 768" @click.self="toggleSidebarMobile">
    
    <!-- ❌ Botón cerrar -->
    <button class="btn-cerrar-sidebar" @click="toggleSidebarMobile">
      <i class="fas fa-times"></i>
    </button>

    <SidebarPerfil
      :seccionActiva="seccionActiva"
      @update:seccionActiva="(id) => { seccionActiva = id; toggleSidebarMobile() }"
      @cerrarSesion="cerrarSesion"
    />
  </div>
</transition>



    <!-- Contenido principal -->
    <div class="perfil-wrapper">
      <div class="perfil-layout">
        <!-- IZQUIERDA: avatar + email -->
        <div class="perfil-left">
          <div class="avatar-preview">
            <img :src="avatarSeleccionado.src" />
          </div>
          <button class="btn btn-sm btn-outline-secondary mt-2" data-bs-toggle="modal" data-bs-target="#modalAvatar">
            <i class="fa-solid fa-pen me-1"></i> Editar imagen
          </button>

          <ModalSeleccionAvatar :avatars="avataresDisponibles" :modelValue="avatarSeleccionado.id"
            @update:modelValue="actualizarAvatarSeleccionado" />

          <div class="datos-usuario" v-if="user">
            <div class="dato-linea">
              <i class="fa-solid fa-envelope"></i>
              <span>{{ user.email }}</span>
            </div>
            <div class="dato-linea uid">
              <i class="fa-solid fa-fingerprint"></i>
              <span>{{ user.uid }}</span>
            </div>
          </div>

          <div v-else class="text-muted small mt-3 d-flex flex-column align-items-center">
            <i class="fas fa-spinner fa-spin fa-2x mb-2 text-secondary"></i>
            Cargando perfil...
          </div>
        </div>

        <!-- DERECHA: componente hijo -->
        <div class="perfil-right">
          <VistaDatosPersonales v-if="seccionActiva === 1" ref="telefonoInput" :nombre="nombre"
            :fechaNacimiento="fechaNacimiento" :direccion="direccion" :fechaMaxima="fechaMaxima"
            :numeroValido="numeroValido" :mostrarBotonVerificar="mostrarBotonVerificar" :telefono="telefono"
            @update:nombre="nombre = $event" @update:fechaNacimiento="fechaNacimiento = $event"
            @update:direccion="direccion = $event" @update:telefono="telefono = $event"
            @abrirModalVerificacion="abrirModalVerificacion" @guardar="guardarPerfil" />

          <VistaFavoritos v-if="seccionActiva === 2" :productos="productosFavoritos" @quitarFavorito="quitarFavorito" />

          <VistaHistorial v-if="seccionActiva === 3" />

          <VistaConfiguracionAvanzada v-if="seccionActiva === 4" />

        </div>

      </div>
    </div>

    <ToastNotificaciones ref="toastRef" />
    <ModalVerificarNumero v-if="mostrarModalVerificacion" :numero-telefono="telefono"
      @cerrar="mostrarModalVerificacion = false" @verificado="numeroVerificado.value = true"
      @actualizarTelefono="telefono = $event" />

  </div>
</template>



<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue'
import { auth, db } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'
import { getDoc, doc, setDoc } from 'firebase/firestore'
import axios from 'axios'

import avatar1 from '../assets/Avatares/chicaPerfil1.png'
import avatar2 from '../assets/Avatares/chicaPerfil2.png'
import avatar3 from '../assets/Avatares/chicaPerfil3.png'
import avatar4 from '../assets/Avatares/chicoPerfil1.png'
import avatar5 from '../assets/Avatares/chicoPerfil2.png'
import avatar6 from '../assets/Avatares/chicoPerfil3.png'
import avatarNeutro from '../assets/Avatares/avatarNeutro.png'

import ModalSeleccionAvatar from '../components/ModalSeleccionAvatar.vue'
import ToastNotificaciones from '../components/ToastNotificacion.vue'
import SidebarPerfil from '../components/SidebarPerfil.vue'
import ModalVerificarNumero from '../components/Modals/ModalVerificarNumero.vue'
import VistaDatosPersonales from '../components/SeccionesDePerfil/VistaDatosPersonales.vue'
import VistaFavoritos from '../components/SeccionesDePerfil/VistaFavoritos.vue'
import VistaHistorial from '../components/SeccionesDePerfil/VistaHistorial.vue'
import VistaConfiguracionAvanzada  from '../components/SeccionesDePerfil/VistaConfiguracionAvanzada.vue'



// Avatares disponibles
const avataresDisponibles = [
  { id: 'avatar1', src: avatar1 },
  { id: 'avatar2', src: avatar2 },
  { id: 'avatar3', src: avatar3 },
  { id: 'avatar4', src: avatar4 },
  { id: 'avatar5', src: avatar5 },
  { id: 'avatar6', src: avatar6 },
  { id: 'neutro', src: avatarNeutro }
]

// Refs generales
const seccionGuardada = parseInt(localStorage.getItem('seccionPerfil')) || 1
const seccionActiva = ref(seccionGuardada)
const user = ref(null)
const nombre = ref('')
const telefono = ref('')
const fechaNacimiento = ref('')
const direccion = ref({
  calle: '',
  numero: '',
  depto: '',
  cp: '',
  ciudad: '',
  provincia: '',
  pais: 'Argentina'
})
const avatarSeleccionado = ref(avataresDisponibles.find(a => a.id === 'neutro'))
const telefonoInput = ref(null)
const mostrarModalVerificacion = ref(false)
const numeroParaVerificar = ref('')
const numeroValido = ref(false)
const mostrarBotonVerificar = ref(false)
const toastRef = ref(null)
const productosFavoritos = ref([])
const mostrarSidebarMobile = ref(false)
const toggleSidebarMobile = () => {
  mostrarSidebarMobile.value = !mostrarSidebarMobile.value
}


// Guardar perfil
const guardarPerfil = async () => {
  try {
    const user = auth.currentUser
    if (!user) return

    const inputInterno = telefonoInput.value?.$refs?.telefonoInput
    const itiInterno = telefonoInput.value?.iti
    let numero = ''

    if (itiInterno && itiInterno.getNumber()) {
      numero = itiInterno.getNumber()
    } else if (inputInterno?.value) {
      numero = inputInterno.value
    }

    telefono.value = numero || null

    const userRef = doc(db, 'usuarios', user.uid)
    await setDoc(userRef, {
      nombre: nombre.value,
      fechaNacimiento: fechaNacimiento.value,
      direccion: direccion.value,
      telefono: telefono.value,
      avatar: avatarSeleccionado.value.id,
      actualizado: new Date().toISOString()
    }, { merge: true })

    toastRef.value?.mostrar('Datos guardados con éxito', '', 'success')
  } catch (err) {
    console.error('❌ Error al guardar perfil:', err)
    toastRef.value?.mostrar('Error al guardar', err.message, 'error')
  }
}

const guardarCambios = guardarPerfil

// 🔄 Carga de usuario y favoritos
onMounted(() => {
  onAuthStateChanged(auth, async (u) => {
    user.value = u
    if (!u) return

    const userRef = doc(db, "usuarios", u.uid)
    const docSnap = await getDoc(userRef)
    if (docSnap.exists()) {
      const data = docSnap.data()
      nombre.value = data.nombre || u.displayName || ""
      fechaNacimiento.value = data.fechaNacimiento || ""
      direccion.value = data.direccion || direccion.value
      telefono.value = data.telefono || ''
      avatarSeleccionado.value = avataresDisponibles.find(a => a.id === data.avatar) || avataresDisponibles[0]

      // ✅ Carga inicial de favoritos
      await cargarProductosFavoritos()
    }
  })
})


// Varios
watch(seccionActiva, (nueva) => {
  console.log('📌 Sección activa ahora es:', nueva)
})

const abrirModalVerificacion = () => {
  numeroParaVerificar.value = telefonoInput.value?.value || ''
  mostrarModalVerificacion.value = true
}

const hoy = new Date()
const hace18Anios = new Date(hoy.getFullYear() - 18, hoy.getMonth(), hoy.getDate())
const fechaMaxima = hace18Anios.toISOString().split('T')[0]

const calcularEdad = computed(() => {
  if (!fechaNacimiento.value) return ''
  const nacimiento = new Date(fechaNacimiento.value)
  let edad = hoy.getFullYear() - nacimiento.getFullYear()
  const mes = hoy.getMonth() - nacimiento.getMonth()
  if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) edad--
  return edad
})

const nombreEsValido = (nombre) => {
  const limpio = limpiarTexto(nombre)
  return !palabrasProhibidas.some(pal => limpio.includes(pal))
}

const limpiarTexto = (texto) => texto
  .toLowerCase()
  .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/[^a-z0-9]/g, '')

const palabrasProhibidas = ['pito', 'pene', 'mierda', 'caca', 'concha', 'verga', 'puta']

const actualizarAvatarSeleccionado = (id) => {
  avatarSeleccionado.value = avataresDisponibles.find(a => a.id === id) || avataresDisponibles[0]
}

const cargarProductosFavoritos = async () => {
  const user = auth.currentUser
  if (!user) return

  const userRef = doc(db, "usuarios", user.uid)
  const docSnap = await getDoc(userRef)
  if (docSnap.exists()) {
    const idsFavoritos = docSnap.data().favoritos || []
    const res = await axios.get('http://localhost:5000/api/products')
    productosFavoritos.value = res.data.filter(p => idsFavoritos.includes(p.id))
    console.log('🧠 Productos favoritos encontrados:', productosFavoritos.value)

  }
}

// 💡 Esto lo expone globalmente para que lo llames desde otros componentes
window.cargarProductosFavoritos = cargarProductosFavoritos

const quitarFavorito = async (idProducto) => {
  const userActual = auth.currentUser
  if (!userActual) return

  const userRef = doc(db, "usuarios", userActual.uid)
  const docSnap = await getDoc(userRef)

  if (!docSnap.exists()) return

  const data = docSnap.data()
  const nuevosIds = (data.favoritos || []).filter(id => id !== idProducto)

  await setDoc(userRef, { favoritos: nuevosIds }, { merge: true })

  // Refrescar productos
  if (window?.cargarProductosFavoritos) {
    window.cargarProductosFavoritos()
  }

  toastRef.value?.mostrar("Producto eliminado de favoritos", "", "info")
}

const windowWidth = ref(window.innerWidth)
onMounted(() => {
  window.addEventListener("resize", () => {
    windowWidth.value = window.innerWidth
  })
})

const estaArriba = ref(true)

onMounted(() => {
  window.addEventListener("scroll", () => {
    estaArriba.value = window.scrollY < 80
  })

  window.addEventListener("resize", () => {
    windowWidth.value = window.innerWidth
  })
})



watch(seccionActiva, (nueva) => {
  console.log('📌 Sección activa ahora es:', nueva)
  localStorage.setItem('seccionPerfil', nueva)
})

watch(telefono, (nuevo) => {
  console.log('📥 Teléfono recibido en el padre:', nuevo)
})
</script>








<style scoped>
body {
  margin: 0;
  padding: 0;
}

.tituloSeccion {
  margin-bottom: 20px;
  font-weight: bold;
  font-size: 25px;
}

.perfil-container {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  width: 100%;
}

.sidebarPerfil {
  position: relative;
  height: auto;
  flex-shrink: 0;
  width: 80px;
}

.perfil-wrapper {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: auto;
  background-color: #f5f5f5;
  border-radius: 1.5rem;
  box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.05);
}

.perfil-layout {
  display: flex;
  flex-direction: row;
  background-color: #e8e8e8;
  color: #222;
  min-height: 700px;
  border-radius: 1.5rem;
  padding: 2rem;
  gap: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.perfil-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #ccc;
  padding: 2rem 1rem;
}

.perfil-right {
  flex: 3;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.avatar-preview img {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.perfil-avatar-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.avatar-option {
  position: relative;
  cursor: pointer;
  border-radius: 50%;
  overflow: hidden;
  transition: transform 0.2s;
}

.avatar-option:hover {
  transform: scale(1.1);
}

.avatar-option input[type="radio"] {
  display: none;
}

.avatar-option img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid transparent;
}

.avatar-option input[type="radio"]:checked+img {
  border-color: var(--colorTerciario);
}

.datos-usuario {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #444;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
  text-align: center;
}

.dato-linea {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dato-linea i {
  color: var(--colorPrincipal);
  font-size: 1rem;
}

.dato-linea.uid {
  font-size: 0.8rem;
  color: #777;
  word-break: break-word;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.25rem;
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  color: var(--colorTextoPrincipal);
}

input.form-control {
  width: 100%;
  padding: 0.9rem 1.1rem;
  font-size: 0.95rem;
  border: 1px solid #d0d0d0;
  border-radius: 12px;
  background-color: #fdfdfd;
  color: #333;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

input.form-control:hover {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 0 2px rgba(255, 193, 7, 0.2);
}

input.form-control:focus {
  border-color: var(--colorPrincipal);
  box-shadow: 0 0 0 2px rgba(13, 110, 253, 0.25);
  outline: none;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(0.6);
  cursor: pointer;
}

.btn-editar {
  background-color: var(--colorTerciario);
  color: #000;
  border: none;
  padding: 0.9rem 1.5rem;
  border-radius: 30px;
  font-weight: 700;
  font-size: 1rem;
  width: 100%;
  transition: all 0.3s ease;
  margin-top: 2rem;
}

.btn-editar:hover {
  background-color: var(--colorTerciarioHover);
  color: white;
}

.btn-verificar-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.aviso-edad-invalida {
  color: #dc3545;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.aviso-edad-invalida::before {
  display: inline-block;
}

.hamburguesa-wrapper {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-start;
}

.btn-hamburguesa {
  position: absolute; /* 👈 en vez de fixed */
  top: 5rem;
  left: 1rem;
  z-index: 10;
  background: var(--colorPrincipal);
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.btn-hamburguesa:hover {
  background: var(--colorPrincipalHover);
  transform: scale(1.05);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 80px;
  height: 100vh;
  background: #343a40;
  z-index: 998;
  padding-top: 60px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
}

/* Slide desde la izquierda */
.slide-sidebar-enter-active {
  animation: slideIn 0.3s forwards;
}

.slide-sidebar-leave-active {
  animation: slideOut 0.3s forwards;
}

.btn-cerrar-sidebar {
  position: absolute;
  top: 12px;
  right: 30px;
  background: transparent;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  z-index: 999;
  transition: transform 0.2s ease;
}

.btn-cerrar-sidebar:hover {
  transform: scale(1.2);
  color: var(--colorTerciario);
}


@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }

  to {
    transform: translateX(-100%);
    opacity: 0;
  }
}


@media (max-width: 768px) {

  .btn-hamburguesa {
    display: flex; /* Mostrar en mobile */
  }

  .hamburguesa-wrapper {
    display: none; /* Ya no la necesitamos visualmente */
  }

  .perfil-layout {
    flex-direction: column;
    padding: 1.5rem 1rem;
  }

  .perfil-left {
    border-right: none;
    border-bottom: 1px solid #ccc;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
  }

  .perfil-right {
    justify-content: flex-start;
  }

  .perfil-wrapper {
    padding: 1rem;
  }

  .tituloSeccion {
    font-size: 1.4rem;
    text-align: center;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .perfil-wrapper {
    padding: 1rem 0.8rem;
  }

  .perfil-left {
    padding: 1rem 0.5rem;
  }

  .avatar-preview img {
    width: 80px;
    height: 80px;
  }

  .tituloSeccion {
    font-size: 1.2rem;
    text-align: center;
  }

  .dato-linea.uid {
    display: none;
  }

  .btn-editar {
    font-size: 0.9rem;
    padding: 0.7rem 1rem;
  }
}
</style>

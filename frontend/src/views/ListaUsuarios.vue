<template>
  <div class="usuarios-container">
    <h1 class="titulo">
      <i class="fas fa-users text-white"></i> Usuarios Registrados
    </h1>

    <div class="filtros-usuarios">
      <input type="text" v-model="filtroBusqueda" placeholder="🔎 Buscar por nombre o email..." />

      <select v-model="filtroRol">
        <option value="">Todos</option>
        <option value="admin">Admins</option>
        <option value="moderador">Moderadores</option>
        <option value="usuario">Usuarios</option>
      </select>
    </div>

    <div class="usuarios-grid">
      <div class="card-usuario" v-for="usuario in usuariosFiltrados" :key="usuario.id">
        <div class="info-principal">
          <h2>{{ usuario.nombre }}</h2>
          <p class="email">{{ usuario.email }}</p>
          <span :class="['rol', usuario.rol ? usuario.rol.toLowerCase() : 'usuario']">
            {{ rolVisual(usuario.rol) }}

          </span>

        </div>

        <div class="acciones">
          <button class="btn-icono" @click="verUsuario(usuario)" title="Ver">
            <i class="fas fa-eye"></i>
          </button>

          <button class="btn-icono" @click="borrarUsuario(usuario)"
            v-if="usuarioActual.rol === 'admin' && usuario.id !== usuarioActual.id" title="Eliminar">

            <i class="fas fa-trash-alt"></i>
          </button>


        </div>

        <div v-if="usuarioActual.rol === 'admin'" class="cambio-rol">
          <i class="fas fa-user-cog" style="margin-right: 6px; color: #ffc107;"></i>
          <label>Cambiar rol:</label>
          <select :value="usuario.rol" @change="e => cambiarRolManual(usuario, e.target.value)"
            :disabled="usuario.id === usuarioActual.id"
            :title="usuario.id === usuarioActual.id ? 'No podés cambiar tu propio rol' : ''">
            <option v-for="rol in rolesDisponibles" :key="rol" :value="rol">
              {{ rol === usuario.rol ? '✔ ' : '' }}{{ rol.charAt(0).toUpperCase() + rol.slice(1) }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div v-if="usuariosFiltrados.length === 0" class="text-center text-white-50 mt-5">
      <i class="fas fa-user-slash fa-2x mb-2"></i>
      <p>No se encontraron usuarios que coincidan con la búsqueda</p>
    </div>
  </div>

  <ModalConfirmacion ref="modalConfirmacionRef"
    :mensaje="usuarioAEliminar ? `¿Querés eliminar a ${usuarioAEliminar.nombre}?` : ''" color-boton="btn-danger"
    @confirmar="confirmarEliminacion" />

  <Notificacion ref="notificacionRef" />

  <SpinnerCarga ref="spinnerRef" mensaje="Cargando usuarios..." />

  <ModalVerUsuario ref="modalVerUsuarioRef" :usuario="usuarioSeleccionado" />

</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { doc, deleteDoc } from 'firebase/firestore'
import { db } from '../firebase' // Asegurate de que el path sea correcto
import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'
import Notificacion from '../components/ToastNotificacion.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'
import ModalVerUsuario from '../components/Modals/ModalVerUsuario.vue'

const usuarios = ref([])
const usuarioActual = ref(null)
const rolesDisponibles = ['admin', 'moderador', 'usuario']
const notificacionRef = ref(null)
const modalConfirmacionRef = ref(null)
const usuarioAEliminar = ref(null)
const modalVerUsuarioRef = ref(null)
const usuarioSeleccionado = ref(null)
const spinnerRef = ref(null)


// ✅ Normalizador de roles
const normalizarRol = (rolCrudo) => {
  const rol = rolCrudo?.toLowerCase().trim()
  return ['admin', 'moderador', 'usuario'].includes(rol) ? rol : 'usuario'
}

const cargarUsuarioDesdeStorage = () => {
  const guardado = localStorage.getItem('usuarioActual')
  if (guardado) {
    try {
      usuarioActual.value = JSON.parse(guardado)
    } catch (e) {
      console.warn('❌ Error al leer localStorage:', e)
    }
  }
}

const verUsuario = (usuario) => {
  usuarioSeleccionado.value = usuario
  modalVerUsuarioRef.value?.abrir()
}

// 🔄 Cargar usuarios
const cargarUsuariosYUsuarioActual = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/usuarios')
    const lista = res.data.map(usuario => ({
      id: usuario.id,
      nombre: usuario.nombre,
      email: usuario.email,
      rol: normalizarRol(usuario.rol)
    }))
    usuarios.value = lista

    const actual = lista.find(u =>
      u.email?.toLowerCase() === usuarioActual.value?.email?.toLowerCase()
    )

    if (actual) {
      usuarioActual.value = { ...usuarioActual.value, ...actual }
      localStorage.setItem('usuarioActual', JSON.stringify(usuarioActual.value))
    } else {
      usuarioActual.value = { nombre: 'Invitado', rol: 'usuario' }
    }
  } catch (err) {
    console.error('❌ Error al cargar usuarios:', err)
    alert('❌ No se pudieron cargar los usuarios')
  }
}

// 🗑 Modal confirmación
const borrarUsuario = (usuario) => {
  usuarioAEliminar.value = usuario
  modalConfirmacionRef.value?.abrir()
}

// ✅ 🔥 Confirmar eliminación con Firestore
const confirmarEliminacion = async () => {
  try {
    const id = usuarioAEliminar.value?.id
    if (!id) return

    // 🔥 Eliminar en Firestore
    await deleteDoc(doc(db, 'usuarios', id))

    // 👋 Quitar de la lista local
    usuarios.value = usuarios.value.filter(u => u.id !== id)

    notificacionRef.value?.mostrar('Usuario eliminado', `El usuario fue eliminado con éxito`, 'success')
  } catch (err) {
    console.error('❌ Error al borrar usuario:', err)
    notificacionRef.value?.mostrar('Error', 'No se pudo eliminar el usuario', 'error')
  }
}

const rolVisual = (rol) => {
  if (!rol) return 'Usuario'
  return rol.charAt(0).toUpperCase() + rol.slice(1)
}

const cambiarRolManual = async (usuario, nuevoRol) => {
  try {
    await axios.put(`http://localhost:5000/api/usuarios/${usuario.id}`, { rol: nuevoRol })
    const index = usuarios.value.findIndex(u => u.id === usuario.id)
    if (index !== -1) {
      usuarios.value[index].rol = normalizarRol(nuevoRol)
      usuarios.value = [...usuarios.value]

      if (usuario.id === usuarioActual.value?.id) {
        usuarioActual.value.rol = normalizarRol(nuevoRol)
        localStorage.setItem('usuarioActual', JSON.stringify(usuarioActual.value))
      }

      notificacionRef.value?.mostrar(
        'Rol actualizado',
        `${usuario.nombre} ahora es ${rolVisual(nuevoRol)}`,
        'success'
      )
    }
  } catch (err) {
    console.error('❌ Error al guardar el nuevo rol:', err)
    notificacionRef.value?.mostrar('Error', 'No se pudo actualizar el rol', 'error')
  }
}

const filtroBusqueda = ref('')
const filtroRol = ref('')

const usuariosFiltrados = computed(() =>
  usuarios.value.filter(usuario => {
    const coincideRol = !filtroRol.value || usuario.rol === filtroRol.value
    const coincideBusqueda =
      usuario.nombre.toLowerCase().includes(filtroBusqueda.value.toLowerCase()) ||
      usuario.email.toLowerCase().includes(filtroBusqueda.value.toLowerCase())
    return coincideRol && coincideBusqueda
  })
)

onMounted(async () => {
  cargarUsuarioDesdeStorage()

  spinnerRef.value?.mostrar()
  await cargarUsuariosYUsuarioActual()
  spinnerRef.value?.ocultar()
})

</script>



<style scoped>
.usuarios-container {
  padding: 2rem;
  background-color: #121212;
  color: #f5f5f5;
  min-height: 100vh;
}

.titulo {
  font-size: 2rem;
  color: #ffc107;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
}

.usuarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card-usuario {
  background-color: #1e1e1e;
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 0 10px rgba(255, 193, 7, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  transition: transform 0.2s ease;
}

.card-usuario:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 12px rgba(255, 193, 7, 0.3);
}


.info-principal h2 {
  font-size: 1.3rem;
  margin: 0;
}

.email {
  font-size: 0.9rem;
  color: #aaa;
  margin-top: 4px;
}

.rol {
  font-size: 0.85rem;
  font-weight: bold;
  margin-top: 8px;
  padding: 4px 10px;
  border-radius: 20px;
  display: inline-block;
  text-transform: capitalize;
}

.rol:hover {
  opacity: 0.9;
  transform: scale(1.05);
  transition: all 0.2s ease;
}


.rol.admin {
  background-color: #ffc10720;
  color: #ffc107;
}

.rol.moderador {
  background-color: #17a2b820;
  color: #17a2b8;
}

.rol.usuario {
  background-color: #28a74520;
  color: #28a745;
}

.acciones {
  display: flex;
  justify-content: flex-start;
  gap: 0.5rem;
}

.btn-icono {
  background: transparent;
  border: none;
  color: #f5f5f5;
  font-size: 1.3rem;
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}

.btn-icono:hover {
  color: #ffc107;
  transform: scale(1.1);
}

.cambio-rol {
  margin-top: auto;
}

.cambio-rol label {
  font-size: 0.85rem;
  margin-right: 0.5rem;
}

select {
  background-color: #2a2a2a;
  color: #fff;
  border: 1px solid #ffc107;
  border-radius: 6px;
  padding: 6px 10px;
}

.btn-icono i {
  transition: transform 0.2s ease;
}

.btn-icono:hover i {
  transform: scale(1.2);
  color: #ffc107;
}

.filtros-usuarios {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.filtros-usuarios input,
.filtros-usuarios select {
  background-color: #1e1e1e;
  color: #f5f5f5;
  border: 1px solid #ffc107;
  border-radius: 6px;
  padding: 0.5rem 1rem;
}

@media (max-width: 768px) {
  .usuarios-container {
    padding: 1rem;
  }

  .usuarios-grid {
    grid-template-columns: 1fr;
  }

  .card-usuario {
    padding: 1rem;
  }

  .filtros-usuarios {
    flex-direction: column;
    align-items: stretch;
    gap: 0.8rem;
  }

  .titulo {
    font-size: 1.5rem;
  }

  .info-principal h2 {
    font-size: 1.1rem;
  }

  .email {
    font-size: 0.85rem;
  }
}
</style>

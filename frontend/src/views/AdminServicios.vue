<template>
  <div class="admin-servicios container-fluid text-white py-5">
    <h1 class="mb-4 display-6 fw-bold text-center">Gestión de Servicios</h1>

    <!-- 🔍 Filtros arriba -->
    <div class="d-flex flex-column flex-md-row align-items-md-center gap-3 mb-4">
      <!-- 🔍 Buscador -->
      <div class="input-group buscador-custom">
        <span class="input-group-text"><i class="fa-solid fa-magnifying-glass text-warning"></i></span>
        <input type="text" v-model="busqueda" class="form-control bg-dark text-white border-warning"
          placeholder="Buscar por nombre, apellido o técnico..." />
      </div>

      <!-- 🔃 Filtro de orden -->
      <select v-model="orden" class="form-select bg-dark text-white border-warning" style="max-width: 200px;">
        <option value="recientes">Más recientes</option>
        <option value="viejos">Más viejos</option>
      </select>
    </div>
<div class="d-flex gap-2 mb-3">
  <button
    class="btn"
    :class="!mostrarTerminados ? 'btn-warning text-dark' : 'btn-outline-warning'"
    @click="mostrarTerminados = false"
  >
    Ver Pendientes
  </button>

  <button
    class="btn"
    :class="mostrarTerminados ? 'btn-warning text-dark' : 'btn-outline-warning'"
    @click="mostrarTerminados = true"
  >
    Ver Terminados
  </button>
</div>


    <!-- 🟡 FILA de columnas -->
    <div class="row gx-4">
      <!-- 📋 Columna izquierda -->
      <div class="col-md-4 serviciosPrendientes">
        <h5 class="mb-3">Servicios {{ mostrarArchivados ? 'Terminados' : 'Pendientes' }}</h5>
        <ul class="list-group">
          <li class="list-group-item list-group-item-dark text-white" v-for="servicio in serviciosFiltrados"
            :key="servicio.id" @click="seleccionarServicio(servicio)"
            :class="{ 'active': servicioSeleccionado?.id === servicio.id }" style="cursor: pointer;">
            <strong>{{ servicio.nombre }} {{ servicio.apellido }}</strong> - {{ servicio.tipoServicio }}
          </li>
        </ul>
      </div>

      <!-- 🧾 Columna derecha -->
      <div class="col-md-8 servicioSeleccionado">
        <div v-if="servicioSeleccionado">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold mb-0">Información del cliente</h4>

            <div class="d-flex gap-3">
              <button class="btn-editar" @click="abrirModalEditarServicio" :disabled="!servicioSeleccionado">
                <i class="fa-solid fa-pen-to-square me-2"></i>Editar
              </button>
              <button class="btn-eliminar" @click="eliminarServicio" :disabled="!servicioSeleccionado">
                <i class="fa-solid fa-trash me-2"></i>Eliminar
              </button>
            </div>
          </div>

          <div class="row gx-4">
            <div class="col-md-3"><label>Nombre</label><input type="text" v-model="servicioSeleccionado.nombre"
                disabled /></div>
            <div class="col-md-3"><label>Apellido</label><input type="text" v-model="servicioSeleccionado.apellido"
                disabled /></div>
            <div class="col-md-3"><label>DNI</label><input type="text" v-model="servicioSeleccionado.dni" disabled />
            </div>
            <div class="col-md-3"><label>Celular</label><input type="text" v-model="servicioSeleccionado.celular"
                disabled /></div>
            <div class="col-md-6"><label>E-Mail</label><input type="email" v-model="servicioSeleccionado.email"
                disabled /></div>
            <div class="col-md-6"><label>Técnico</label><input type="text" v-model="servicioSeleccionado.tecnico"
                disabled /></div>
            <div class="col-md-6"><label>Precio</label><input type="text" :value="precioFormateado" disabled /></div>
            <div class="col-12"><label>Descripción</label><textarea v-model="servicioSeleccionado.descripcion"
                disabled></textarea></div>

            <div class="pasos-container justify-content-center mt-3">
              <button v-for="(etapa, i) in etapas" :key="i" class="paso" :class="{
                ['paso-' + i]: true,
                'paso-activo': servicioSeleccionado.estado === i,
                'paso-completado': servicioSeleccionado.estado > i
              }" @click="actualizarEstado(i)">
                {{ etapa }}
              </button>
            </div>
          </div>
        </div>

        <!-- ❌ Nada seleccionado -->
        <div v-else class="d-flex align-items-center justify-content-center h-100">
          <p class="text-muted fs-5 text-center">Seleccioná un servicio para ver los detalles</p>
        </div>
      </div>
    </div>

    <!-- 📦 Modal agregar / editar -->
    <ModalAgregarServicio v-if="modalVisible" :visible="modalVisible"
      :servicioParaEditar="modoEdicion ? servicioParaEditar : null" @cerrar="modalVisible = false"
      @servicioAgregado="agregarServicio" @servicioEditado="actualizarServicio" />

    <!-- 🗑️ Modal confirmación -->
    <ModalConfirmacion ref="modalConfirmacionRef"
      :mensaje="`¿Querés eliminar el servicio de ${servicioSeleccionado?.nombre || 'este cliente'}?`"
      colorBoton="btn-danger" @confirmar="confirmarEliminacion" />
  </div>
</template>




<script setup>
import { ref, watch, onUnmounted, onMounted, computed } from 'vue'
import { collection, getDocs, deleteDoc, doc, updateDoc } from 'firebase/firestore'
import { db } from '../firebase'
import ModalAgregarServicio from '../components/Modals/ModalAgregarServicio.vue'
import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'

// 🔧 Refs
const listaServicios = ref([])
const servicioSeleccionado = ref(null)
const modalVisible = ref(false)
const modalConfirmacionRef = ref(null)
const modoEdicion = ref(false)
const servicioParaEditar = ref(null)
const busqueda = ref('')
const orden = ref('recientes')
const mostrarTerminados = ref(false)

// 🔁 Controla el scroll cuando el modal está abierto
watch(modalVisible, (nuevoValor) => {
  document.body.style.overflow = nuevoValor ? 'hidden' : 'auto'
})

// 🟨 Etapas del servicio
const etapas = [
  "Ingresado",
  "En Revisión",
  "Casi Terminado",
  "Listo para Retirar"
]

// 📥 Cargar servicios desde Firebase
const obtenerServicios = async () => {
  try {
    const querySnapshot = await getDocs(collection(db, 'servicios'))
    const servicios = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }))

    listaServicios.value = servicios.sort((a, b) => {
      const fechaA = a.fechaCreacion?.toMillis?.() || 0
      const fechaB = b.fechaCreacion?.toMillis?.() || 0
      return fechaB - fechaA
    })
  } catch (error) {
    console.error('Error al obtener servicios:', error)
  }
}

// 🚀 Cargar al iniciar
onMounted(() => {
  obtenerServicios()
})

// ➕ Mostrar modal para agregar
const abrirModalAgregarServicio = () => {
  modalVisible.value = true
}

// ✅ Seleccionar un servicio
const seleccionarServicio = (servicio) => {
  servicioSeleccionado.value = servicio
}

// ➕ Agregar nuevo servicio (local, sin persistencia)
const agregarServicio = (nuevoServicio) => {
  listaServicios.value.push(nuevoServicio)
}

// 🔄 Actualizar lista y selección
const actualizarServicio = async (servicioActualizado) => {
  await obtenerServicios()
  servicioSeleccionado.value = servicioActualizado
}

// 🟡 Cambiar estado
const actualizarEstado = async (nuevoEstado) => {
  if (!servicioSeleccionado.value) return

  servicioSeleccionado.value.estado = nuevoEstado

  try {
    const docRef = doc(db, 'servicios', servicioSeleccionado.value.id)
    await updateDoc(docRef, { estado: nuevoEstado })

    if (nuevoEstado === etapas.length - 1) {
      await obtenerServicios()
      servicioSeleccionado.value = null
      return
    }
  } catch (error) {
    console.error('Error al actualizar estado:', error)
  }

  const numero = servicioSeleccionado.value.celular.replace(/\D/g, '')
  const numeroWhatsApp = `549${numero}`

  const mensajes = [
    `¡Hola ${servicioSeleccionado.value.nombre}! Tu servicio fue ingresado correctamente. Pronto lo revisaremos.`,
    `Hola ${servicioSeleccionado.value.nombre}, ya estamos revisando tu producto.`,
    `¡Buenas! Tu servicio está casi listo para entregar.`,
    `¡Perfecto ${servicioSeleccionado.value.nombre}! Tu servicio ya está listo para retirar.`
  ]

  const mensaje = encodeURIComponent(mensajes[nuevoEstado])
  const link = `https://wa.me/${numeroWhatsApp}?text=${mensaje}`
  window.open(link, '_blank')
}

// ❌ Eliminar con confirmación
const eliminarServicio = () => {
  if (!servicioSeleccionado.value) return
  modalConfirmacionRef.value?.abrir()
}

const confirmarEliminacion = async () => {
  try {
    await deleteDoc(doc(db, 'servicios', servicioSeleccionado.value.id))
    listaServicios.value = listaServicios.value.filter(s => s.id !== servicioSeleccionado.value.id)
    servicioSeleccionado.value = null
  } catch (error) {
    console.error('Error al eliminar el servicio:', error)
  }
}

// ✏️ Editar
const abrirModalEditarServicio = () => {
  if (!servicioSeleccionado.value) return
  modoEdicion.value = true
  servicioParaEditar.value = { ...servicioSeleccionado.value }
  modalVisible.value = true
}

// 💰 Precio formateado ARS
const precioFormateado = computed(() => {
  if (!servicioSeleccionado.value?.precio) return ''
  return `$ ${Number(servicioSeleccionado.value.precio).toLocaleString('es-AR')}`
})

// 🧼 Restaurar scroll
onUnmounted(() => {
  document.body.style.overflow = 'auto'
})

// 🔍 Filtro de servicios dinámico
const serviciosFiltrados = computed(() => {
  let filtrados = listaServicios.value.filter(s =>
    mostrarTerminados.value
      ? s.estado === etapas.length - 1
      : s.estado !== etapas.length - 1
  )

  if (busqueda.value.trim() !== '') {
    const search = busqueda.value.toLowerCase()
    filtrados = filtrados.filter(s =>
      s.nombre?.toLowerCase().includes(search) ||
      s.apellido?.toLowerCase().includes(search) ||
      s.tecnico?.toLowerCase().includes(search)
    )
  }

  if (orden.value === 'viejos') {
    filtrados.sort((a, b) => {
      const fechaA = a.fechaCreacion?.toMillis?.() || 0
      const fechaB = b.fechaCreacion?.toMillis?.() || 0
      return fechaA - fechaB
    })
  } else {
    filtrados.sort((a, b) => {
      const fechaA = a.fechaCreacion?.toMillis?.() || 0
      const fechaB = b.fechaCreacion?.toMillis?.() || 0
      return fechaB - fechaA
    })
  }

  return filtrados
})
</script>





<style scoped>
.admin-servicios {
  background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
  min-height: 100vh;
  padding-bottom: 4rem;
  font-family: 'Montserrat', sans-serif;
}

/* TITULOS Y LABELS */
h1 {
  color: #ffc107;
  font-size: 2.2rem;
  letter-spacing: 1px;
  text-align: center;
  font-weight: 700;
  margin-bottom: 2rem;
}

h4,
h5,
label {
  color: #ffc107;
}

h5 {
  font-size: 1.2rem;
  font-weight: 600;
}

label {
  margin-bottom: 6px;
  display: block;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #f1f1f1;
}

/* INPUTS & TEXTAREA */
input,
textarea {
  background-color: #0d0d0d;
  color: #f1f1f1;
  border: 1px solid #ffc107;
  border-radius: 20px;
  padding: 10px 15px;
  width: 100%;
  font-weight: bold;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

input[type="email"] {
  color: #ffd54f;
}

input:focus,
textarea:focus {
  outline: none;
  color: #ffffff;
  border-color: #ffc107;
  box-shadow: 0 0 8px rgba(255, 193, 7, 0.3);
  background-color: #121212;
}

textarea {
  min-height: 100px;
  resize: none;
}

/* BOTONES */
.btn-guardar,
.btn-cancelar {
  padding: 10px 25px;
  border-radius: 20px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-guardar {
  background-color: transparent;
  color: #ffc107;
  border: 2px solid #ffc107;
}

.btn-guardar:hover {
  background-color: #ffc107;
  color: #000;
}

.btn-cancelar {
  background-color: transparent;
  color: #f1f1f1;
  border: 2px solid #dc3545;
}

.btn-cancelar:hover {
  background-color: #dc3545;
  color: #fff;
}

/* PASOS */
.pasos-container {
  display: flex;
  gap: 10px;
  margin-top: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.paso {
  padding: 10px 18px;
  border-radius: 25px;
  font-weight: bold;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.paso-0 {
  background-color: #ffc107;
  color: #000;
}

.paso-1 {
  background-color: #1e1e1e;
  color: #ffc107;
  border-color: #ffc107;
}

.paso-2 {
  background-color: #000;
  color: #ffc107;
}

.paso-3 {
  background-color: #555;
  color: #fff;
}

/* LISTA DE SERVICIOS */
.list-group-item {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  border-radius: 12px !important;
  margin-bottom: 10px;
  font-size: 0.9rem;

}

.list-group-item:hover {
  background-color: rgba(255, 193, 7, 0.2);
  transform: scale(1.01);
}

.list-group-item.active {
  background-color: #ffc107;
  border-color: #ffc107;
  color: #000;
  font-weight: bold;
}

.list-group-item strong {
  font-weight: 600;
}

/* COLUMNA IZQ Y DER */
.col-md-4,
.col-md-8 {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  border: 1px solid #ffc107;
}

/* CAMPOS DESHABILITADOS */
.servicioSeleccionado input[disabled],
.servicioSeleccionado textarea[disabled] {
  opacity: 0.85;
  cursor: not-allowed;
}

/* ESPACIO CUSTOM (opcional) */
.row-gap-custom {
  gap: 1rem;
}

.gap-x-4>.col-md-4,
.gap-x-4>.col-md-8 {
  margin-right: 1rem;
}

.gap-x-4>.col-md-8 {
  margin-left: 1rem;
}

.servicioSeleccionado {
  margin-right: px;
}

/* Espaciado entre campos */
.row.gx-4>.col-md-3,
.row.gx-4>.col-md-6,
.row.gx-4>.col-12 {
  margin-bottom: 1rem;
}

/* Más espacio entre descripción y botones */
textarea {
  margin-bottom: 1.5rem;
}

/* Botones alineados con espacio */
.col-12.d-flex.gap-3.justify-content-center {
  gap: 1.5rem;
  margin-bottom: 1rem;
}

/* Botones de estado separados y con espacio arriba */
.pasos-container {
  margin-top: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-eliminar {
  background-color: transparent;
  color: #ff4c4c;
  border: 2px solid #ff4c4c;
  padding: 10px 25px;
  border-radius: 20px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-eliminar:hover {
  background-color: #ff4c4c;
  color: #fff;
}

.btn-eliminar:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-editar {
  background-color: transparent;
  color: #ffc107;
  border: 2px solid #ffc107;
  padding: 10px 25px;
  border-radius: 20px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-editar:hover {
  background-color: #ffc107;
  color: #000;
}

.btn-editar:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.paso-activo {
  background-color: #ffc107 !important;
  color: #000 !important;
}

.paso-completado {
  background-color: #28a745 !important;
  color: #fff !important;
  border-color: #28a745 !important;
}



/* Responsive tweek */
@media (max-width: 768px) {

  .row.gx-4>.col-md-3,
  .row.gx-4>.col-md-6 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .serviciosPrendientes {
    margin-right: 16px;
  }

  .col-md-4,
  .col-md-8 {
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.8rem;
  }
}
</style>

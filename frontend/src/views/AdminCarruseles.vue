<template>
  <div class="admin-carruseles container-fluid py-5 text-white">
    <h1 class="titulo-principal text-center">
      <i class="fas fa-film me-2 text-white"></i>
      Gestión de Carruseles
    </h1>

    <div class="acciones-carrusel text-center mb-5">
      <p class="explicacion mb-3">
        Creá un nuevo carrusel para destacar productos en tu página principal.
        Seleccioná un nombre y los productos que quieras mostrar
      </p>

      <button class="btn btn-warning" @click="abrirModalNuevoCarrusel">
        <i class="fas fa-plus me-2"></i>Nuevo carrusel
      </button>

      <hr class="separador mt-5" />
    </div>

    <div v-if="carruseles.length === 0">No hay carruseles creados aún.</div>

    <draggable v-model="carruseles" item-key="id" class="row g-4" handle=".handle" @end="guardarNuevoOrden">
      <template #item="{ element: carrusel }">
        <div class="carrusel-preview mb-5">
          <div class="encabezado-carrusel d-flex justify-content-between align-items-center mb-3 px-2 px-md-4">
            <h2 class="nombre-carrusel">
              <i class="fas fa-grip-vertical me-2 handle" title="Arrastrar para reordenar"></i>
              {{ carrusel.nombre }}
            </h2>
            <span class="badge bg-secondary px-3 py-2">{{ carrusel.productos?.length || 0 }} productos</span>
          </div>

          <!-- 🔁 Flechas FUERA del Swiper -->
          <div class="swiper-con-flechas position-relative">
            <Swiper :modules="[Navigation]" :navigation="{
              nextEl: `.next-${carrusel.id}`,
              prevEl: `.prev-${carrusel.id}`
            }" class="swiper-wrapper-custom" :slides-per-view="'auto'" :space-between="16">
              <swiper-slide v-for="producto in filtrarProductosPorID(carrusel.productos)" :key="producto.id"
                class="slide-card">
                <div class="card-preview text-white">
                  <img :src="producto.imagen" class="imagen-preview" :alt="producto.nombre" />
                  <p class="nombre-preview mt-2" :title="producto.nombre">{{ producto.nombre }}</p>
                </div>
              </swiper-slide>
            </Swiper>

            <!-- Flechas únicas por carrusel con POSICIÓN -->
            <div :class="`flecha-custom boton-prev prev-${carrusel.id}`">
              <i class="fas fa-chevron-left"></i>
            </div>
            <div :class="`flecha-custom boton-next next-${carrusel.id}`">
              <i class="fas fa-chevron-right"></i>
            </div>

          </div>

          <div class="text-end mt-3 px-2 px-md-4 d-flex justify-content-between align-items-center">
            <div>
              <button class="btn btn-outline-light btn-sm me-2" @click="moverCarrusel(carrusel.id, -1)">
                <i class="fas fa-arrow-up"></i>
              </button>
              <button class="btn btn-outline-light btn-sm" @click="moverCarrusel(carrusel.id, 1)">
                <i class="fas fa-arrow-down"></i>
              </button>
            </div>

            <div>
              <button class="btn btn-outline-primary me-2" @click="abrirModalOrden(carrusel)">
                <i class="fas fa-arrows-alt me-1 text-white"></i> Reordenar
              </button>

              <button class="btn btn-outline-info me-2" @click="editarCarrusel(carrusel)">
                <i class="fas fa-pen me-1 text-white"></i> Editar
              </button>

              <button class="btn btn-outline-danger" @click="confirmarEliminacion(carrusel)">
                <i class="fas fa-trash-alt me-1 text-white"></i> Eliminar
              </button>

            </div>
          </div>
        </div>
      </template>
    </draggable>

    <div class="estado-vacio text-center my-5" v-if="carruseles.length === 0">
      <i class="fas fa-box-open fa-2x mb-3 text-secondary"></i>
      <p class="text-white-50">Aún no creaste carruseles. Usá el botón para comenzar a destacar tus productos.</p>
      <button class="btn btn-warning mt-3" @click="abrirModalNuevoCarrusel">
        <i class="fas fa-plus me-2"></i> Crear primer carrusel
      </button>
    </div>

  </div>

  <ModalCarrusel v-if="mostrarModal" :carrusel="carruselSeleccionado" @cerrar="cerrarModal"
    @guardar="guardarCarrusel" />

  <ModalConfirmacion ref="modalConfirmacion" :mensaje="mensajeModal" :colorBoton="'btn-danger'"
    @confirmar="eliminarCarruselConfirmado" />

  <SpinnerCarga ref="spinner" mensaje="Procesando cambios..." />

  <ToastNotificacion ref="toast" />

  <ModalOrdenarCarrusel v-if="mostrarModalOrden" :key="carruselSeleccionado?.id" ref="modalOrdenRef"
    :carrusel="carruselSeleccionado" :productos="productos" @guardar-orden="actualizarOrdenProductos" />


</template>

<script setup>
// 📦 Core de Vue
import { ref, onMounted, nextTick } from 'vue'

// 🔥 Firestore
import { collection, getDocs, addDoc, updateDoc, doc, deleteDoc } from 'firebase/firestore'
import { db } from '../firebase'
import draggable from 'vuedraggable'


// 🧩 Componentes
import ModalCarrusel from '../components/Carruseles/ModalCarrusel.vue'
import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'
import ModalOrdenarCarrusel from '../components/Modals/ModalOrdenProductos.vue'
import ToastNotificacion from '../components/ToastNotificacion.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'

// 🌀 Swiper
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'


// 🔁 Refs
const carruseles = ref([])
const productos = ref([])
const mostrarModal = ref(false)
const mostrarModalOrden = ref(false)
const carruselSeleccionado = ref(null)
const modalConfirmacion = ref(null)
const mensajeModal = ref('')
const carruselAEliminar = ref(null)
const toast = ref(null)
const spinner = ref(null)
const mensajeSpinner = ref('Cargando...')
const modalOrdenRef = ref(null)


// 📦 Carga inicial
onMounted(async () => {
  spinner.value?.mostrar()
  await cargarProductos()
  await cargarCarruseles()
  spinner.value?.ocultar()
})

// 🚚 Productos
const cargarProductos = async () => {
  const snapshot = await getDocs(collection(db, 'productos'))
  productos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
}

// 🧱 Carruseles
const cargarCarruseles = async () => {
  const snapshot = await getDocs(collection(db, 'carruselesHome'))
  const docsConOrden = snapshot.docs.map((doc, index) => {
    const data = doc.data()
    console.log(`🔥 Carrusel "${data.nombre}" → productos:`, data.productos)
    return {
      id: doc.id,
      ...data,
      orden: data.orden ?? index
    }
  })

  carruseles.value = docsConOrden.sort((a, b) => a.orden - b.orden)
}

// ➕ Nuevo carrusel
const abrirModalNuevoCarrusel = () => {
  carruselSeleccionado.value = null
  mostrarModal.value = true
}

// ✏️ Editar carrusel
const editarCarrusel = (carrusel) => {
  carruselSeleccionado.value = carrusel
  mostrarModal.value = true
}

// ✅ Guardar carrusel
const guardarCarrusel = async (carrusel, esNuevo = false) => {
  spinner.value?.mostrar()
  try {
    if (carruselSeleccionado.value) {
      // 🛠 EDITAR
      await updateDoc(doc(db, 'carruselesHome', carruselSeleccionado.value.id), carrusel)
      toast.value?.mostrar('Carrusel actualizado', `"${carrusel.nombre}" se actualizó con éxito`, 'success')
    } else {
      // ✨ NUEVO
      const nuevoDoc = await addDoc(collection(db, 'carruselesHome'), {
        ...carrusel,
        orden: carruseles.value.length
      })
      toast.value?.mostrar('Carrusel creado', `"${carrusel.nombre}" se creó con éxito`, 'success')

      // 👉 Abrí modal de orden solo si es nuevo
      if (esNuevo) {
        const nuevoCarrusel = { id: nuevoDoc.id, ...carrusel, orden: carruseles.value.length }
        abrirModalOrden(nuevoCarrusel)
      }
    }

    await cargarCarruseles()
  } catch (e) {
    toast.value?.mostrar('Error', 'Ocurrió un error al guardar', 'error')
  } finally {
    spinner.value?.ocultar()
    mostrarModal.value = false
  }
}


// ❌ Eliminar carrusel
const confirmarEliminacion = (carrusel) => {
  carruselAEliminar.value = carrusel
  mensajeModal.value = `¿Querés eliminar el carrusel "${carrusel.nombre}"?`
  modalConfirmacion.value?.abrir()
}

const eliminarCarruselConfirmado = async () => {
  spinner.value?.mostrar()
  try {
    await deleteDoc(doc(db, 'carruselesHome', carruselAEliminar.value.id))
    await cargarCarruseles()
    toast.value?.mostrar('Carrusel eliminado', `"${carruselAEliminar.value.nombre}" fue eliminado`, 'success')
  } catch (err) {
    toast.value?.mostrar('Error al eliminar', 'No se pudo eliminar el carrusel', 'error')
  } finally {
    spinner.value?.ocultar()
  }
}

// 🔃 Mover carrusel
const moverCarrusel = async (id, direccion) => {
  const indexActual = carruseles.value.findIndex(c => c.id === id)
  const indexDestino = indexActual + direccion
  if (indexDestino < 0 || indexDestino >= carruseles.value.length) return

  const temp = carruseles.value[indexActual]
  carruseles.value[indexActual] = carruseles.value[indexDestino]
  carruseles.value[indexDestino] = temp

  const carruselA = carruseles.value[indexActual]
  const carruselB = carruseles.value[indexDestino]

  await Promise.all([
    updateDoc(doc(db, 'carruselesHome', carruselA.id), { orden: indexActual }),
    updateDoc(doc(db, 'carruselesHome', carruselB.id), { orden: indexDestino })
  ])
  await cargarCarruseles()
}

// 🧲 Drag & drop (orden global)
const guardarNuevoOrden = async () => {
  try {
    spinner.value?.mostrar()

    const updates = carruseles.value.map((carrusel, index) =>
      updateDoc(doc(db, 'carruselesHome', carrusel.id), { orden: index })
    )

    await Promise.all(updates)
    await cargarCarruseles()

    toast.value?.mostrar('✅ Orden actualizado', 'Nuevo orden guardado correctamente.', 'success')
  } catch (err) {
    toast.value?.mostrar('❌ Error', 'No se pudo guardar el nuevo orden.', 'error')
    console.error(err)
  } finally {
    spinner.value?.ocultar()
  }
}

// 🧠 Guardar nuevo orden de productos en un carrusel
const actualizarOrdenProductos = async (nuevoCarrusel) => {
  console.log('📥 Guardando en Firestore el nuevo orden:', nuevoCarrusel.productos)

  try {
    await updateDoc(doc(db, 'carruselesHome', nuevoCarrusel.id), {
      productos: nuevoCarrusel.productos
    })

    const index = carruseles.value.findIndex(c => c.id === nuevoCarrusel.id)
    if (index !== -1) {
      carruseles.value[index].productos = [...nuevoCarrusel.productos]
      carruseles.value = [...carruseles.value] // Forzar reactividad
      console.log('🎯 Carrusel actualizado:', carruseles.value[index])
    }

    toast.value?.mostrar('✅ Orden actualizado', 'El orden de los productos fue guardado.', 'success')
  } catch (error) {
    toast.value?.mostrar('❌ Error', 'No se pudo guardar el orden en Firestore.', 'error')
    console.error('⛔ Error al guardar el orden de productos:', error)
  }

  console.log('📦 Recibido para actualizar orden:', nuevoCarrusel)
}

// 🪟 Abrir modal de ordenamiento
const abrirModalOrden = (carrusel) => {
  carruselSeleccionado.value = { ...carrusel } // nueva referencia
  mostrarModalOrden.value = false
  nextTick(() => {
    mostrarModalOrden.value = true
  })
}

// 🔍 Filtrar productos por ID
const filtrarProductosPorID = (ids) => {
  if (!Array.isArray(ids)) return []

  const mapa = new Map(productos.value.map(p => [p.id, p]))
  return ids.map(id => mapa.get(id)).filter(Boolean)
}

</script>

<style scoped>
.admin-carruseles {
  background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
  min-height: 100vh;
  padding: 3rem 2rem;
  width: 100%;
  overflow-x: hidden;
}

/* Título principal */
.titulo-principal {
  font-size: 2.8rem;
  font-weight: 800;
  color: var(--colorTerciario);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
}

/* Botón de crear carrusel */
.btn-warning {
  font-weight: 600;
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
  transition: all 0.2s ease;
}

.btn-warning:hover {
  background-color: #eab308;
  color: #000;
}

/* Explicación */
.acciones-carrusel .explicacion {
  color: #d1d5db;
  font-size: 1.05rem;
  max-width: 600px;
  margin: 0 auto;
}

/* Separador */
.separador {
  border: none;
  height: 2px;
  background: rgb(173, 173, 173);
  max-width: 500px;
  margin: 2rem auto;
  border-radius: 10px;
}

/* Cards carrusel */
.card-carrusel {
  background-color: #181818;
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
  width: 100%;
  max-width: 100%;
  margin-bottom: 3rem;
}

.btn i {
  color: white !important;
}


.card-carrusel:hover {
  transform: translateY(-6px);
}

/* Carrusel completo */
.carrusel-preview {
  background-color: #181818;
  border-radius: 20px;
  padding: 2rem 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  width: 100%;
}

.encabezado-carrusel {
  flex-wrap: wrap;
}

.nombre-carrusel {
  color: var(--colorTerciario);
  font-size: 1.5rem;
  font-weight: 700;
}

.badge {
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 10px;
}

/* Card individual */
.slide-card {
  width: 200px !important;
}

.card-preview {
  background-color: #111;
  border-radius: 16px;
  padding: 1rem;
  text-align: center;
  height: 260px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s;
}

.card-preview:hover {
  transform: translateY(-4px);
}

/* Imagen de producto */
.imagen-preview {
  width: 100%;
  height: 160px;
  object-fit: contain;
  border-radius: 10px;
  background-color: #1f1f1f;
  padding: 0.5rem;
}

/* Nombre del producto */
.nombre-preview {
  font-size: 0.9rem;
  font-weight: 500;
  color: #f3f4f6;
  text-align: center;
  line-height: 1.3;
  height: 2.6em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Swiper general */
.swiper-preview-admin {
  padding: 0 1rem;
}

.vista-previa-swiper .swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
}

/* Flechas < > */
.swiper-con-flechas {
  position: relative;
  padding: 0 2rem;
}


/* Flechas */
.flecha-custom {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  background-color: rgba(255, 255, 255, 0.08);
  border: 2px solid var(--colorTerciario);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--colorTerciario);
  font-size: 1rem;
  z-index: 10;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
  pointer-events: none;
}

.swiper-con-flechas:hover .flecha-custom {
  opacity: 1;
  pointer-events: auto;
}

.boton-prev {
  left: 0px;
}

.boton-next {
  right: 0px;
}

.flecha-custom:hover {
  background-color: var(--colorTerciario);
  color: #000;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 0 10px var(--colorTerciario);
}
</style>

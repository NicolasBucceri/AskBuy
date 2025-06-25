<template>
  <div class="modal-overlay">
    <div class="modal-contenido bg-dark text-white rounded-4 shadow-lg">

      <div class="row g-4 p-4">
        <!-- 🧱 Columna izquierda: Info carrusel + preview -->
        <div class="col-md-7 d-flex flex-column justify-content-between">
          <div class="box-info-carrusel">
            <h3 class="titulo-seccion mb-4">
              <i class="fas fa-sliders-h me-2"></i>
              {{ carrusel ? 'Editar carrusel' : 'Nuevo carrusel' }}
            </h3>

            <!-- 🏷 Nombre -->
            <div class="mb-4">
              <label class="form-label">Nombre del carrusel</label>
              <input type="text" ref="inputNombre" v-model="nombre" class="form-control"
                placeholder="Ej: Ofertas" />

            </div>

            <!-- 🖼 Vista previa productos seleccionados -->
            <div class="box-vista-previa">
              <h5 class="subtitulo-seccion mb-3"><i class="fas fa-eye me-1"></i>Vista previa</h5>
              <div class="vista-previa-scroll d-flex flex-wrap gap-3">
                <div v-for="prod in productos.filter(p => productosSeleccionados.includes(p.id))" :key="prod.id"
                  class="vista-previa-item">
                  <img :src="prod.imagen" :alt="prod.nombre" />
                </div>
              </div>
            </div>
          </div>
        </div>


        <!-- 📦 Columna derecha: Selector de productos -->
        <div class="col-md-5 d-flex flex-column" style="max-height: calc(99vh - 100px);">
          <div class="contenedor-selector-productos flex-grow-1">
            <SelectorProductos :productos="productos" :seleccionados="productosSeleccionados"
              @actualizar="productosSeleccionados = $event" />

          </div>
        </div>

        <!-- 🔘 Botones abajo -->
        <div class="col-12 d-flex justify-content-end gap-2 mt-3">
          <button class="btn btn-outline-light" @click="$emit('cerrar')">Cancelar</button>
          <button class="btn btn-success" :disabled="!puedeGuardar" @click="guardarCarrusel">
            Guardar carrusel
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, onUpdated, nextTick } from 'vue'
import SelectorProductos from './SelectorProductos.vue'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../../firebase'

// Props
const props = defineProps({
  carrusel: Object // null si es nuevo
})

// Emit
const emit = defineEmits(['cerrar', 'guardar'])

// Estado local
const nombre = ref('')
const productos = ref([])
const productosSeleccionados = ref([])
const inputNombre = ref(null)

// Cargar productos y precargar si es edición
onMounted(async () => {
  const snap = await getDocs(collection(db, 'productos'))
  productos.value = snap.docs.map(d => ({ id: d.id, ...d.data() }))

  if (props.carrusel) {
    nombre.value = props.carrusel.nombre
    productosSeleccionados.value = [...props.carrusel.productos]
  }
})

onUnmounted(() => {
  document.body.classList.remove('modal-bloqueo-scroll')
  nombre.value = ''
  productosSeleccionados.value = []
})


onUnmounted(() => {
  document.body.classList.remove('modal-bloqueo-scroll')
})

onUpdated(() => {
  nextTick(() => {
    if (inputNombre.value) {
      inputNombre.value.focus()
      inputNombre.value.setSelectionRange(nombre.value.length, nombre.value.length)
    }
  })
})


// Guardar
const guardarCarrusel = () => {
  const nuevo = {
    nombre: nombre.value.trim(),
    productos: productosSeleccionados.value
  }
  const esNuevo = !props.carrusel
  emit('guardar', nuevo, esNuevo)
}


// Validación
const puedeGuardar = computed(() =>
  nombre.value.trim() !== '' && productosSeleccionados.value.length > 0
)
</script>

<style scoped>
body.modal-bloqueo-scroll {
  overflow: hidden !important;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-contenido {
  width: 95vw;
  height: auto;
  max-height: 95vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-contenido {
  z-index: 10000;
  position: relative;
}

input.form-control {
  z-index: 1;
  position: relative;
}


.vista-previa-item {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  background-color: #111;
  overflow: hidden;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}

.vista-previa-item img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.contenedor-selector-productos {
  height: 100%;
  overflow-y: auto;
  padding-right: 4px;
  scrollbar-width: thin;
  scrollbar-color: var(--colorTerciario) #2a2a2a;
}

.contenedor-selector-productos::-webkit-scrollbar {
  width: 6px;
}

.contenedor-selector-productos::-webkit-scrollbar-thumb {
  background-color: var(--colorTerciario);
  border-radius: 10px;
}

.vista-previa-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

.vista-previa-item {
  width: 110px;
  height: 110px;
  border-radius: 16px;
  background-color: #ffffff;
  border: 1px solid #ffffff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.vista-previa-item:hover {
  transform: scale(1.03);
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.08);
}


.vista-previa-item img {
  width: 85%;
  height: 85%;
  object-fit: contain;
  border-radius: 12px;
  transition: transform 0.2s ease;
}

.vista-previa-item:hover img {
  transform: scale(1.03);
}
</style>

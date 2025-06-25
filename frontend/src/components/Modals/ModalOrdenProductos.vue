<template>
    <div class="modal fade" id="modalOrdenProductos" tabindex="-1" aria-hidden="true" ref="modalRef">
        <div class="modal-dialog modal-xl">
            <div class="modal-content bg-dark text-white rounded-4 shadow-lg">
                <div class="modal-header border-0">
                    <h5 class="modal-title">
                        🌪️ Reordenar productos - <strong>{{ carruselSeleccionado?.nombre }}</strong>
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <Draggable v-model="productosOrdenados" item-key="id" class="lista-productos" handle=".drag-handle">
                        <template #item="{ element }">
                            <div
                                class="producto-item d-flex align-items-center justify-content-between p-3 mb-2 bg-black rounded-3">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-grip-vertical me-3 drag-handle text-secondary"></i>
                                    <img :src="element.imagen" alt="img" class="img-preview me-3" />
                                    <span class="nombre-producto">{{ element.nombre }}</span>
                                </div>
                            </div>
                        </template>
                    </Draggable>
                </div>

                <div class="modal-footer border-0">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="fas fa-times me-1"></i> Cancelar
                    </button>
                    <button class="btn btn-warning" @click="guardarOrden">
                        <i class="fas fa-save me-1"></i> Guardar orden
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { Modal } from 'bootstrap'
import Draggable from 'vuedraggable'

// Props del modal
const props = defineProps({
  carrusel: Object,
  productos: Array
})

const emit = defineEmits(['guardar-orden'])

// Refs internas
const modalRef = ref(null)
let modalInstance = null

const productosOrdenados = ref([])
const carruselSeleccionado = ref(null)

// Watch para mostrar el modal y cargar productos ordenados
watch(
  () => props.carrusel?.productos,
  () => {
    if (props.carrusel) {
      carruselSeleccionado.value = props.carrusel

      productosOrdenados.value = props.carrusel.productos.map(p =>
        typeof p === 'string' ? props.productos.find(prod => prod.id === p) : p
      ).filter(Boolean)

      nextTick(() => {
        if (!modalInstance) modalInstance = new Modal(modalRef.value)
        modalInstance.show()
      })
    }
  },
  { immediate: true }
)


// Emitir orden actualizado
const guardarOrden = () => {
  const productosSoloIDs = productosOrdenados.value.map(p => p.id)

  console.log('🧠 Orden guardado desde el modal:', productosSoloIDs)

  emit('guardar-orden', {
    id: carruselSeleccionado.value.id,
    productos: productosSoloIDs
  })

  modalInstance?.hide()
}
</script>

<style scoped>
.lista-productos {
    max-height: 500px;
    overflow-y: auto;
}

.img-preview {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 10px;
}

.nombre-producto {
    font-weight: 500;
    font-size: 1.1rem;
}

.drag-handle {
    cursor: grab;
}
</style>

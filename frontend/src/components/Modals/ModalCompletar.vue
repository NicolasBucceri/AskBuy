<template>
  <div class="modal fade" ref="modalRef" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content bg-dark text-white">
        <div class="modal-header border-bottom border-secondary">
          <h5 class="modal-title">
            <i class="fas fa-pencil-alt me-2"></i> Completar Producto
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Nombre</label>
              <input v-model="local.nombre" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Marca</label>
              <input v-model="local.marca" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Color</label>
              <input v-model="local.color" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Etiqueta</label>
              <input v-model="local.etiqueta" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Descripción</label>
              <textarea v-model="local.descripcion" rows="3" class="form-control"></textarea>
            </div>
            <div class="col-12">
              <label class="form-label">Imagen (URL)</label>
              <input v-model="local.imagen" class="form-control" />
              <small class="text-white-50">Dejá vacío para mantener la imagen actual.</small>
            </div>

            <!-- Vista previa de imagen -->
            <div class="col-12 text-center" v-if="local.imagen">
              <img :src="local.imagen" alt="Vista previa" class="img-fluid rounded mt-2" style="max-height: 200px;" />
            </div>
          </div>
        </div>

        <div class="modal-footer border-top border-secondary">
          <button class="btn btn-outline-light" data-bs-dismiss="modal">
            Cancelar
          </button>
          <button class="btn btn-warning" @click="guardar">
            <i class="fas fa-save me-2"></i> Guardar Cambios
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive, nextTick, watch } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  producto: Object
})

const emit = defineEmits(['guardado'])

const modalRef = ref(null)
let modalInstance = null

const local = reactive({
  nombre: '',
  marca: '',
  color: '',
  descripcion: '',
  etiqueta: '',
  imagen: ''
})

// 🔁 Sincroniza datos del producto al abrir el modal
watch(() => props.producto, (nuevo) => {
  if (nuevo) {
    Object.assign(local, {
      nombre: nuevo.nombre || '',
      marca: nuevo.marca || '',
      color: nuevo.color || '',
      descripcion: nuevo.descripcion || '',
      etiqueta: nuevo.etiqueta || '',
      imagen: nuevo.imagen !== '/Img/imagenNoDisponible.jpg' ? nuevo.imagen : ''
    })
  }
})

// 📤 Abre el modal
const abrir = async () => {
  await nextTick()
  modalInstance = new Modal(modalRef.value)
  modalInstance.show()
}

// 💾 Guarda cambios y actualiza el producto
const guardar = () => {
  const estaCompleto = local.nombre && local.marca && local.color && local.descripcion && local.etiqueta

  if (!estaCompleto) {
    alert('⚠️ Faltan completar todos los campos obligatorios.')
    return
  }

  Object.assign(props.producto, {
    ...local,
    completado: true,
    oculto: false,
    imagen: local.imagen || ''
  })

  emit('guardado', props.producto)
  modalInstance?.hide()
}

// 👇 Esta línea es CLAVE para que el padre pueda hacer modalCompletar.value.abrir()
defineExpose({ abrir })
</script>



<style scoped>
.modal-content {
  border-radius: 12px;
}
</style>

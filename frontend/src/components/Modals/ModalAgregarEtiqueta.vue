<template>
  <div
    class="modal fade"
    id="modalAgregarEtiqueta"
    tabindex="-1"
    aria-labelledby="modalEtiquetaLabel"
    aria-hidden="true"
    ref="modalRef"
  >
    <div class="modal-dialog">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title" id="modalEtiquetaLabel">Agregar Nueva Etiqueta</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>

        <div class="modal-body">
          <label for="nuevaEtiqueta">Nombre de la Etiqueta:</label>
          <input
            type="text"
            v-model="nuevaEtiqueta"
            id="nuevaEtiqueta"
            class="form-control"
            placeholder="Ejemplo: Gaming"
          />
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
          <button type="button" class="btn btn-primary" @click="emitirEtiqueta">Agregar</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const nuevaEtiqueta = ref('')
const modalRef = ref(null)
let modalInstance = null

const emit = defineEmits(['agregar-etiqueta', 'toast'])

onMounted(() => {
  if (modalRef.value) {
    modalInstance = new bootstrap.Modal(modalRef.value)
  }
})

async function emitirEtiqueta() {
  const nombre = nuevaEtiqueta.value.trim()
  if (!nombre) {
    emit('toast', '⚠️ Ingresá un nombre válido')
    return
  }

  try {
    const response = await axios.post('http://localhost:5000/api/etiquetas', { nombre })
    if (response.data) {
      emit('agregar-etiqueta', response.data)
      emit('toast', `✅ Etiqueta "${nombre}" agregada`)
      nuevaEtiqueta.value = ''
      modalInstance?.hide()

      setTimeout(() => {
        document.activeElement.blur()
        document.body.focus()
      }, 100)
    }
  } catch (error) {
    console.error('❌ Error al guardar la etiqueta:', error)
    emit('toast', '❌ Error al guardar la etiqueta')
  }
}
</script>

<style scoped>
.modal-content {
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  color: #f1f1f1;
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
}

.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #ffc107;
}

.modal-body label {
  font-weight: 500;
  margin-bottom: 5px;
  color: #fff;
}

.form-control {
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: #fff;
}

.form-control:focus {
  border-color: #ffc107;
  box-shadow: 0 0 8px rgba(255, 193, 7, 0.4);
  outline: none;
}

.btn {
  font-weight: 500;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.btn-primary {
  background-color: #ffc107;
  color: #000;
  border: none;
}

.btn-primary:hover {
  background-color: #e6b800;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-close {
  filter: invert(1);
}
</style>

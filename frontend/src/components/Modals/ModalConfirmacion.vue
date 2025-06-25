<template>
  <div class="modal fade" id="modalConfirmarEliminacion" tabindex="-1" aria-hidden="true" ref="modalRef">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">¿Estás seguro?</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p>{{ mensaje }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
          <button :class="['btn', colorBoton]" @click="confirmarAccion">Confirmar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  mensaje: {
    type: String,
    required: true
  },
  colorBoton: {
    type: String,
    default: 'btn-danger'
  }
})

const emit = defineEmits(['confirmar'])

const modalRef = ref(null)
let modalInstance = null

onMounted(() => {
  modalInstance = new bootstrap.Modal(modalRef.value)
})

function abrir() {
  modalInstance?.show()
}

function confirmarAccion() {
  emit('confirmar')
  cerrar()
}


function cerrar() {
  modalInstance?.hide()
}

defineExpose({ abrir, cerrar })
</script>

<style scoped>
.modal-content {
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  color: #f1f1f1;
  border-radius: 15px;
  border: none;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(6px);
}

.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  font-weight: 600;
  font-size: 1.4rem;
  color: #ffc107;
}

.btn-close {
  filter: invert(1);
}

.modal-body p {
  font-size: 1.05rem;
  color: #ddd;
  margin: 0;
}

.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  font-weight: 500;
  padding: 10px 18px;
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-danger {
  background-color: #dc3545;
  color: #fff;
  border: none;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-warning {
  background-color: #ff9800;
  border: none;
  color: #000;
}

.btn-warning:hover {
  background-color: #e67e00;
}

.btn-primary {
  background-color: #ffc107;
  border: none;
  color: #000;
}

.btn-primary:hover {
  background-color: #e6b800;
}
</style>

<template>
  <div class="modal fade" tabindex="-1" ref="modalRef">
    <div class="modal-dialog">
      <div class="modal-content bg-dark text-white rounded-4 shadow-lg border border-warning">
        <div class="modal-header border-0 pb-0">
          <h5 class="modal-title d-flex align-items-center gap-2">
            <i class="fas fa-eye text-warning"></i> Usuario: {{ usuario?.nombre }}
          </h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            data-bs-dismiss="modal"
            aria-label="Cerrar"
          ></button>
        </div>

        <div class="modal-body pt-1">
          <div class="detalle-usuario">
            <p><i class="fas fa-user text-warning me-2"></i> <strong>Nombre:</strong> {{ usuario?.nombre }}</p>
            <p><i class="fas fa-envelope text-warning me-2"></i> <strong>Email:</strong> {{ usuario?.email }}</p>
            <p><i class="fas fa-user-tag text-warning me-2"></i> <strong>Rol:</strong> {{ usuario?.rol }}</p>

            <p v-if="usuario?.telefono">
              <i class="fas fa-phone text-warning me-2"></i> <strong>Teléfono:</strong> {{ usuario.telefono }}
            </p>

            <p v-if="usuario?.ubicacion">
              <i class="fas fa-map-marker-alt text-warning me-2"></i>
              <strong>Ubicación:</strong> {{ usuario.ubicacion }}
            </p>

            <p v-if="usuario?.fechaRegistro">
              <i class="fas fa-calendar-alt text-warning me-2"></i>
              <strong>Registro:</strong> {{ formatFecha(usuario.fechaRegistro) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  usuario: Object
})

const modalRef = ref(null)
let instanciaModal = null

const abrir = () => {
  if (modalRef.value) {
    instanciaModal = new Modal(modalRef.value)
    instanciaModal.show()
  }
}

const formatFecha = (timestamp) => {
  if (!timestamp) return ''
  const fecha = timestamp.toDate ? timestamp.toDate() : new Date(timestamp)
  return fecha.toLocaleString()
}

defineExpose({ abrir })
</script>

<style scoped>
.detalle-usuario {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-size: 0.95rem;
}

.detalle-usuario p {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(255, 193, 7, 0.15);
}

.modal-body {
  padding: 1.5rem 2rem;
  animation: aparecer 0.3s ease;
}

.modal-content {
  border: 1px solid #ffc107;
  border-radius: 16px;
}

.modal-header {
  padding: 1.2rem 2rem 0.5rem;
  border-bottom: none;
}

@keyframes aparecer {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

</style>

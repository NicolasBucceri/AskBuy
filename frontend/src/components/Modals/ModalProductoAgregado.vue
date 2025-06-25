<template>
  <div
    class="modal fade"
    id="modalProductoAgregado"
    tabindex="-1"
    aria-labelledby="modalProductoAgregadoLabel"
    aria-hidden="true"
    ref="modalRef"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-admin-dark">
        <div class="modal-header">
          <h5 class="modal-title texto-dorado" id="modalProductoAgregadoLabel">
            🎉 ¡Producto Agregado!
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body texto-blanco">
          El producto se cargó correctamente en la base de datos.
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-admin" data-bs-dismiss="modal">
            Aceptar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const modalRef = ref(null)
let modalInstance = null

onMounted(() => {
  modalInstance = new bootstrap.Modal(modalRef.value)
})

function abrir() {
  modalInstance?.show()
}

defineExpose({ abrir })
</script>

<style scoped>
.modal-admin-dark {
  background-color: #1c1c1c;
  border: 1px solid #444;
  color: var(--colorTextoSecundario);
}

.texto-dorado {
  color: var(--colorTerciario);
  font-weight: bold;
}

.texto-blanco {
  color: #fff;
}

.btn-admin {
  background-color: var(--colorTerciario);
  border: none;
  color: #fff;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-admin:hover {
  background-color: var(--colorTerciarioHover);
  transform: scale(1.05);
}

.btn-close-white {
  filter: invert(1);
}
</style>

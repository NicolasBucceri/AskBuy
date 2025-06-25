<template>
  <teleport to="body">
    <div class="noti-container">
      <div
        v-for="noti in notificaciones"
        :key="noti.id"
        :class="['noti-toast', noti.tipo, { saliendo: noti.saliendo }]"
      >
        <i class="icono" :class="noti.icono"></i>
        <div class="contenido">
          <span class="titulo">{{ noti.titulo }}</span>
          <span class="tiempo">Ahora</span>
          <p class="mensaje">{{ noti.mensaje }}</p>
        </div>
        <button class="btn-cerrar" @click="cerrar(noti.id)" aria-label="Cerrar notificación">×</button>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'

const notificaciones = ref([])
let idCounter = 0

function mostrar(titulo, mensaje, tipo = 'info') {
  const id = idCounter++
  const icono =
    tipo === 'success' ? 'fas fa-check-circle' :
    tipo === 'error' ? 'fas fa-times-circle' :
    'fas fa-info-circle'

  const nueva = { id, titulo, mensaje, tipo, icono, saliendo: false }
  notificaciones.value.unshift(nueva)

  setTimeout(() => cerrar(id), 4000)
}

function cerrar(id) {
  const index = notificaciones.value.findIndex(n => n.id === id)
  if (index === -1) return

  notificaciones.value[index].saliendo = true
  setTimeout(() => {
    notificaciones.value = notificaciones.value.filter(n => n.id !== id)
  }, 300)
}

defineExpose({ mostrar })
</script>

<style scoped>
.noti-container {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 999999 !important;
  display: flex;
  flex-direction: column-reverse;
  gap: 1rem;
}

.noti-toast {
  background-color: #212529;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  min-width: 280px;
  max-width: 350px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  gap: 12px;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease-out;
}

.noti-toast.saliendo {
  opacity: 0;
  transform: translateY(20px);
}

.noti-toast.success {
  border-left: 5px solid #28a745;
}

.noti-toast.error {
  border-left: 5px solid #dc3545;
}

.noti-toast.info {
  border-left: 5px solid #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.icono {
  margin-top: 2px;
  font-size: 1.2rem;
}

.contenido {
  flex: 1;
}

.titulo {
  display: block;
  font-weight: 600;
}

.tiempo {
  font-size: 0.75rem;
  color: #ccc;
}

.mensaje {
  margin: 0.2rem 0 0;
  font-size: 0.9rem;
}

.btn-cerrar {
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}
</style>

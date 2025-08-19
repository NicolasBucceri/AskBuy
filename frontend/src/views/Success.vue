<template>
  <div class="container text-white py-5 text-center">
    <h2 class="mb-4">✅ ¡Pago realizado con éxito!</h2>

    <div v-if="datosPago">
      <p class="fs-5">Gracias por tu compra de <strong>{{ datosPago.producto.nombre }}</strong>.</p>
      <img
        :src="datosPago.producto.imagen"
        alt="Producto"
        class="my-3"
        style="max-width: 180px; border-radius: 12px;"
      />
      <p class="mb-2">Cantidad: {{ datosPago.cantidad }}</p>
      <p class="mb-4">Total abonado: <strong>{{ formatPrice(datosPago.total) }}</strong></p>
    </div>
    <div v-else>
      <p>No se encontraron datos del pago.</p>
    </div>

    <button class="btn btn-outline-warning" @click="volverInicio">
      Volver al inicio
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const datosPago = ref(null)

onMounted(() => {
  const datos = localStorage.getItem('datosPago')
  if (datos) {
    datosPago.value = JSON.parse(datos)
    localStorage.removeItem('datosPago') // limpiamos después de usarlo
  }
})

function volverInicio() {
  router.push('/')
}

function formatPrice(value) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(value || 0)
}
</script>

<style scoped>
.container {
  min-height: 80vh;
}
</style>

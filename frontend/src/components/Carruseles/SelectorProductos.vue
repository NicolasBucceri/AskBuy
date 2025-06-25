<template>
  <div class="selector-productos mt-4">
    <label class="form-label fw-bold">Seleccioná los productos</label>

    <!-- Buscador -->
    <input type="text" class="form-control mb-3 buscador" placeholder="Buscar por nombre..." v-model="busqueda" />

    <!-- Lista visual de productos -->
    <div class="producto-grid">
      <div v-for="producto in productosFiltrados" :key="producto.id" class="producto-card"
        :class="{ seleccionado: seleccionadosLocales.includes(producto.id) }" @click="toggleSeleccion(producto.id)">
        <div class="img-wrap">
          <img :src="producto.imagen" alt="Producto" />
        </div>

        <div class="info-wrap">
          <h6 class="nombre">{{ producto.nombre }}</h6>
          <p class="precio">{{ formatPrice(producto.precio) }}</p>
        </div>

        <div class="check-overlay" v-if="seleccionadosLocales.includes(producto.id)">
          <i class="fas fa-check"></i>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  productos: Array,
  seleccionados: Array
})

const emit = defineEmits(['actualizar'])

const seleccionadosLocales = ref([...props.seleccionados])
const busqueda = ref('')


const productosFiltrados = computed(() => {
  return props.productos.filter(p =>
    p.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
  )
})

watch(() => props.seleccionados, (nuevos) => {
  seleccionadosLocales.value = [...nuevos]
}, { immediate: true })

function toggleSeleccion(id) {
  const index = seleccionadosLocales.value.indexOf(id)
  if (index === -1) {
    seleccionadosLocales.value.push(id)
  } else {
    seleccionadosLocales.value.splice(index, 1)
  }
  emit('actualizar', seleccionadosLocales.value) // 👈 esta línea es clave
}


function formatPrice(value) {
  if (!value || isNaN(value)) return '$0';
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0
  }).format(value);
}
</script>


<style scoped>
.selector-productos {
  border: 1px solid #555;
  padding: 1rem;
  border-radius: 12px;
  background-color: #1f1f1f;
  max-height: 500px;
  overflow-y: auto;
}

/* Input buscador */
.buscador {
  background-color: #2a2a2a;
  color: white;
  border-radius: 10px;
  border: 1px solid #444;
  padding: 0.6rem 1rem;
}
.buscador::placeholder {
  color: white;
  opacity: 0.6; /* podés subir o bajar el contraste */
}

.buscador:focus {
  outline: none;
  border-color: var(--colorTerciario);
  box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.2);
}

/* Grid visual */
.producto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.producto-card {
  background: #2c2c2c;
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #eee;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.producto-card:hover {
  transform: translateY(-3px);
  border-color: #666;
}

.producto-card.seleccionado {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 10px rgba(250, 204, 21, 0.4);
}

.img-wrap img {
  width: 100%;
  height: 100px;
  object-fit: contain;
  margin-bottom: 0.5rem;
}

.info-wrap {
  text-align: center;
  margin-bottom: 0.5rem;
}

.nombre {
  font-size: 0.9rem;
  font-weight: 600;
}

.precio {
  font-size: 0.85rem;
  color: #aaa;
}

.check-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: var(--colorTerciario);
  color: #000;
  border-radius: 50%;
  padding: 4px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
}

</style>

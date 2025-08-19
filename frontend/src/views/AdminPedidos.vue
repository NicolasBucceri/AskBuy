<template>
  <div class="admin-pedidos text-white">
    <h1 class="mb-4 fw-bold text-warning">📦 Gestión de Pedidos</h1>

    <!-- Tabs Bootstrap -->
    <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="activos-tab" data-bs-toggle="tab" data-bs-target="#activos-pane"
          type="button" role="tab" aria-controls="activos-pane" aria-selected="true">
          Pedidos Activos
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="entregados-tab" data-bs-toggle="tab" data-bs-target="#entregados-pane"
          type="button" role="tab" aria-controls="entregados-pane" aria-selected="false">
          Pedidos Entregados
        </button>
      </li>
    </ul>

    <!-- Contenido -->
    <div class="tab-content" id="myTabContent">
      <div class="tab-pane fade show active" id="activos-pane" role="tabpanel" aria-labelledby="activos-tab"
        tabindex="0">
        <PedidosActivos />
      </div>

      <div class="tab-pane fade" id="entregados-pane" role="tabpanel" aria-labelledby="entregados-tab" tabindex="0">
        <PedidosEntregados />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const entregadosRef = ref(null)

import PedidosActivos from '../components/SeccionesDePedidos/PedidosActivos.vue'
import PedidosEntregados from '../components/SeccionesDePedidos/PedidosEntregados.vue'

const recargarEntregados = () => {
  entregadosRef.value?.cargarPedidos() // Llama a la función del hijo
}
</script>

<style scoped>
.admin-pedidos {
  background-color: #0a0a0a;
  min-height: 100vh;
  padding: 1.5rem;
}

.nav-tabs {
  border-bottom: 1px solid var(--colorTerciario);
}

.nav-tabs .nav-link {
  color: var(--colorTextoSecundario);
  background: transparent !important;
  border: none !important;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  transition: color 0.2s ease-in-out, border-color 0.2s ease-in-out;
}

.nav-tabs .nav-link:hover {
  color: var(--colorTerciario);
  background: transparent !important;
}

.nav-tabs .nav-link.active {
  color: var(--colorTerciario) !important; /* Texto amarillo */
  background: transparent !important;
  border: none !important;
  border-bottom: 3px solid #fff !important; /* Subrayado blanco */
  font-weight: 700;
}

</style>

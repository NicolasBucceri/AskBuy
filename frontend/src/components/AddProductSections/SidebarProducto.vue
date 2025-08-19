<template>
  <div>
    <!-- Sidebar Izquierda -->
    <div class="sidebarIzquierda">
      <a v-for="seccion in secciones" :key="seccion.id" href="#"
        @click.prevent="$emit('update:activeSection', seccion.id)" :class="{ active: activeSection === seccion.id }"
        :title="seccion.tooltip">
        <i :class="seccion.icono"></i>
      </a>

      <div class="sidebarBottom">
        <a class="btnSidebar" @click="$emit('abrirModalCategoriasEtiquetas')">
          <i class="fas fa-tags"></i>
        </a>
      </div>
    </div>

    <!-- Sidebar Derecha -->
    <div class="sidebarDerecha">
      <a href="#" data-bs-toggle="tooltip" data-bs-placement="bottom"
        :title="product.ocultar ? 'Producto oculto' : 'Producto visible'" @click="$emit('toggleOcultar')">
        <i :class="product.ocultar ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
      </a>
      <a href="#" @click.prevent="$emit('abrirModalVistaPrevia')" title="Ampliar Vista">
        <i class="fas fa-expand"></i>
      </a>

      <div class="sidebarBottom">
        <a href="#" @click.prevent="$emit('abrirModalLimpieza')" title="Limpiar Formulario" class="text-danger">
          <i class="fas fa-trash-alt"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  activeSection: Number,
  product: Object
});

const secciones = [
  { id: 1, icono: 'fas fa-info-circle', tooltip: 'Información' },
  { id: 2, icono: 'fas fa-images', tooltip: 'Imágenes' },
  { id: 3, icono: 'fa-solid fa-file', tooltip: 'Detalles Técnicos' },
  { id: 4, icono: 'fas fa-palette', tooltip: 'Modelos' },
  { id: 5, icono: 'fas fa-list', tooltip: 'Resumen' }
];
</script>

<style scoped>
.sidebarIzquierda {
  width: 80px;
  background: #343a40;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  flex-shrink: 0;
  min-height: 100vh;
  overflow: hidden;
}

.sidebarBottom {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  align-items: center;
  margin-top: auto;
  padding-bottom: 20px;
}

.sidebarIzquierda a {
  color: white;
  font-size: 24px;
  margin: 10px 0;
  text-decoration: none;
  padding: 10px;
  transition: background 0.3s;
}

.sidebarIzquierda a:hover {
  background: #495057;
  border-radius: 8px;
}

.sidebarIzquierda a.active {
  background: var(--colorTerciario);
  color: #343a40;
  border-radius: 8px;
}

.sidebarDerecha {
  width: 80px;
  background: #3b3b3b;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  flex-shrink: 0;
  min-height: 100vh;
  overflow: hidden;
  position: fixed;
  right: 0;
  top: 0;
}

.sidebarDerecha a {
  color: var(--colorTerciario);
  font-size: 24px;
  margin: 10px 0;
  text-decoration: none;
  padding: 10px;
  transition: background 0.3s;
}

.btnSidebar {
  padding: 10px !important;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btnSidebar:hover {
  background-color: #0056b3;
}
</style>

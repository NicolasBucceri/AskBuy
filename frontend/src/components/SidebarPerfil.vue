<template>
  <div class="sidebarPerfil">
    <a v-for="seccion in secciones" :key="seccion.id"
       href="#" @click.prevent="$emit('update:seccionActiva', seccion.id)"
       :class="{ active: seccionActiva === seccion.id }"
       :title="seccion.tooltip">
      <i :class="seccion.icono"></i>
    </a>

    <div class="sidebarBottom">
      <a href="#" title="Cerrar sesión" @click.prevent="$emit('cerrarSesion')">
        <i class="fas fa-sign-out-alt"></i>
      </a>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  seccionActiva: Number
})


const secciones = [
  { id: 1, icono: 'fas fa-user', tooltip: 'Datos personales' },
  { id: 2, icono: 'fas fa-heart', tooltip: 'Favoritos' },
  { id: 3, icono: 'fas fa-shopping-bag', tooltip: 'Historial de compras' },
  { id: 4, icono: 'fas fa-cog', tooltip: 'Configuración avanzada' }
]
</script>

<style scoped>
.sidebarPerfil {
  width: 80px;
  background: #343a40;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}

.sidebarPerfil a {
  color: white;
  font-size: 22px;
  margin: 12px 0;
  text-decoration: none;
  padding: 12px;
  transition: background 0.3s;
  border-radius: 8px;
}

.sidebarPerfil a:hover {
  background: #495057;
}

.sidebarPerfil a.active {
  background: var(--colorTerciario);
  color: #343a40;
}

.sidebarBottom {
  margin-top: auto;
  padding-bottom: 20px;
}
</style>

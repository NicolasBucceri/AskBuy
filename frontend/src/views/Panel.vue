<template>
  <div class="admin-wrapper py-5" v-if="usuarioActual">
    <div class="header text-center mb-5">
      <h1 class="display-5 fw-bold text-white">Panel de Administración</h1>
      <p class="text-light">Gestioná tu contenido de manera eficiente</p>
    </div>

    <div class="admin-grid container">
      <router-link v-for="card in cards" :key="card.titulo" :to="card.ruta" class="admin-option"
        :style="{ background: card.gradient }" :aria-label="`Ir a ${card.titulo}`">

        <div class="icon-container mb-3">
          <i :class="card.icono"></i>
        </div>
        <div class="text-container">
          <small class="text-white-50">{{ card.textoSecundario }}</small>
          <h3 class="text-white fw-bold mb-0">{{ card.titulo }}</h3>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'


const usuarioActual = ref(null)

onMounted(() => {
  const guardado = localStorage.getItem('usuarioActual')
  if (guardado) {
    usuarioActual.value = JSON.parse(guardado)
  }
})

const cards = computed(() => {
  const base = [
    {
      titulo: "Agregar Producto", textoSecundario: "Administrá", ruta: "/add-product", icono: "fa-solid fa-plus", gradient: "linear-gradient(135deg, #ff416c, #ff4b2b)"
    },
    {
      titulo: "Ver Productos", textoSecundario: "Gestioná", ruta: "/adminproductos", icono: "fa-solid fa-boxes-stacked", gradient: "linear-gradient(135deg, #f7971e, #ffd200)"
    },
    {
      titulo: "Pedidos", textoSecundario: "Revisá", ruta: "/admin-pedidos", icono: "fa-solid fa-truck", gradient: "linear-gradient(135deg, #1e3c72, #2a5298)"
    },
    {
      titulo: "Descuentos", textoSecundario: "Promocioná", ruta: "/admindescuentos", icono: "fa-solid fa-tags", gradient: "linear-gradient(135deg, #6a11cb, #2575fc)"
    },
    {
      titulo: "Carruseles", textoSecundario: "Editá el Home", ruta: "/admincarruseles", icono: "fa-solid fa-sliders", gradient: "linear-gradient(135deg, #fc4a1a, #f7b733)"
    },
    {
      titulo: "Carga Masiva", textoSecundario: "Subí productos", ruta: "/admincargamasiva", icono: "fa-solid fa-file-import", gradient: "linear-gradient(135deg, #43cea2, #185a9d)"
    },
    {
      titulo: "Analíticas", textoSecundario: "Analizá", ruta: "/adminanaliticas", icono: "fa-solid fa-chart-line", gradient: "linear-gradient(135deg, #ff5f6d, #ffc371)"
    },

  ]


  const extraAdmin = {
    titulo: "Usuarios", textoSecundario: "Controlá", ruta: "/listausuarios", icono: "fa-solid fa-users", gradient: "linear-gradient(135deg, #1d976c, #93f9b9)"
  }

  return usuarioActual.value?.rol?.toLowerCase() === 'admin' ? [...base, extraAdmin] : base

})


</script>

<style scoped>
.admin-wrapper {
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  min-height: 100vh;
}

.header {
  background: rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 20px;
  margin: 0 auto;
  max-width: 700px;
  backdrop-filter: blur(4px);
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.admin-option {
  text-decoration: none;
  padding: 2rem;
  border-radius: 20px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.admin-option:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.4);
}

.icon-container {
  font-size: 2.8rem;
    transition: transform 0.3s ease;
}

.admin-option:hover .icon-container {
  transform: scale(1.1);
}

@media (max-width: 600px) {
  .admin-wrapper {
    padding: 2rem 1rem;
  }

  .admin-option {
    padding: 1.5rem;
    font-size: 0.9rem;
  }

  .icon-container {
    font-size: 2.2rem;
    margin-bottom: 1rem;
  }

  .header h1 {
    font-size: 1.8rem;
  }

  .header p {
    font-size: 0.95rem;
  }
}
</style>
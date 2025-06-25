<template>
  <div>
    <BannerHome />
    <CategoriasHome />
    <IconosSeccion />
    <ProductList />
    <ServicioExpress />
    <TutorialTooltip v-if="mostrarTutorial" @cerrar="cerrarTutorial" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { auth } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'

import BannerHome from '../views/BannerHome.vue'
import CategoriasHome from '../views/CategoriasHome.vue'
import IconosSeccion from '../views/IconosSeccion.vue'
import ProductList from '../components/ProductList.vue'
import ServicioExpress from '../views/ServicioExpress.vue'
import TutorialTooltip from '../components/TutorialTooltip.vue'

const mostrarTutorial = ref(false)
const displayName = ref('')

onMounted(() => {
  const desdeRegistro = localStorage.getItem('registroRecienHecho')
  console.log('🔍 [HomeView] flag registroRecienHecho =', desdeRegistro)

  onAuthStateChanged(auth, user => {
    console.log('👤 [HomeView] onAuthStateChanged user =', user)
    if (user && desdeRegistro === 'true') {
      displayName.value = user.displayName || 'usuario'
      mostrarTutorial.value = true
      console.log('✅ [HomeView] mostrando tutorial a', displayName.value)
    } else {
      console.log('❌ [HomeView] no muestro tutorial')
    }
  })
})

// cerrarTutorial limpia todo
function cerrarTutorial() {
  mostrarTutorial.value = false
  localStorage.removeItem('registroRecienHecho')
  console.log('🗑️ [HomeView] flag borrado')
}
</script>

<style scoped>
/* ... tus estilos existentes ... */
</style>

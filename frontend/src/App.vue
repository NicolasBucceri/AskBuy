<template>
  <div id="app">
    <Navbar />
    <router-view />
    <Footer v-if="noMostrarFooter" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

const route = useRoute()

// Ocultar footer solo en la vista de login-registro
const noMostrarFooter = computed(() =>
  route.name !== 'LoginRegistro'
  && route.name !== 'AddProduct'
  && route.name !== 'Panel'
  && route.name !== 'AdminProductos'
  && route.name !== 'AdminDescuentos'
  && route.name !== 'AdminCarruseles'
  && route.name !== 'AdminCargaMasiva'
  && route.name !== 'AdminAnaliticas'
  && route.name !== 'ListaUsuarios'
);

</script>



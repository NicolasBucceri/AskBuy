<template>
  <div class="bg-white shadow-lg rounded-lg p-4">
    <img :src="producto.imagen" class="w-full h-40 object-cover rounded-t-lg">
    <h2 class="text-lg font-bold">{{ producto.nombre }}</h2>
    <p class="text-gray-600">{{ producto.descripcion }}</p>
    <span class="text-green-500 font-semibold">${{ producto.precio }}</span>
  </div>
</template>

<script setup>
defineProps(["productos"]);
</script>

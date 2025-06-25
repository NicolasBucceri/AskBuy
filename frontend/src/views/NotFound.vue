<!-- views/NotFound.vue -->
<template>
  <div class="notfound">
    <h1>🚧 404</h1>
    <p>La ruta que estás buscando no existe o no tenés permiso para acceder.</p>
    <router-link to="/" class="btn-volver">Volver al inicio</router-link>
  </div>
</template>

<style scoped>
.notfound {
  text-align: center;
  padding: 100px 20px;
  color: #fff;
  background-color: #121212;
}
.notfound h1 {
  font-size: 6rem;
  color: var(--colorTerciario);
}
.btn-volver {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: var(--colorTerciario);
  color: #000;
  border-radius: 8px;
  text-decoration: none;
}
</style>

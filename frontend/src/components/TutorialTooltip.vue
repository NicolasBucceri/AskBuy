<template>
  <div class="tooltip-container">
    <div class="flecha"></div>
    <div class="tooltip-box">
      <p>👋 ¡Completá tu perfil para aprovechar al máximo tu cuenta!</p>
      <button @click="$emit('cerrar')">Entendido</button>
    </div>
  </div>
</template>

<script>
export default {
  emits: ['cerrar']
}
</script>

<style scoped>
.tooltip-container {
  position: absolute;
  top: 50px; /* ajustalo según tu navbar */
  right: 230px; /* ajustalo para apuntar al botón de perfil */
  z-index: 9999;
}

.tooltip-box {
  background-color: #1c1c1c;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
  font-size: 0.95rem;
  text-align: center;
  max-width: 280px;
}

.tooltip-box button {
  margin-top: 0.75rem;
  background-color: var(--colorTerciario);
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  color: #000;
}

.flecha {
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 12px solid #1c1c1c;
  margin: 0 auto;
}
</style>

<template>
  <teleport to="body">
    <div class="overlay-spinner" v-show="visible">

      <div class="spinner-content">
        <img src="../assets/Logos/LogoAB.png" alt="AskBuy Logo" class="logo-spinner" />

        <p class="mensaje">{{ mensaje }}</p>

      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  mensaje: {
    type: String,
    default: 'Cargando...'
  }
})

const visible = ref(false)

function mostrar() {
  visible.value = true
}
function ocultar() {
  visible.value = false
}

defineExpose({ mostrar, ocultar })
</script>


<style scoped>
.overlay-spinner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(240, 248, 255, 0.75);
  backdrop-filter: blur(6px);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
}


.spinner-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}


/* 👇 Emoji que simula el logo */
.emoji-logo {
  font-size: 3rem;
  animation: girar 1.2s linear infinite;
  margin-bottom: 1rem;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid var(--main-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: girar 1s linear infinite;
  margin: 0 auto;
}

.logo-spinner {
  display: block;
  margin: 0 auto 0 auto;
  width: 100px;
  height: auto;
  animation: girar 1.2s linear infinite;
}



.mensaje {
  margin-top: 1rem;
  color: #333;
  font-weight: 600;
}

@keyframes girar {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>

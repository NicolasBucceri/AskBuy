<template>
  <div class="contact-container">
    <!-- Sección izquierda -->
    <div class="contact-info">
      <h2>Estamos acá</h2>
      <iframe
        class="mapa"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3282.662387434594!2d-58.44585668477077!3d-34.61795186560866!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95bccb6c5d4f83a3%3A0x73e02bcf464da7c9!2sBuenos%20Aires!5e0!3m2!1ses!2sar!4v1617668169256!5m2!1ses!2sar"
        allowfullscreen=""
        loading="lazy"
      ></iframe>

      <div class="info-items">
        <div class="info-item">
          <i class="fas fa-phone-alt"></i>
          <p>+54 9 11 1234 5678</p>
        </div>
        <div class="info-item">
          <i class="fas fa-envelope"></i>
          <p>contacto@askbuy.com</p>
        </div>
        <div class="info-item">
          <i class="fas fa-map-marker-alt"></i>
          <p>Buenos Aires, Argentina</p>
        </div>
      </div>
    </div>

    <!-- Sección derecha -->
    <div class="contact-form">
      <h1>Contáctanos</h1>
      <p class="contact-text">Dejanos tu consulta y te responderemos a la brevedad.</p>

      <form @submit.prevent="enviarFormulario">
        <div class="floating-label">
          <input v-model="form.nombre" type="text" id="nombre" placeholder=" " required />
          <label for="nombre">Nombre</label>
        </div>

        <div class="floating-label">
          <input v-model="form.email" type="email" id="email" placeholder=" " required />
          <label for="email">Correo electrónico</label>
        </div>

        <div class="floating-label campoMensaje">
          <textarea v-model="form.mensaje" id="mensaje" rows="4" placeholder=" " required></textarea>
          <label for="mensaje">Mensaje</label>
        </div>

        <div class="contendorBoton">
          <button type="submit" class="btn-enviar">Enviar Mensaje</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Toast de confirmación -->
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div id="liveToast" class="toast text-bg-dark" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header bg-dark text-white border-0">
        <strong class="me-auto">AskBuy</strong>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Cerrar"></button>
      </div>
      <div class="toast-body d-flex align-items-center gap-2">
        ✅ Tu mensaje fue enviado con éxito
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

let toastEl = null
let toastInstance = null

const form = ref({
  nombre: '',
  email: '',
  mensaje: ''
})

onMounted(() => {
  toastEl = document.getElementById('liveToast')
  toastInstance = new bootstrap.Toast(toastEl)
})

const mostrarToast = (mensaje) => {
  const toastBody = toastEl.querySelector('.toast-body')
  toastBody.innerHTML = `✅ ${mensaje}`

  toastEl.classList.remove('text-bg-success', 'text-bg-danger', 'text-bg-warning')
  toastEl.classList.add('text-bg-dark')

  toastInstance.show()
}

const enviarFormulario = () => {
  console.log('Formulario enviado:', form.value)
  mostrarToast('Tu mensaje fue enviado con éxito')

  form.value = {
    nombre: '',
    email: '',
    mensaje: ''
  }
}
</script>

<style scoped>
.contact-container {
  display: flex;
  flex-wrap: wrap;
  height: 100vh;
  overflow: hidden;
  font-family: var(--fuentePrincipal);
  background-color: var(--colorFondoPrincipal);
  color: var(--colorTextoPrincipal);
}

/* ----- Izquierda ----- */
.contact-info {
  flex: 1 1 50%;
  background-color: var(--colorFondoSecundario);
  color: var(--colorTextoSecundario);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px 40px;
  box-sizing: border-box;
}

.contact-info h2 {
  font-family: var(--fuenteTerciario);
  font-size: 32px;
  margin-bottom: 30px;
}

.mapa {
  width: 100%;
  height: 280px;
  border: none;
  border-radius: 20px;
  margin-bottom: 40px;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
}

.info-item i {
  font-size: 20px;
  min-width: 24px;
  text-align: center;
  color: var(--colorTerciario);
}

.info-item p {
  margin: 0;
  line-height: 1.5;
  font-size: 18px;
}

/* ----- Derecha ----- */
.contact-form {
  flex: 1 1 50%;
  padding: 0px 60px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: var(--colorFondoPrincipal);
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.05);
}

.contact-form h1 {
  font-size: 40px;
  font-weight: 800;
  margin-bottom: 10px;
}

.contact-text {
  font-size: 16px;
  margin-bottom: 50px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.floating-label {
  position: relative;
}

/* INPUTS y TEXTAREAS - Default en Secundario */
/* INPUTS - Default en Secundario */
.floating-label input {
  width: 100%;
  padding: 16px;
  border: 2px solid var(--colorSecundario);
  border-radius: 12px;
  background: transparent;
  font-size: 16px;
  color: var(--colorSecundario);
  transition: all 0.3s ease;
  outline: none;
}

/* TEXTAREA - Custom más grande */
.campoMensaje {
  width: 150%;
  display: flex;
  justify-content: flex-start;
  margin-left: 121px;
}

.campoMensaje textarea {
  width: 110% !important;
  min-height: 160px;
  padding: 16px;
  border: 2px solid var(--colorSecundario);
  border-radius: 12px;
  font-size: 16px;
  resize: vertical;
  background: transparent;
  color: var(--colorSecundario);
  box-sizing: border-box;
}







/* Focus - colorPrincipal */
.floating-label input:focus,
.floating-label textarea:focus {
  border-color: var(--colorPrincipal);
  color: var(--colorSecundario);
}

/* LABEL default */
.floating-label label {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%);
  background-color: var(--colorFondoPrincipal);
  color: var(--colorSecundario);
  padding: 0 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  pointer-events: none;
}

/* Focus o contenido - el label sube y se pone Principal */
.floating-label input:focus + label,
.floating-label textarea:focus + label {
  top: -10px;
  left: 12px;
  font-size: 12px;
  color: var(--colorPrincipal);
}

/* Si tiene contenido pero no focus, vuelve a Secundario */
.floating-label input:not(:focus):not(:placeholder-shown) + label,
.floating-label textarea:not(:focus):not(:placeholder-shown) + label {
  top: -10px;
  left: 12px;
  font-size: 12px;
  color: var(--colorSecundario);
}

/* Cuando no hay focus y no hay contenido */
.floating-label input:placeholder-shown:not(:focus),
.floating-label textarea:placeholder-shown:not(:focus) {
  border-color: var(--colorSecundario);
  color: var(--colorSecundario);
}

.floating-label input:placeholder-shown:not(:focus) + label,
.floating-label textarea:placeholder-shown:not(:focus) + label {
  color: var(--colorSecundario);
}

.campoMensaje textarea {
  width: 100% !important;
  min-height: 140px !important; /* más espacio para escribir */
  resize: vertical; /* opcional, para que lo pueda agrandar */
}





/* Botón enviar */
.contendorBoton {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.btn-enviar {
  display: inline-block;
  padding: 14px 28px;
  font-size: 18px;
  font-weight: 600;
  color: var(--colorFondoSecundario);
  background-color: var(--colorTerciario);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  min-width: 200px;
  text-align: center;
}

.btn-enviar:hover {
  background-color: var(--colorTerciarioHover);
  color: var(--colorFondoPrincipal);
  transform: translateY(-2px);
}

/* Toast estilos */
.toast.text-bg-dark {
  background-color: #212529;
  color: #fff;
  border-radius: 10px;
}

.toast-header {
  background-color: #212529 !important;
  color: #fff !important;
  border-radius: 10px 10px 0 0;
  border: none;
}

.toast-body {
  color: #fff;
  font-size: 14px;
  padding: 16px;
}

.btn-close-white {
  filter: invert(1);
}

/* Responsive */
/* Responsive */
@media (max-width: 1024px) {
  .contact-container {
    flex-direction: column;
    height: auto;
  }

  .contact-info,
  .contact-form {
    flex: 1 1 100%;
    padding: 40px 20px;
    border-radius: 0;
  }

  .contact-info h2 {
    font-size: 26px;
    text-align: center;
  }

  .mapa {
    height: 220px;
  }

  .info-items {
    align-items: center;
  }

  .info-item {
    justify-content: center;
    text-align: center;
  }

  .contact-form h1 {
    font-size: 32px;
    text-align: center;
  }

  .contact-text {
    text-align: center;
    font-size: 14px;
    margin-bottom: 30px;
  }

  .contendorBoton {
    justify-content: center;
  }

  .btn-enviar {
    width: 100%;
    min-width: unset;
  }

  .campoMensaje {
  width: 100%;
  display: flex;
  justify-content: flex-start;
}
}

@media (max-width: 600px) {
  .contact-info,
  .contact-form {
    padding: 20px 15px;
  }

  .contact-info h2 {
    font-size: 22px;
  }

  .mapa {
    height: 180px;
  }

  .info-item p {
    font-size: 16px;
  }

  .contact-form h1 {
    font-size: 26px;
  }

  .floating-label input,
  .floating-label textarea {
    padding: 12px;
    font-size: 14px;
  }

  .floating-label label {
    font-size: 14px;
  }

  .btn-enviar {
    font-size: 16px;
    padding: 12px 20px;
  }
}

</style>

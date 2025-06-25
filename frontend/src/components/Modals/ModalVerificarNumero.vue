<template>
    <div class="modal-verificacion">
        <div class="modal-contenido">
            <h4>Verificar número</h4>
            <p>Te enviaremos un código por SMS para confirmar tu número.</p>

            <input ref="telefonoInputModal" id="telefono" type="tel" class="form-control" placeholder="+54 9 11..." />

            <button class="btn-verificar mt-3" @click="enviarCodigoSMS">
                Enviar código SMS
            </button>

            <div v-if="verificacionEnviada" class="mt-4">
                <label for="codigo">Código recibido</label>
                <input ref="telefonoVerificacion" type="tel" class="form-control" :value="numeroTelefono" />

                <button class="btn-confirmar mt-2" @click="verificarCodigoSMS">Confirmar código</button>
            </div>
            <!-- Invisible reCAPTCHA -->
            <div id="recaptcha-container-modal"></div>

            <button class="btn-cerrar mt-4" @click="$emit('cerrar')">Cerrar</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RecaptchaVerifier, signInWithPhoneNumber } from 'firebase/auth'
import { auth } from '../../firebase'
import intlTelInput from 'intl-tel-input'
import 'intl-tel-input/build/css/intlTelInput.css'
import { watch } from 'vue'

const emit = defineEmits(['cerrar', 'actualizarTelefono' ]) // 👈 agregamos nuevo evento


const telefonoInputModal = ref(null)
const verificacionEnviada = ref(false)
const codigoVerificacion = ref('')
const confirmationResult = ref(null)

let iti = null

const props = defineProps({
  numeroTelefono: String
})

watch(() => props.numeroTelefono, (nuevoValor) => {
  console.log('[Modal] Watch activado - nuevo número:', nuevoValor)
  if (iti && nuevoValor) {
    iti.setNumber(nuevoValor)
    console.log('[Modal] Número seteado por watch:', nuevoValor)
  }
})


onMounted(() => {
  console.log('[Modal] Mounted, props.numeroTelefono:', props.numeroTelefono)

  iti = intlTelInput(telefonoInputModal.value, {
    initialCountry: "ar",
    preferredCountries: ["ar", "us", "es"],
    separateDialCode: true,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.19/build/js/utils.js"
  })

  telefonoInputModal.value.addEventListener('input', () => {
  const numeroActualizado = iti.getNumber() || telefonoInputModal.value.value
  emit('actualizarTelefono', numeroActualizado)
})


  // ⛔ Este console te dice si llega algo en el primer render
  if (props.numeroTelefono) {
    console.log('[Modal] Seteando número en onMounted:', props.numeroTelefono)
    iti.setNumber(props.numeroTelefono)
  } else {
    console.warn('[Modal] Número no presente al montar')
  }
})


const enviarCodigoSMS = async () => {
    try {
        const numero = telefonoInputModal.value?.value
        if (!numero || numero.length < 6) return alert("Número inválido")

        window.recaptchaVerifier = new RecaptchaVerifier(auth, "recaptcha-container-modal", {
            size: "invisible"
        })

        confirmationResult.value = await signInWithPhoneNumber(auth, numero, window.recaptchaVerifier)
        verificacionEnviada.value = true
        alert("Código enviado ✅")
    } catch (error) {
        alert("Error al enviar SMS: " + error.message)
    }
}

const verificarCodigoSMS = async () => {
    try {
        await confirmationResult.value.confirm(codigoVerificacion.value)
        alert("¡Número verificado correctamente! ✅")
        emit('cerrar')
    } catch (error) {
        alert("Código incorrecto ❌")
    }
}
</script>

<style scoped>
.modal-verificacion {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.modal-contenido {
    background: #fff;
    padding: 2rem;
    border-radius: 12px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

input.form-control {
    width: 100%;
    padding: 0.7rem;
    border-radius: 10px;
    border: 1px solid #ccc;
    margin-top: 0.5rem;
}

.btn-verificar,
.btn-confirmar,
.btn-cerrar {
    width: 100%;
    padding: 0.7rem;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    transition: 0.3s ease;
}

.btn-verificar {
    background-color: var(--colorPrincipal);
    color: white;
}

.btn-verificar:hover {
    background-color: var(--colorPrincipalHover);
}

.btn-confirmar {
    background-color: var(--colorExito);
    color: white;
}

.btn-confirmar:hover {
    background-color: #1e7e34;
}

.btn-cerrar {
    background-color: #ddd;
    color: #333;
}

.btn-cerrar:hover {
    background-color: #bbb;
}
</style>

<template>
    <div class="configuracion-avanzada">
        <h2 class="tituloSeccion">Configuración Avanzada</h2>

        <!-- 🔄 Cambiar Email -->
        <!-- 🔄 Cambiar Email -->
        <div class="form-group">
            <label for="nuevoEmail">Nuevo correo electrónico</label>
            <input id="nuevoEmail" v-model="nuevoEmail" type="email" class="form-control"
                placeholder="ejemplo@correo.com" />

            <label for="contrasenaEmail">Contraseña actual</label>
            <div class="campo-contrasena">
                <input id="contrasenaEmail" :type="mostrarContrasenaEmail ? 'text' : 'password'"
                    v-model="contrasenaActualEmail" class="form-control" placeholder="********" />
                <i :class="mostrarContrasenaEmail ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-icon"
                    @click="mostrarContrasenaEmail = !mostrarContrasenaEmail"></i>
            </div>

            <button class="btn-accion" @click="actualizarEmail" :disabled="!nuevoEmail || !contrasenaActualEmail">
                Actualizar correo
            </button>
        </div>

        <!-- 🔒 Cambiar Contraseña -->
        <div class="form-group">
            <label for="contrasenaActual">Contraseña actual</label>
            <div class="campo-contrasena">
                <input id="contrasenaActual" :type="mostrarContrasenaActual ? 'text' : 'password'"
                    v-model="contrasenaActualContrasena" class="form-control" placeholder="********" />
                <i :class="mostrarContrasenaActual ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-icon"
                    @click="mostrarContrasenaActual = !mostrarContrasenaActual"></i>
            </div>

            <label for="nuevaContrasena">Nueva contraseña</label>
            <div class="campo-contrasena">
                <input id="nuevaContrasena" :type="mostrarNuevaContrasena ? 'text' : 'password'"
                    v-model="nuevaContrasena" class="form-control" placeholder="Mínimo 6 caracteres" />
                <i :class="mostrarNuevaContrasena ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-icon"
                    @click="mostrarNuevaContrasena = !mostrarNuevaContrasena"></i>
            </div>

            <button class="btn-accion" @click="actualizarContrasena"
                :disabled="!nuevaContrasena || !contrasenaActualContrasena">
                Actualizar contraseña
            </button>
        </div>

    </div>
</template>



<script setup>
import { ref, onMounted } from 'vue'
import { auth } from '../../firebase'
import { EmailAuthProvider, reauthenticateWithCredential, updateEmail, updatePassword  } from 'firebase/auth'

const nuevoEmail = ref('')
const nuevaContrasena = ref('')
const contrasenaActual = ref('') // 🔐 campo extra
const user = ref(null)
const contrasenaActualEmail = ref('')
const contrasenaActualContrasena = ref('')

const mostrarNuevaContrasena = ref(false)

contrasenaActualContrasena.value = ''
nuevaContrasena.value = ''



onMounted(() => {
    user.value = auth.currentUser
    if (user.value) {
        nuevoEmail.value = user.value.email // 🧠 precarga
    }
})

// ✅ Reautenticación común
const reautenticar = async () => {
    if (!user.value || !contrasenaActual.value) throw new Error("Falta la contraseña actual")
    const cred = EmailAuthProvider.credential(user.value.email, contrasenaActual.value)
    await reauthenticateWithCredential(user.value, cred)
}

const actualizarEmail = async () => {
  const user = auth.currentUser
  console.log('📧 Intentando actualizar email...', { nuevoEmail: nuevoEmail.value, user })

  if (!user || !nuevoEmail.value || !contrasenaActualEmail.value) {
    console.warn('🚫 Datos incompletos para actualizar email')
    return
  }

  const credential = EmailAuthProvider.credential(user.email, contrasenaActualEmail.value)

  try {
    await reauthenticateWithCredential(user, credential)
    console.log('✅ Reautenticación exitosa para email')

    await updateEmail(user, nuevoEmail.value)
    console.log('✅ Email actualizado correctamente')
    alert('✅ Correo actualizado con éxito')
  } catch (error) {
    console.error('❌ Error al actualizar correo:', error)
    alert('❌ Error al actualizar correo: ' + error.message)
  }
}


const actualizarContrasena = async () => {
  console.log('🔐 Intentando actualizar contraseña...', { nuevaContrasena: nuevaContrasena.value })

  try {
    const credential = EmailAuthProvider.credential(user.value.email, contrasenaActualContrasena.value)
    await reauthenticateWithCredential(user.value, credential)
    console.log('✅ Reautenticación exitosa para contraseña')

    await updatePassword(user.value, nuevaContrasena.value)
    console.log('✅ Contraseña actualizada correctamente')
    alert('🔒 Contraseña actualizada correctamente')
  } catch (error) {
    console.error('❌ Error al actualizar contraseña:', error)
    alert('❌ Error al actualizar contraseña: ' + error.message)
  }
}


</script>


<style scoped>
.configuracion-avanzada {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem 0;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

label {
    font-weight: 600;
}

input.form-control {
    padding: 0.8rem;
    border-radius: 10px;
    border: 1px solid #ccc;
}

.configuracion-avanzada {
    padding: 1.5rem;
    background: #f1f1f1;
    border-radius: 12px;
}

.form-group {
    margin-bottom: 2rem;
}

.btn-accion {
    margin-top: 1rem;
    background: var(--colorPrincipal);
    color: white;
    border: none;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
}

.btn-accion:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.campo-contrasena {
    position: relative;
}

.toggle-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: #666;
}
</style>

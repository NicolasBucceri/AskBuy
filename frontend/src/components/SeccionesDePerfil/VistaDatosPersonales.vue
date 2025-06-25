<template>
    <div class="perfil-right">
        <h5 class="tituloSeccion">Información principal</h5>

        <div class="form-grid">
            <!-- NOMBRE -->
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input :value="nombre" @input="$emit('update:nombre', $event.target.value)" id="nombre" type="text"
                    class="form-control" placeholder="Tu nombre" />
                <p v-if="!nombreEsValido(nombre)" class="aviso-edad-invalida">
                    🚫 Ese nombre no está permitido
                </p>
            </div>

            <!-- TELÉFONO -->
            <div class="form-group">
                <label for="telefono">Teléfono</label>
                <input ref="telefonoInput" id="telefono" type="tel" class="form-control" placeholder="+54 9 11..."
                    style="min-width: 289px" />

                <!-- Botón de verificar -->
                <div class="btn-verificar-wrapper" v-if="mostrarVerificar">

                    <button class="btn-verificar-discreto" @click="$emit('abrirModalVerificacion')">
                        Verificar número
                    </button>
                </div>

                <!-- Ícono de número verificado -->
                <i v-if="numeroValido" class="fas fa-check-circle text-success ms-2"></i>
            </div>


            <!-- FECHA NACIMIENTO -->
            <div class="form-group">
                <label for="fechaNacimiento">Fecha de nacimiento</label>
                <input :value="fechaNacimiento" @input="$emit('update:fechaNacimiento', $event.target.value)"
                    id="fechaNacimiento" type="date" class="form-control" :max="fechaMaxima" />
                <p v-if="fechaNacimiento && calcularEdad < 18" class="aviso-edad-invalida">
                    Debés tener al menos 18 años
                </p>
            </div>
        </div>

        <h5 class="tituloSeccion">Dirección</h5>
        <div class="form-grid">
            <div class="form-group"><label>Calle</label>
                <input :value="direccion.calle"
                    @input="$emit('update:direccion', { ...direccion, calle: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>Número</label>
                <input :value="direccion.numero"
                    @input="$emit('update:direccion', { ...direccion, numero: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>Piso / Depto</label>
                <input :value="direccion.depto"
                    @input="$emit('update:direccion', { ...direccion, depto: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>Código Postal</label>
                <input :value="direccion.cp"
                    @input="$emit('update:direccion', { ...direccion, cp: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>Ciudad</label>
                <input :value="direccion.ciudad"
                    @input="$emit('update:direccion', { ...direccion, ciudad: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>Provincia</label>
                <input :value="direccion.provincia"
                    @input="$emit('update:direccion', { ...direccion, provincia: $event.target.value })"
                    class="form-control" />
            </div>
            <div class="form-group"><label>País</label>
                <input :value="direccion.pais"
                    @input="$emit('update:direccion', { ...direccion, pais: $event.target.value })"
                    class="form-control" />
            </div>
        </div>

        <button class="btn-editar mt-6" @click="$emit('guardar')">
            <i class="fa-solid fa-floppy-disk me-2"></i> Guardar cambios
        </button>
    </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, watch } from 'vue'
import 'intl-tel-input/build/css/intlTelInput.css'
import intlTelInput from 'intl-tel-input'
import utilsScript from 'intl-tel-input/build/js/utils.js?url'


const props = defineProps({
    nombre: String,
    fechaNacimiento: String,
    direccion: Object,
    fechaMaxima: String,
    numeroValido: Boolean,
    mostrarBotonVerificar: Boolean,
    telefono: String

})


const emit = defineEmits([
    'update:nombre',
    'update:fechaNacimiento',
    'update:direccion',
    'update:telefono',
    'guardar',
    'abrirModalVerificacion'
])

const telefonoInput = ref(null)
const iti = ref(null)
const mostrarVerificar = ref(false)


const telefono = ref(props.telefono || '')

// 👉 Sincroniza si cambia desde el padre
watch(() => props.telefono, (nuevo) => {
    telefono.value = nuevo || ''

    if (telefonoInput.value && iti.value) {
        iti.value.setNumber(nuevo || '')
        console.log('📲 Input actualizado con número del padre:', nuevo)
    }
})


// 🛠️ Al montar, inicializamos intl-tel-input y emitimos valor inicial
onMounted(async () => {
    await nextTick()

    if (!telefonoInput.value) {
        console.warn('🚨 telefonoInput no está montado todavía')
        return
    }

    iti.value = intlTelInput(telefonoInput.value, {
        initialCountry: 'ar',
        preferredCountries: ['ar', 'us', 'es'],
        utilsScript
    })

    // 👇 Recién acá es seguro
    telefonoInput.value.value = props.telefono || ''
    iti.value.setNumber(props.telefono || '')

    const numeroFormateadoInicial = iti.value.getNumber() || telefonoInput.value.value
    console.log('📤 Emitiendo teléfono inicial:', numeroFormateadoInicial)
    emit('update:telefono', numeroFormateadoInicial)

    telefonoInput.value.addEventListener('input', async () => {
        await nextTick()
        const numeroCrudo = telefonoInput.value.value
        const numero = iti.value.getNumber() || numeroCrudo
        emit('update:telefono', numero)

        const cantidadNumeros = numero.replace(/\D/g, '').length

        const esValido =
            iti.value.isValidNumber() ||
            (numero.startsWith('+54') && numero.includes('11') && cantidadNumeros >= 10)

        mostrarVerificar.value = esValido
    })

})

// 🔒 Validación de nombre
const palabrasProhibidas = ['pito', 'pene', 'mierda', 'caca', 'concha', 'verga', 'puta']
const nombreEsValido = (nombre) => {
    const limpio = nombre.toLowerCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]/g, '')
    return !palabrasProhibidas.some(pal => limpio.includes(pal))
}

// 🎂 Calcular edad
const calcularEdad = computed(() => {
    if (!props.fechaNacimiento) return ''
    const hoy = new Date()
    const nacimiento = new Date(props.fechaNacimiento)
    let edad = hoy.getFullYear() - nacimiento.getFullYear()
    const mes = hoy.getMonth() - nacimiento.getMonth()
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) edad--
    return edad
})



defineExpose({
    telefonoInput,
    iti
})

</script>

<style scoped>
body {
    margin: 0;
    padding: 0;
}

.tituloSeccion {
    margin-bottom: 20px;
    font-weight: bold;
    font-size: 25px;
}

.perfil-container {
    display: flex;
    flex-direction: row;
    min-height: 100vh;
    width: 100%;
}

.sidebarPerfil {
    position: relative;
    height: auto;
    flex-shrink: 0;
    width: 80px;
}

.perfil-wrapper {
    flex: 1;
    padding: 2rem;
    max-width: 1400px;
    margin: auto;
    background-color: #f5f5f5;
    border-radius: 1.5rem;
    box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.05);
}

.perfil-layout {
    display: flex;
    flex-direction: row;
    background-color: #e8e8e8;
    color: #222;
    min-height: 700px;
    border-radius: 1.5rem;
    padding: 2rem;
    gap: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.perfil-left {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-right: 1px solid #ccc;
    padding: 2rem 1rem;
}

.perfil-right {
    flex: 3;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.avatar-preview img {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.perfil-avatar-selector {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.avatar-options {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
}

.avatar-option {
    position: relative;
    cursor: pointer;
    border-radius: 50%;
    overflow: hidden;
    transition: transform 0.2s;
}

.avatar-option:hover {
    transform: scale(1.1);
}

.avatar-option input[type="radio"] {
    display: none;
}

.avatar-option img {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid transparent;
}

.avatar-option input[type="radio"]:checked+img {
    border-color: var(--colorTerciario);
}

.datos-usuario {
    margin-top: 1.5rem;
    font-size: 0.95rem;
    color: #444;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
    text-align: center;
}

.dato-linea {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.dato-linea i {
    color: var(--colorPrincipal);
    font-size: 1rem;
}

.dato-linea.uid {
    font-size: 0.8rem;
    color: #777;
    word-break: break-word;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.25rem;
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
    color: var(--colorTextoPrincipal);
}

input.form-control {
    width: 100%;
    padding: 0.9rem 1.1rem;
    font-size: 0.95rem;
    border: 1px solid #d0d0d0;
    border-radius: 12px;
    background-color: #fdfdfd;
    color: #333;
    transition: all 0.3s ease;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

input.form-control:hover {
    border-color: var(--colorTerciario);
    box-shadow: 0 0 0 2px rgba(255, 193, 7, 0.2);
}

input.form-control:focus {
    border-color: var(--colorPrincipal);
    box-shadow: 0 0 0 2px rgba(13, 110, 253, 0.25);
    outline: none;
}

input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(0.6);
    cursor: pointer;
}

.btn-editar {
    background-color: var(--colorTerciario);
    color: #000;
    border: none;
    padding: 0.9rem 1.5rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1rem;
    width: 100%;
    transition: all 0.3s ease;
    margin-top: 2rem;
}

.btn-editar:hover {
    background-color: var(--colorTerciarioHover);
    color: white;
}

.btn-verificar-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}

.btn-verificar-discreto {
    background-color: transparent;
    color: var(--colorPrincipal);
    border: 1px solid var(--colorPrincipal);
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    margin-top: 0.5rem;
}

.btn-verificar-discreto:hover {
    background-color: var(--colorPrincipal);
    color: white;
}


.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.aviso-edad-invalida {
    color: #dc3545;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.aviso-edad-invalida::before {
    display: inline-block;
}
</style>

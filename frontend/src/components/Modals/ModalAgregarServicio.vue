<template>
  <div>
    <!-- Fondo oscuro con transición -->
    <transition name="fade">
      <div v-if="visible" class="modal-backdrop-custom"></div>
    </transition>

    <!-- Modal -->
    <div class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
        <div class="modal-content bg-dark text-white p-4 rounded-4 shadow-lg">

          <div class="modal-header border-0 pb-0">
            <h4 class="modal-title fw-bold">
              <i class="bi bi-clipboard-plus-fill me-2 text-warning"></i> Agregar nuevo servicio
            </h4>
            <button type="button" class="btn-close btn-close-white" @click="cerrarModal"></button>
          </div>

          <form @submit.prevent="guardarServicio" class="w-100">
            <div class="modal-body pt-3">
              <div class="row g-4 h-100">
                <!-- Columna izquierda -->
                <div class="col-md-8 d-flex flex-column justify-content-between">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Nombre</label>
                      <input v-model="nuevoServicio.nombre" type="text" placeholder="Nico"
                        class="form-control form-control-lg rounded-pill">
                      <small class="text-danger" v-if="errores.nombre">{{ errores.nombre }}</small>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Apellido</label>
                      <input v-model="nuevoServicio.apellido" type="text" placeholder="Diaz"
                        class="form-control form-control-lg rounded-pill" :class="{ 'is-invalid': errores.apellido }">
                      <small class="text-danger" v-if="errores.apellido">{{ errores.apellido }}</small>
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">DNI</label>
                      <input v-model="nuevoServicio.dni" type="text" placeholder="12345678"
                        class="form-control form-control-lg rounded-pill" :class="{ 'is-invalid': errores.dni }">
                      <small class="text-danger" v-if="errores.dni">{{ errores.dni }}</small>
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">Celular</label>
                      <input v-model="nuevoServicio.celular" type="text" placeholder="1151083065"
                        class="form-control form-control-lg rounded-pill" :class="{ 'is-invalid': errores.celular }">
                      <small class="text-danger" v-if="errores.celular">{{ errores.celular }}</small>
                    </div>

                    <div class="col-md-12">
                      <label class="form-label">Email</label>
                      <input v-model="nuevoServicio.email" type="email" placeholder="nicolasbucceri@hotmail.com"
                        class="form-control form-control-lg rounded-pill" :class="{ 'is-invalid': errores.email }">
                      <small class="text-danger" v-if="errores.email">{{ errores.email }}</small>
                    </div>

                    <div class="col-md-12">
                      <label class="form-label">Técnico</label>
                      <select v-model="nuevoServicio.tecnico" class="form-select form-select-lg rounded-pill"
                        :class="{ 'is-invalid': errores.tecnico }">
                        <option disabled value="">Seleccione</option>
                        <option v-for="t in tecnicos" :key="t.id" :value="t.nombre">
                          {{ t.nombre }}
                        </option>
                      </select>
                      <small class="text-danger" v-if="errores.tecnico">{{ errores.tecnico }}</small>
                    </div>
                    <div class="col-md-12">
                      <label class="form-label">Tipo de servicio</label>
                      <select v-model="nuevoServicio.tipoServicio" class="form-select form-select-lg rounded-pill"
                        :class="{ 'is-invalid': errores.tipoServicio }">
                        <option disabled value="">Seleccione</option>
                        <option value="Reparación">Reparación</option>
                        <option value="Mantenimiento">Mantenimiento</option>
                        <option value="Instalación">Instalación</option>
                        <option value="Diagnóstico">Diagnóstico</option>
                      </select>
                      <small class="text-danger" v-if="errores.tipoServicio">{{ errores.tipoServicio }}</small>
                    </div>
                    <div class="col-md-12">
                      <label class="form-label">Precio</label>
                      <input v-model="nuevoServicio.precio" type="number" min="0" placeholder="Ej: 10000"
                        class="form-control form-control-lg rounded-pill" :class="{ 'is-invalid': errores.precio }">
                      <small class="text-danger" v-if="errores.precio">{{ errores.precio }}</small>
                    </div>


                  </div>
                </div>

                <!-- Columna derecha -->
                <div class="col-md-4 d-flex flex-column">
                  <label class="form-label">Descripción del servicio</label>
                  <textarea v-model="nuevoServicio.descripcion" placeholder="Descripción"
                    class="form-control rounded-4 p-3" rows="12"></textarea>
                </div>
              </div>
            </div>

            <div class="modal-footer border-0 pt-4">
              <button type="button" class="btn btn-light rounded-pill px-4" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn btn-warning rounded-pill px-4 fw-bold">Guardar servicio</button>
            </div>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch, defineProps, defineEmits } from 'vue'
import { collection, getDocs, addDoc, updateDoc, doc } from 'firebase/firestore'
import { db } from '../../firebase'

// 🟡 Props y emits
const props = defineProps({
  visible: Boolean,
  servicioParaEditar: Object
})

const emit = defineEmits(['cerrar', 'servicioAgregado', 'servicioEditado'])

// 📝 Datos del formulario
const nuevoServicio = reactive({
  nombre: '',
  apellido: '',
  dni: '',
  celular: '',
  email: '',
  tecnico: '',
  descripcion: '',
  tipoServicio: '',
  precio: ''
})

const errores = reactive({
  nombre: '',
  apellido: '',
  dni: '',
  celular: '',
  email: '',
  tecnico: '',
  descripcion: '',
  tipoServicio: '',
  precio: ''
})


// 🔧 Técnicos
const tecnicos = ref([])

onMounted(async () => {
  document.body.style.overflow = 'hidden'

  try {
    const snapshot = await getDocs(collection(db, 'usuarios'))
    snapshot.forEach(doc => {
      const data = doc.data()
      if (data.rol === 'moderador') {
        tecnicos.value.push({
          id: doc.id,
          nombre: data.nombre
        })
      }
    })
  } catch (error) {
    console.error('Error al obtener usuarios:', error)
  }

  // ESC para cerrar
  const escHandler = (e) => {
    if (e.key === 'Escape') cerrarModal()
  }

  document.addEventListener('keydown', escHandler)
  onUnmounted(() => {
    document.removeEventListener('keydown', escHandler)
    document.body.style.overflow = 'auto'
  })
})

// 🟡 Carga los datos si está en modo edición
watch(
  () => props.servicioParaEditar,
  (nuevoValor) => {
    if (nuevoValor) {
      Object.assign(nuevoServicio, nuevoValor)
    } else {
      resetearFormulario()
    }
  },
  { immediate: true }
)

// 🧼 Reset
function resetearFormulario() {
  Object.assign(nuevoServicio, {
    nombre: '',
    apellido: '',
    dni: '',
    celular: '',
    email: '',
    tecnico: '',
    descripcion: '',
    tipoServicio: ''
  })
  Object.keys(errores).forEach(key => errores[key] = '')
}

// ❌ Cerrar modal
function cerrarModal() {
  document.body.style.overflow = 'auto'
  resetearFormulario()
  emit('cerrar')
}

// ✅ Guardar o actualizar
async function guardarServicio() {
  Object.keys(errores).forEach(key => errores[key] = '')
  let valido = true

  for (const campo in nuevoServicio) {
    if (!nuevoServicio[campo]) {
      errores[campo] = `El campo ${campo} es obligatorio.`
      valido = false
    }
  }

  if (!valido) return

  try {
    if (props.servicioParaEditar?.id) {
      // ✏️ Editar
      await updateDoc(doc(db, 'servicios', props.servicioParaEditar.id), { ...nuevoServicio })
      emit('servicioEditado', { ...nuevoServicio, id: props.servicioParaEditar.id })
    } else {
      // ➕ Nuevo
      const docRef = await addDoc(collection(db, 'servicios'), {
        ...nuevoServicio,
        fechaCreacion: new Date()
      })
      emit('servicioAgregado', { ...nuevoServicio, id: docRef.id })

      // WhatsApp sólo en alta
      const numeroLimpio = nuevoServicio.celular.replace(/\D/g, '')
      const numeroWhatsApp = `549${numeroLimpio}`
      const mensaje = encodeURIComponent(
        `¡Hola ${nuevoServicio.nombre}! Gracias por confiar en AskBuy. Tu servicio fue registrado correctamente. Pronto nos pondremos en contacto.`
      )
      const link = `https://wa.me/${numeroWhatsApp}?text=${mensaje}`
      window.open(link, '_blank')
    }

    cerrarModal()
  } catch (error) {
    console.error('Error al guardar el servicio:', error)
  }
}
</script>

<style scoped>
/* Fondo del modal */
.modal-content {
  background-color: #121212 !important;
  color: #f1f1f1;
}

/* Fondo opaco con animación */
.modal-backdrop-custom {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(3px);
  z-index: 1040;
}

/* Animación fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Inputs */
.form-label {
  font-weight: 600;
  color: #f1c40f;
}

.form-control,
.form-select,
textarea {
  background-color: #1e1e1e !important;
  color: #ffffff;
  font-size: 0.95rem;
  padding: 0.55rem 1rem;
  border: 1px solid #444;
  transition: border 0.3s, box-shadow 0.3s;
}

.form-control-lg,
.form-select-lg {
  font-size: 0.95rem !important;
  padding: 0.55rem 1rem !important;
}

.form-control:focus,
.form-select:focus,
textarea:focus {
  border-color: #f1c40f;
  box-shadow: 0 0 0 0.15rem rgba(241, 196, 15, 0.25);
}

textarea {
  resize: none;
}

::placeholder {
  color: #aaa;
  font-weight: 400;
}

.btn-warning {
  background-color: #f1c40f;
  border: none;
  color: #000;
}

.btn-warning:hover {
  background-color: #e0b90d;
}

.btn-light {
  background-color: #2c2c2c;
  border: 1px solid #444;
  color: #f1f1f1;
}

.btn-light:hover {
  background-color: #3a3a3a;
}

small.text-danger {
  font-size: 0.875rem;
  font-weight: 500;
}

.is-invalid {
  border: 2px solid #dc3545 !important;
}

.col-md-6:last-of-type {
  margin-top: 0.5rem;
}
.form-label[for="tipoServicio"],
.form-label[for="precio"] {
  margin-top: 1rem;
  border-left: 4px solid #f1c40f;
  padding-left: 0.5rem;
}

</style>

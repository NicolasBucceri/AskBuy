<template>
    <div class="container py-5 text-white">
        <h2 class="mb-5 display-5 fw-bold text-center text-warning">Seguimiento de tus Servicios</h2>

        <div v-if="cargando" class="text-center text-muted fs-6">Cargando servicios...</div>
        <div v-else-if="servicios.length === 0" class="text-center text-muted fs-5">Aún no hay servicios cargados.</div>

        <div v-for="servicio in servicios" :key="servicio.id"
            class="card bg-gradient-dark mb-5 shadow rounded-4 border border-warning p-4">

            <div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-3">
                <div>
                    <h4 class="text-white fw-bold mb-1">{{ servicio.nombre }} {{ servicio.apellido }}</h4>
                    <p class="mb-1"><i
                            class="fa-solid fa-screwdriver-wrench me-2 text-warning"></i><strong>Técnico:</strong> {{
                                servicio.tecnico || 'Sin asignar' }}</p>
                    <p><i class="fa-regular fa-file-lines me-2 text-warning"></i><strong>Descripción:</strong> {{
                        servicio.descripcion }}</p>
                </div>
                <div class="text-end">
                    <span class="badge bg-warning text-dark fs-6">{{ textoEtapa(servicio.estado) }}</span>
                    <div class="mt-2 fs-5 text-white">
                        <i class=" me-1 text-success"></i><strong>{{ formatoPrecio(servicio.precio) }}</strong>

                    </div>
                </div>
            </div>


            <!-- 🟡 Barra de progreso animada -->
            <div class="progress-bar-wrapper mt-4">
                <div class="progress-line">
                    <div class="progress-fill" :style="{ width: porcentajeAvance(servicio.estado) + '%' }"></div>
                </div>
                <div class="progress-steps d-flex justify-content-between mt-2">
                    <div v-for="(etapa, index) in etapas" :key="index" class="step text-center"
                        :class="{ 'step-active': index <= servicio.estado }">
                        <div class="icon-wrapper mb-1">
                            <i :class="iconoEtapa(etapa)"></i>
                        </div>
                        <small>{{ etapa }}</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { collection, query, where, orderBy, onSnapshot } from 'firebase/firestore'
import { db } from '../firebase'
import { getAuth, onAuthStateChanged } from 'firebase/auth'

// 🧾 Lista reactiva de servicios del usuario
const servicios = ref([])
const cargando = ref(true)


// 🪜 Etapas del servicio
const etapas = [
    "Ingresado",
    "En Revisión",
    "Casi Terminado",
    "Listo para Retirar"
]

const textoEtapa = (numero) => etapas[numero] || 'Desconocido'

// 🎯 Íconos por etapa
const iconoEtapa = (estado) => {
    switch (estado) {
        case "Ingresado":
            return "fa-solid fa-box-open text-secondary"
        case "En Revisión":
            return "fa-solid fa-magnifying-glass text-info"
        case "Casi Terminado":
            return "fa-solid fa-tools text-primary"
        case "Listo para Retirar":
            return "fa-solid fa-check-circle text-success"
        default:
            return "fa-regular fa-circle text-muted"
    }
}

// 📡 Escuchar en tiempo real los servicios vinculados al email del usuario
const auth = getAuth()

onAuthStateChanged(auth, (user) => {
    if (!user) {
        console.warn("No hay usuario logueado")
        return
    }

    const q = query(
        collection(db, 'servicios'),
        where('email', '==', user.email),
        orderBy('fechaCreacion', 'desc')
    )

    onSnapshot(q, (snapshot) => {
        cargando.value = false
        servicios.value = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }))
    })
})
const porcentajeAvance = (estado) => {
  const totalEtapas = etapas.length - 1
  const base = (estado / totalEtapas) * 100

  // Evitamos que se pase del 100%
  const ajuste = estado < totalEtapas ? 12 : 0

  return Math.min(base + ajuste, 100)
}


const formatoPrecio = (valor) => {
  if (!valor || isNaN(valor)) return '$0';
  return `$${Number(valor).toLocaleString('es-AR')}`;
}

</script>




<style scoped>
.bg-gradient-dark {
    background: linear-gradient(to right, #1f1f1f, #2c2c2c);
}

.progress-bar-wrapper {
    position: relative;
    padding: 1rem 0;
}

.progress-line {
    height: 6px;
    background-color: #333;
    border-radius: 10px;
    overflow: hidden;
}

.progress-fill {
    height: 6px;
    background-color: #ffc107;
    transition: width 0.6s ease-in-out;
}

.progress-steps .step {
    width: 24%;
    color: #888;
}

.step-active {
    color: #fff;
}

.icon-wrapper {
    font-size: 1.2rem;
    background-color: #333;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    transition: background-color 0.3s;
}

.step-active .icon-wrapper {
    background-color: #ffc107;
    color: black;
}

.card {
  backdrop-filter: blur(4px);
  background: linear-gradient(145deg, #1e1e1e, #292929);
  border: 1px solid #444;
  box-shadow: 0 0 10px rgba(255, 193, 7, 0.1);
}

.progress-line {
  height: 6px;
  background-color: #333;
  border-radius: 10px;
  overflow: visible; /* por si acaso */
}

.card .badge {
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 12px;
}

</style>

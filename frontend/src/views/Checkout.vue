<template>
  <div class="checkout container py-5 text-white">
    <h2 class="mb-4 text-center">Resumen de tu compra</h2>

    <div v-if="producto" class="resumen-compra p-4 rounded-4 shadow">
      <div class="row g-4">
        
        <!-- 🖼 Producto -->
        <div class="col-md-6">
          <div class="producto-card">
            <img :src="producto.imagen" alt="Producto" />
            <h4>{{ producto.nombre }}</h4>
            <p>Color: {{ producto.color }}</p>
            <p>Cantidad: {{ producto.cantidad }}</p>
          </div>
        </div>

        <!-- 📦 Detalles -->
        <div class="col-md-6 d-flex flex-column justify-content-between">
          <div>
            <div class="envio-card mb-3">
              <h5>Dirección de envío</h5>

              <!-- Dirección en perfil -->
              <div v-if="!direccionIncompleta" class="bg-light p-3 rounded mb-3">
                {{ direccion.calle }} {{ direccion.numero }},
                {{ direccion.ciudad }}, {{ direccion.provincia }},
                (CP {{ direccion.cp }}) - {{ direccion.pais }}
              </div>

              <!-- Dirección faltante -->
              <div v-else>
                <div class="alert alert-warning p-2 mb-3">
                  ⚠️ No tienes dirección guardada en tu perfil.
                </div>
                <small class="text-muted mb-2 d-block">
                  Esta dirección se guardará en tu perfil y se usará para este pedido.
                </small>

                <div class="p-3 rounded mb-3 bg-dark">
                  <input v-model="direccionTemporal.calle" placeholder="Calle" class="form-control mb-2" />
                  <input v-model="direccionTemporal.numero" placeholder="Número" class="form-control mb-2" />
                  <input v-model="direccionTemporal.ciudad" placeholder="Ciudad" class="form-control mb-2" />
                  <input v-model="direccionTemporal.provincia" placeholder="Provincia" class="form-control mb-2" />
                  <input v-model="direccionTemporal.cp" placeholder="Código Postal" class="form-control mb-2" />
                  <input v-model="direccionTemporal.pais" placeholder="País" class="form-control mb-2" />
                  <input v-model="direccionTemporal.depto" placeholder="Depto (opcional)" class="form-control mb-2" />
                </div>
              </div>
            </div>

            <h5>Total a pagar</h5>
            <p class="fs-4 fw-bold text-success">
              {{ formatPrice(producto.precio * producto.cantidad) }}
            </p>
          </div>

          <button
            class="btn btn-warning w-100 fw-semibold mt-3"
            @click="pagarConMercadoPago"
            :disabled="loading || !direccionValida"
          >
            {{ loading ? 'Generando pago...' : 'Pagar con Mercado Pago' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else>
      <p class="text-center">No hay producto para comprar.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { getAuth } from 'firebase/auth'
import {
  getFirestore,
  doc,
  getDoc,
  updateDoc,
  collection,
  addDoc,
  serverTimestamp
} from 'firebase/firestore'

const auth = getAuth()
const db = getFirestore()

const producto = ref(null)
const direccion = ref({})
const direccionTemporal = ref({})
const loading = ref(false)

onMounted(() => {
  const item = localStorage.getItem('productoParaCheckout')
  if (item) producto.value = JSON.parse(item)
  cargarDireccionUsuario()
})

async function cargarDireccionUsuario() {
  const user = auth.currentUser
  if (!user) return
  try {
    const docRef = doc(db, 'usuarios', user.uid)
    const docSnap = await getDoc(docRef)
    direccion.value = docSnap.exists() ? docSnap.data().direccion || {} : {}
  } catch (e) {
    console.error('❌ Error al obtener la dirección:', e)
  }
}

const direccionIncompleta = computed(() => {
  return !direccion.value?.calle || !direccion.value?.numero
})

const direccionValida = computed(() => {
  if (!direccionIncompleta.value) return true
  const d = direccionTemporal.value
  return d.calle && d.numero && d.ciudad && d.provincia && d.cp && d.pais
})

function formatPrice(value) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(value || 0)
}

async function guardarDireccionEnPerfil(dir) {
  const user = auth.currentUser
  if (!user) return console.warn('⚠️ Usuario no autenticado')

  const ref = doc(db, 'usuarios', user.uid)
  await updateDoc(ref, { direccion: dir })

  direccion.value = dir
  console.log('✅ Dirección guardada en el perfil')
}

async function guardarCompra(producto) {
  const user = auth.currentUser
  if (!user) return console.warn('⚠️ Usuario no autenticado')

  const direccionCompra = !direccionIncompleta.value
    ? direccion.value
    : direccionTemporal.value

  // Si estaba incompleta, guardar en perfil
  if (direccionIncompleta.value) {
    await guardarDireccionEnPerfil(direccionTemporal.value)
  }

  const compra = {
    usuarioId: user.uid,
    email: user.email,
    producto: {
      nombre: producto.nombre,
      cantidad: producto.cantidad,
      precio_unitario: producto.precio,
      imagen: producto.imagen,
      color: producto.color || ''
    },
    total: producto.precio * producto.cantidad,
    direccion: direccionCompra,
    estado: 'pendiente',
    fecha: serverTimestamp()
  }

  await addDoc(collection(db, 'compras'), compra)
  await addDoc(collection(db, `usuarios/${user.uid}/compras`), compra)
}

async function pagarConMercadoPago() {
  if (!producto.value) return
  const payload = {
    nombre: producto.value.nombre || '',
    cantidad: parseInt(producto.value.cantidad || 1),
    precio: parseFloat(producto.value.precio || 0),
    imagen: producto.value.imagen || ''
  }
  try {
    loading.value = true
    const response = await axios.post('http://localhost:5000/crear-preferencia', payload)
    if (response.data.sandbox_init_point) {
      await guardarCompra(producto.value)
      window.location.href = response.data.sandbox_init_point
    } else {
      alert('No se pudo generar la preferencia de pago.')
    }
  } catch (error) {
    console.error('❌ Error al generar preferencia:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.checkout.container {
  max-width: 100% !important; /* que ocupe todo el ancho */
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.checkout {
  min-height: 100vh;
  padding: 2rem 0;
  /* Fondo moderno degradado */
  background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
}

.resumen-compra {
  border: 1px solid rgba(255, 193, 7, 0.3);
  background-color: #121212;
  border-radius: 1rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
}


/* Card general */
.resumen-compra {
  border: 1px solid rgba(255, 193, 7, 0.3);
  background-color: #121212;
}

/* Card producto */
.producto-card {
  background-color: #1a1a1a;
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
}

.producto-card img {
  max-width: 200px;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.producto-card h4 {
  color: var(--colorTerciario);
}

/* Card envío */
.envio-card {
  background-color: #1a1a1a;
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 10px;
  padding: 1rem;
}

.envio-card h5 {
  color: var(--colorTerciario);
}

.envio-card .bg-light {
  background-color: #2a2a2a !important;
  color: white !important;
}

/* Inputs */
.form-control {
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: white;
}

.form-control:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 5px var(--colorTerciario);
  background-color: #2a2a2a;
}

/* Botón */
.btn-warning {
  background-color: var(--colorTerciario);
  border: none;
  font-weight: bold;
}

.btn-warning:hover {
  background-color: var(--colorTerciarioHover);
}

/* Alertas */
.alert-warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: var(--colorTerciario);
  border: 1px solid var(--colorTerciario);
}
</style>

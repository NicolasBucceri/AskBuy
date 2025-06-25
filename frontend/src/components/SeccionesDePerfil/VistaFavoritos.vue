<template>
  <div class="productosVista">
    <h1 class="titulo">Tus productos favoritos</h1>

    <SpinnerCarga ref="spinnerRef"  />

    <div v-if="productosConDescuento.length" class="llevateloYa">
      <h2>🔥 ¡Llevátelo YA con descuento!</h2>
      <div class="gridProductos">
        <div v-for="prod in productosConDescuento" :key="prod.id" class="cardProducto">
          <router-link :to="`/producto/${prod.id}`" class="contenidoCard">
            <img :src="prod.imagen" class="imagen" />
            <h3>{{ prod.nombre }}</h3>

            <!-- Precio original tachado -->
            <p class="precio-original" v-if="prod.porcentajeDescuento">
              {{ formatPrice(calcularPrecioOriginal(prod)) }}
            </p>

            <!-- Precio con descuento -->
            <p class="precio-descuento">
              {{ formatPrice(prod.precio) }}
            </p>

            <!-- Badge de descuento -->
            <span class="badge-descuento">-{{ prod.porcentajeDescuento }}% OFF</span>
          </router-link>
        </div>
      </div>
    </div>

    <div class="gridProductos">
      <div v-for="prod in productos" :key="prod.id" class="cardProducto">
        <!-- Botón de favorito -->
        <button class="btn-fav" @click.stop="toggleFavorito(prod)">
          <i :class="[
            estaEnFavoritos(prod.id) ? 'fas fa-heart' : 'far fa-heart',
            animandoId === prod.id ? 'latido' : ''
          ]"></i>
        </button>

        <router-link :to="`/producto/${prod.id}`" class="contenidoCard">
          <img :src="prod.imagen" alt="Imagen" class="imagen" />
          <h3>{{ prod.nombre }}</h3>
          <p class="precio">{{ formatPrice(prod.precio) }}</p>
          <p class="categoria">{{ prod.categoria }}</p>
        </router-link>
      </div>
    </div>
  </div>

  <button v-if="!loading && productos.length" class="btn-vaciar" @click="vaciarFavoritos">
    Vaciar favoritos 🗑️
  </button>

  <p v-if="!loading && productos.length === 0" class="mensaje-vacio">
    No tenés productos agregados a favoritos 😢
  </p>

  <Notificacion ref="notiRef" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { auth, db } from '../../firebase'
import { doc, getDoc, setDoc } from 'firebase/firestore'
import { onAuthStateChanged } from 'firebase/auth'
import Notificacion from '../ToastNotificacion.vue'
import SpinnerCarga from '../SpinnerCarga.vue'

const productos = ref([])
const animandoId = ref(null)
const notiRef = ref(null)
const spinnerRef = ref(null)
const loading = ref(true)

onMounted(() => {
  spinnerRef.value?.mostrar()
  onAuthStateChanged(auth, async (user) => {
    if (!user) {
      loading.value = false
      spinnerRef.value?.ocultar()
      return
    }

    try {
      const userRef = doc(db, 'usuarios', user.uid)
      const docSnap = await getDoc(userRef)
      const idsFavoritos = docSnap.exists() ? (docSnap.data().favoritos || []) : []

      const res = await fetch("http://localhost:5000/api/products")
      const todosLosProductos = await res.json()

      productos.value = todosLosProductos.filter(p => idsFavoritos.includes(p.id))

      if (productosConDescuento.value.length > 0 && notiRef.value) {
        notiRef.value.mostrar(
          '¡Descuentos activos!',
          '🤑 Tenés productos con descuento entre tus favoritos',
          'success'
        )
      }
    } catch (error) {
      console.error('❌ Error al cargar productos:', error)
      if (notiRef.value) {
        notiRef.value.mostrar('Error', 'No se pudieron cargar los productos', 'error')
      }
    } finally {
      loading.value = false
      spinnerRef.value?.ocultar()
    }
  })
})

const formatPrice = (value) => {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(value || 0)
}

const estaEnFavoritos = (id) => {
  return productos.value.some(p => p.id === id)
}

const toggleFavorito = async (producto) => {
  const user = auth.currentUser
  if (!user) {
    if (notiRef.value) {
      notiRef.value.mostrar(
        'Iniciá sesión',
        'Tenés que tener una cuenta para usar favoritos',
        'info'
      )
    }
    return
  }

  const userRef = doc(db, 'usuarios', user.uid)
  const docSnap = await getDoc(userRef)
  let idsFavoritos = docSnap.exists() ? (docSnap.data().favoritos || []) : []

  let mensaje = ''
  let tipo = ''

  if (idsFavoritos.includes(producto.id)) {
    idsFavoritos = idsFavoritos.filter(id => id !== producto.id)
    productos.value = productos.value.filter(p => p.id !== producto.id)
    mensaje = 'Se eliminó de tus favoritos'
    tipo = 'error'
  } else {
    idsFavoritos.push(producto.id)
    productos.value.push(producto)
    mensaje = 'Agregado a favoritos con éxito'
    tipo = 'success'
  }

  await setDoc(userRef, { favoritos: idsFavoritos }, { merge: true })

  if (notiRef.value) {
    notiRef.value.mostrar('Favoritos', mensaje, tipo)
  }
}

const vaciarFavoritos = async () => {
  const user = auth.currentUser
  if (!user) return

  try {
    const userRef = doc(db, 'usuarios', user.uid)
    await setDoc(userRef, { favoritos: [] }, { merge: true })
    productos.value = []

    if (notiRef.value) {
      notiRef.value.mostrar(
        'Favoritos vaciados',
        'Eliminaste todos los productos de tu lista',
        'error'
      )
    }
  } catch (error) {
    console.error('❌ Error al vaciar favoritos:', error)
    if (notiRef.value) {
      notiRef.value.mostrar('Error', 'No se pudo vaciar favoritos', 'error')
    }
  }
}

const productosConDescuento = computed(() =>
  productos.value
    .filter(p => p.descuento === true && p.porcentajeDescuento > 0)
    .sort((a, b) => b.porcentajeDescuento - a.porcentajeDescuento)
)

const calcularPrecioOriginal = (producto) => {
  if (producto.tipoDescuento === 'porcentaje' && producto.porcentajeDescuento) {
    const descuento = Number(producto.porcentajeDescuento);
    const precioConDescuento = Number(producto.precio);
    return Math.round((precioConDescuento * 100) / (100 - descuento));
  }
  return producto.precio;
}
</script>


<style scoped>
.productosVista {
  padding: 2rem;
}

.titulo {
  text-align: center;
  font-family: var(--fuentePrincipal);
  margin-bottom: 2rem;
}

.gridProductos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 2rem;
}

.cardProducto {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 1.5rem;
  background: #fff;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 100%;
  border: 1px solid transparent;
  position: relative;
}

.cardProducto:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  border-color: var(--main-color);
}

.cardProducto .imagen {
  height: 160px;
  object-fit: contain;
  margin-bottom: 1rem;
  width: 100%;
}

.cardProducto h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  line-height: 1.4;
  color: #1f2937;
  /* gris oscuro elegante */
}

.cardProducto .precio {
  font-size: 1rem;
  font-weight: bold;
  color: #1d4ed8;
  /* azul intenso */
  margin-bottom: 0.2rem;
}

.precio-original {
  font-size: 0.9rem;
  color: #9ca3af;
  text-decoration: line-through;
  margin-bottom: 0.2rem;
}

.precio-descuento {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1d4ed8;
  margin-bottom: 0.3rem;
}


.cardProducto .categoria {
  font-size: 0.9rem;
  color: #999;
}

.btn-fav {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  /* ✅ */
  font-size: 1.3rem;
  z-index: 10;
  color: red;
  transition: transform 0.2s ease, color 0.2s ease;
}

.btn-fav:hover {
  transform: scale(1.1);
  color: var(--main-color);
}

.fas.fa-heart {
  color: red;
  animation: latido 0.3s ease;
}

.llevateloYa {
  background: linear-gradient(135deg, #e6f4ec, #d9f7ee);
  border: none;
  border-radius: 1.5rem;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  position: relative;
}

.llevateloYa h2 {
  font-size: 1.7rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2rem;
  color: #088f63;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 1px #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.llevateloYa h2::after {
  content: '';
  flex: 1;
  height: 2px;
  background: #b2e2c5;
  margin-left: 1rem;
}

.llevateloYa .cardProducto {
  padding: 1.2rem;
  border-radius: 1.2rem;
  border: 1px solid #c8e7db;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background-color: #fff;
  position: relative;
}

.llevateloYa .cardProducto:hover {
  transform: scale(1.015);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
}

.llevateloYa .badge-descuento {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background-color: #16a34a;
  color: #fff;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 2;
}


.btn-vaciar {
  background: #ffecec;
  color: #d9534f;
  border: 1px solid #f5c6cb;
  padding: 0.5rem 1rem;
  font-weight: bold;
  border-radius: 0.8rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-vaciar:hover {
  background: #f8d7da;
}

.mensaje-vacio {
  text-align: center;
  font-size: 1.1rem;
  font-weight: 500;
  color: #999;
  margin-top: 1rem;
}

.btn-vaciar {
  display: block;
  margin: 1rem auto 2rem;
  padding: 0.75rem 1.5rem;
  background-color: #fee2e2;
  border: 1px solid #fca5a5;
  color: #b91c1c;
  font-weight: bold;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-vaciar:hover {
  background-color: #fecaca;
}

</style>
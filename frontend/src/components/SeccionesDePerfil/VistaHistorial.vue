<template>
  <div class="vista-historial">
    <h1 class="titulo">
      <i class="fas fa-receipt me-2"></i> Historial de Compras
    </h1>

    <div v-if="historial.length === 0" class="mensaje-vacio">
      No hay compras registradas.
    </div>

    <div v-else class="lista-compras">
      <div v-for="item in historial" :key="item.id" class="item-compra">
        <img :src="item.imagen" alt="Producto" class="thumb" />
        <div class="info">
          <h4>{{ item.nombre }}</h4>
          <p>{{ formatFecha(item.fecha) }} • {{ formatPrecio(item.precio) }}</p>
        </div>
        <span :class="`estado ${item.estado.toLowerCase()}`">{{ item.estado }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAuth } from 'firebase/auth'
import { getFirestore, collection, query, where, getDocs } from 'firebase/firestore'

const historial = ref([])
const auth = getAuth()
const db = getFirestore()

onMounted(async () => {
  const user = auth.currentUser
  if (!user) return console.warn('⚠️ Usuario no autenticado')

  try {
    const q = query(
      collection(db, 'compras'),
      where('usuarioId', '==', user.uid)
    )
    const querySnapshot = await getDocs(q)
    historial.value = querySnapshot.docs.map(doc => {
      const data = doc.data()
      return {
        id: doc.id,
        nombre: data.producto?.nombre || 'Producto',
        imagen: data.producto?.imagen || '',
        fecha: data.fecha?.toDate() || new Date(),
        precio: data.producto?.total || 0,
        estado: data.estado || 'pendiente'
      }
    })
  } catch (error) {
    console.error('❌ Error al obtener historial:', error)
  }
})

const formatPrecio = (valor) => {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(valor)
}

const formatFecha = (fecha) => {
  return fecha.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}
</script>


<style scoped>
.vista-historial {
  padding: 2rem;
}

.titulo {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.lista-compras {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.item-compra {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  gap: 1rem;
  flex-wrap: wrap;
}

.thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.info {
  flex-grow: 1;
  min-width: 150px;
}

.info h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.estado {
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.85rem;
  padding: 4px 10px;
  border-radius: 8px;
  white-space: nowrap;
}

.estado.pagado {
  color: #198754;
  background-color: #d1e7dd;
}

.estado.pendiente {
  color: #ffc107;
  background-color: #fff3cd;
}

.estado.cancelado {
  color: #dc3545;
  background-color: #f8d7da;
}

.mensaje-vacio {
  color: #888;
  font-style: italic;
  text-align: center;
  margin-top: 2rem;
}

/* 📱 Mobile: se apila todo */
@media (max-width: 600px) {
  .item-compra {
    flex-direction: column;
    align-items: flex-start;
  }

  .thumb {
    width: 100%;
    max-width: 100px;
    margin-bottom: 0.5rem;
  }

  .info {
    width: 100%;
  }

  .estado {
    align-self: flex-end;
    margin-top: 0.5rem;
  }
}

</style>

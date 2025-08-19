<template>
  <div>
    <div v-if="cargando" class="text-center py-5">
      <div class="spinner-border text-warning" role="status"></div>
    </div>

    <div v-else class="tabla-wrapper">
      <table class="tabla-admin">
        <thead>
          <tr>
            <th>Email</th>
            <th>Producto</th>
            <th>Cant.</th>
            <th>Dirección</th>
            <th>Fecha</th>
            <th>Total</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pedido in pedidos" :key="pedido.id">
            <td>{{ pedido.email }}</td>
            <td class="producto-cell">
              <img :src="pedido.producto.imagen" alt="Producto" />
              <span>{{ pedido.producto.nombre }}</span>
            </td>
            <td>{{ pedido.producto.cantidad }}</td>
            <td>
              {{ pedido.direccion?.calle }} {{ pedido.direccion?.numero }},
              {{ pedido.direccion?.ciudad }}, {{ pedido.direccion?.provincia }}
            </td>
            <td>{{ formatoFecha(pedido.fecha) }}</td>
            <td class="precio">
              {{ formatoMoneda(
                pedido.total ?? (pedido.producto.precio_unitario * pedido.producto.cantidad)
              ) }}
            </td>
            <td>
              <select :value="pedido.estado" @change="actualizarEstado(pedido.id, $event.target.value)" class="select-estado">
                <option value="pendiente">Pendiente</option>
                <option value="en camino">En camino</option>
                <option value="entregado">Entregado</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="pedidos.length === 0" class="text-center py-4 text-muted">
        No hay pedidos activos.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { collection, getDocs, orderBy, query, doc, updateDoc, getDoc, setDoc, deleteDoc } from 'firebase/firestore'
import { db } from '../../firebase'

const pedidos = ref([])
const cargando = ref(true)
const emit = defineEmits(['pedidoEntregado'])

const cargarPedidos = async () => {
  cargando.value = true
  try {
    const q = query(collection(db, 'compras'), orderBy('fecha', 'desc'))
    const querySnapshot = await getDocs(q)
    pedidos.value = querySnapshot.docs
      .map(doc => ({ id: doc.id, ...doc.data() }))
      .filter(p => p.estado !== 'entregado') // Solo activos
  } catch (error) {
    console.error('Error al cargar pedidos activos:', error)
  } finally {
    cargando.value = false
  }
}

const moverAPedidosEntregados = async (pedidoId) => {
  const ref = doc(db, 'compras', pedidoId)
  const snap = await getDoc(ref)
  if (!snap.exists()) return

  await setDoc(doc(db, 'compras_entregadas', pedidoId), snap.data())
  await deleteDoc(ref)
}

const actualizarEstado = async (pedidoId, nuevoEstado) => {
  if (nuevoEstado === 'entregado') {
    await moverAPedidosEntregados(pedidoId)
    emit('pedidoEntregado') // Avisar al padre que recargue entregados
  } else {
    await updateDoc(doc(db, 'compras', pedidoId), { estado: nuevoEstado })
  }
  await cargarPedidos()
}

const formatoFecha = (fecha) => {
  try {
    return fecha?.toDate().toLocaleString('es-AR', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    }) || '-'
  } catch {
    return '-'
  }
}

const formatoMoneda = (valor) => {
  const numero = Number(valor)
  if (isNaN(numero)) return '-'
  return numero.toLocaleString('es-AR', { style: 'currency', currency: 'ARS' })
}

onMounted(cargarPedidos)
</script>

<style>
/* 📦 Contenedor tabla */
.tabla-wrapper {
  flex: 1;
  overflow-x: auto;
}

/* 📋 Tabla */
.tabla-admin {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.tabla-admin thead {
  background: linear-gradient(
    90deg,
    var(--colorTerciario),
    var(--colorTerciarioHover)
  );
  color: var(--colorTextoPrincipal);
}

.tabla-admin th,
.tabla-admin td {
  padding: 0.8rem;
  text-align: left;
}

.tabla-admin tbody tr {
  border-bottom: 1px solid rgba(255, 193, 7, 0.2); /* Se puede adaptar a rgba de var */
  transition: 0.2s;
}

.tabla-admin tbody tr:hover {
  background-color: rgba(255, 193, 7, 0.08); /* Hover sutil */
  transform: scale(1.002);
}

/* 🖼 Producto */
.producto-cell {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.producto-cell img {
  width: 50px;
  height: auto;
  border-radius: 0.4rem;
  border: 1px solid var(--colorTerciario);
  transition: transform 0.2s;
}

.producto-cell img:hover {
  transform: scale(1.08);
}

/* 💲 Precio */
.precio {
  font-weight: bold;
  color: var(--colorExito);
}

/* 🎛 Select estado */
.select-estado {
  background: var(--colorFondoSecundario);
  color: var(--colorTextoSecundario);
  border: 1px solid var(--colorTerciario);
  padding: 0.4rem 0.8rem;
  border-radius: 0.4rem;
  transition: 0.2s;
}

.select-estado:hover {
  border-color: var(--colorTerciarioHover);
  box-shadow: 0 0 6px var(--colorTerciario);
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .tabla-admin th,
  .tabla-admin td {
    font-size: 0.85rem;
  }
}

</style>
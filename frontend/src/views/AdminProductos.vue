<template>

  <SpinnerCarga ref="spinnerRef" mensaje="Cargando productos de la tienda..." />

  <div class="admin-productos">
    <h1 class="tituloPrincipal">
      <i class="fas fa-box-open icono-blanco me-2"></i>
      <span class="texto-dorado">Administrar Productos</span>
    </h1>

    <div class="tabla-wrapper">
      <table class="tabla-productos">
        <thead>
          <tr>
            <th>Imagen</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="producto in productos" :key="producto.id">
            <td data-label="Imagen">
              <img :src="producto.imagenCarrusel?.[0] || producto.imagen || '/img/no-image.png'" @error="onImgError"
                alt="imagen" class="img-mini" />
            </td>
            <td data-label="Nombre">{{ producto.nombre }}</td>
            <td data-label="Precio">{{ formatPrice(obtenerPrecioFinal(producto)) }}</td>
            <td data-label="Stock">{{ producto.stockDisponible }}</td>
            <td class="acciones-centradas" data-label="Acciones">
              <button class="btn-action editar" @click="editar(producto)">
                <i class="fa-solid fa-pen"></i>
              </button>
              <button class="btn-action eliminar" @click="eliminar(producto.id)">
                <i class="fa-solid fa-trash"></i>
              </button>
              <button class="btn-action ver" @click="verProducto(producto)">
                <i class="fa-solid fa-eye"></i>
              </button>
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  </div>

  <VistaPreviaProducto v-if="productoParaVistaPrevia" :producto="productoParaVistaPrevia" :modoPreview="true"
    @cerrar="productoParaVistaPrevia = null" />

  <ModalConfirmacion ref="modalConfirmacion" :mensaje="mensajeConfirmacion" :colorBoton="'btn-danger'"
    @confirmar="confirmarEliminar" />

  <ModalEditarProducto ref="modalEditarProductoRef" :producto="productoSeleccionado" @guardar="guardarEdicion" />


  <Notificacion ref="notificacionRef" />

  <router-link to="/add-product" class="btn-flotante-agregar" title="Agregar producto">
    <i class="fas fa-plus"></i>
  </router-link>


</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'
import Notificacion from '../components/ToastNotificacion.vue'
import ModalEditarProducto from '../components/Modals/ModalEditarProducto.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'
import VistaPreviaProducto from '../components/VistaPreviaProducto.vue'


// 📦 Estado
const productos = ref([])
const productoAEliminar = ref(null)
const productoEditando = ref(null)
const modalConfirmacion = ref(null)
const mensajeConfirmacion = ref('')
const notificacionRef = ref(null)
const modalEditarProductoRef = ref(null)
const productoSeleccionado = ref(null)
const cargando = ref(true)
const spinnerRef = ref(null)
const productoParaVistaPrevia = ref(null) // 👁 Producto seleccionado para vista previa
const modalVistaPreviaRef = ref(null)

const props = defineProps({
  producto: Object
})


// 🎉 Notificaciones
function mostrarNoti({ titulo = 'Éxito', mensaje = '', tipo = 'success' }) {
  notificacionRef.value?.mostrar(titulo, mensaje, tipo)
}

// 🚀 Cargar productos
onMounted(async () => {
  spinnerRef.value?.mostrar()
  try {
    const res = await axios.get('http://localhost:5000/api/products')
    productos.value = res.data
  } catch (err) {
    console.error('Error cargando productos:', err)
  } finally {
    spinnerRef.value?.ocultar()
  }
})

function verProducto(producto) {
  productoParaVistaPrevia.value = producto

  nextTick(() => {
    const modalDOM = modalVistaPreviaRef.value
    if (modalDOM) {
      const modalInstance = bootstrap.Modal.getOrCreateInstance(modalDOM)
      modalInstance.show()
    }
  })
}

// 🗑️ Confirmar eliminación
function eliminar(id) {
  const prod = productos.value.find(p => p.id === id)
  productoAEliminar.value = prod
  mensajeConfirmacion.value = `¿Querés eliminar el producto "${prod.nombre}"?`
  modalConfirmacion.value.abrir()
}

async function confirmarEliminar() {
  const id = productoAEliminar.value.id
  try {
    await axios.delete(`http://localhost:5000/api/product/${id}`)
    productos.value = productos.value.filter(p => p.id !== id)

    mostrarNoti({ titulo: 'Producto eliminado', mensaje: '', tipo: 'success' })
  } catch (err) {
    mostrarNoti({
      titulo: 'Error al eliminar',
      mensaje: 'No se pudo eliminar el producto.',
      tipo: 'error'
    })
  }
}

function obtenerPrecioFinal(producto) {
  if (producto.descuento) {
    if (producto.tipoDescuento === 'porcentaje') {
      return producto.precio - (producto.precio * (producto.porcentajeDescuento || 0) / 100)
    } else if (producto.tipoDescuento === 'monto') {
      return producto.precio - (producto.montoDescuento || 0)
    }
  }
  return producto.precio
}


// ✏️ Edición
const editar = (producto) => {
  productoSeleccionado.value = {
    ...producto,
    imagenCarrusel: producto.imagenCarrusel || []
  }
  modalEditarProductoRef.value?.abrir() // 👈 asegurate que esto esté así
}


async function confirmarEdicion() {
  try {
    const { id, nombre, precio, stockDisponible } = productoEditando.value
    await axios.put(`http://localhost:5000/api/product/${id}`, { nombre, precio, stockDisponible })

    const index = productos.value.findIndex(p => p.id === id)
    if (index !== -1) {
      productos.value[index] = { ...productos.value[index], nombre, precio, stockDisponible }
    }

    modalEditarInstance?.hide()
    mostrarNoti({ titulo: '✅ Producto actualizado', mensaje: '', tipo: 'success' })
  } catch (err) {
    mostrarNoti({ titulo: 'Error al editar', mensaje: 'No se pudo guardar los cambios.', tipo: 'error' })
  }
}

// 🖼️ Imagen fallback
function onImgError(event) {
  event.target.src = '/img/no-image.png'
}

// 💸 Formato precio AR
function formatPrice(value) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(value || 0)
}

// 🖼️ Imagenes del carrusel
const fileInputsCarrusel = ref([])

function abrirInputCarrusel(index) {
  const input = fileInputsCarrusel.value[index]
  if (input) input.click()
}

function handleImagenPortada(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = e => {
      productoEditando.value.imagen = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function handleImagenCarrusel(event, index) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = e => {
      productoEditando.value.imagenCarrusel[index] = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

async function guardarEdicion(productoEditado) {
  try {
    // Actualizá en el backend
    await axios.put(`http://localhost:5000/api/product/${productoEditado.id}`, productoEditado)

    // Reemplazá el producto actualizado en el array local
    const index = productos.value.findIndex(p => p.id === productoEditado.id)
    if (index !== -1) {
      productos.value[index] = { ...productoEditado }
    }

    // Cerrá el modal
    modalEditarProductoRef.value?.cerrar()

    // Mostrá notificación
    mostrarNoti({ titulo: '✅ Producto actualizado', mensaje: '', tipo: 'success' })
  } catch (err) {
    console.error('Error al guardar edición:', err)
    mostrarNoti({
      titulo: '❌ Error al editar',
      mensaje: 'No se pudo guardar los cambios.',
      tipo: 'error'
    })
  }
}
</script>




<style scoped>
.admin-productos {
  background-color: #0f0f0f;
  color: #f1f1f1;
  min-height: 100vh;
  padding: 2rem;
}

.tituloPrincipal {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #ffc107;
  text-shadow: 0 1px 5px rgba(255, 193, 7, 0.3);
}

.icono-blanco {
  color: white;
}

/* ====================
   📊 TABLA DE PRODUCTOS
==================== */
.tabla-wrapper {
  overflow-x: auto;
  border-radius: 1rem;
  background: #1c1c1c;
  box-shadow: 0 0 20px rgba(255, 193, 7, 0.1);
  padding: 1rem;
}

.tabla-productos {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 0.8rem;
}

th {
  background-color: transparent;
  color: #ffc107;
  font-weight: 700;
  text-align: left;
  padding: 0.8rem 1rem;
  font-size: 0.9rem;
  border-bottom: 1px solid #333;
}

td {
  background: #151515;
  padding: 1rem;
  border-radius: 0.5rem;
  vertical-align: middle;
  font-size: 0.95rem;
  color: #f1f1f1;
  border: 1px solid #222;
  transition: background 0.3s ease;
}

tr:hover td {
  background-color: #222;
}

.img-mini {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 0.75rem;
  border: 2px solid #444;
}

/* ====================
   🎯 BOTONES DE ACCIÓN
==================== */
.acciones-centradas {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 100px;
  gap: 0.5rem;
}



.btn-action {
  background: #2a2a2a;
  color: #ffc107;
  border: 1px solid #444;
  font-size: 1rem;
  padding: 0.4rem 0.6rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-action:hover {
  background-color: #333;
}

.btn-action.editar {
  color: #0d6efd;
}

.btn-action.editar:hover {
  background-color: rgba(13, 110, 253, 0.1);
}

.btn-action.eliminar {
  color: #dc3545;
}

.btn-action.eliminar:hover {
  background-color: rgba(220, 53, 69, 0.1);
}

.btn-flotante-agregar {
  position: fixed;
  bottom: 1rem;
  right: 0.6rem;
  background-color: #ffc107;
  color: #0f0f0f;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.8rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  z-index: 999;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, background-color 0.2s;
  text-decoration: none;
}

.btn-flotante-agregar:hover {
  transform: scale(1.1);
  background-color: #e6b000;
  color: #000;
}


@media (max-width: 768px) {
  .tabla-productos thead {
    display: none;
  }

  .tabla-productos,
  .tabla-productos tbody,
  .tabla-productos tr,
  .tabla-productos td {
    display: block;
    width: 100%;
  }

  .tabla-productos tr {
    margin-bottom: 1.5rem;
    border: 1px solid #333;
    border-radius: 0.75rem;
    padding: 1rem;
    background-color: #1a1a1a;
  }

  .tabla-productos td {
    padding: 0.5rem 0;
    border: none;
    border-bottom: 1px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .tabla-productos td::before {
    content: attr(data-label);
    font-weight: bold;
    color: #ffc107;
    flex-shrink: 0;
    margin-right: 1rem;
    text-transform: uppercase;
    font-size: 0.75rem;
  }

  .acciones-centradas {
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .btn-flotante-agregar {
    position: fixed;
    bottom: 2rem;
    right: 0.4rem;
    background-color: #ffc107;
    color: #000;
    border-radius: 50%;
    width: 46px;
    height: 46px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.8rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    z-index: 999;
    text-decoration: none;
    transition: transform 0.2s ease-in-out;
  }

  .btn-flotante-agregar:hover {
    background-color: #e0aa00;
    transform: scale(1.1);
  }
}
</style>

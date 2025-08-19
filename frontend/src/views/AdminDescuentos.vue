<template>
  <div class="admin-descuentos">
    <div class="contenido container py-5">
      <h1 class="titulo mb-4">
        <i class="fa-solid fa-tags me-2 icono-titulo"></i>
        Panel de Descuentos
      </h1>

      <!-- Sección de productos con descuento -->
      <section class="seccion-glass mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h2 class="subtitulo">🍭 Productos con Descuento</h2>
          <i class="fa-solid fa-tags me-2 icono-titulo" title="Descuentos activos"></i>
        </div>
        <p class="descripcion">Editá o eliminá los descuentos activos en productos y sus modelos.</p>

        <div v-if="productosConDescuento.length === 0" class="placeholder text-center text-white-50 py-5">
          <i class="fa-solid fa-circle-info me-2"></i>
          No hay descuentos activos por el momento.
        </div>

        <div v-else class="row g-4">
          <div v-for="producto in productosConDescuento" :key="producto.id" class="col-md-6 col-lg-4">
            <div class="card bg-dark text-white h-100 shadow-lg">
              <img :src="producto.imagen || producto.imagenCarrusel?.[0]"
                   class="card-img-top object-fit-contain p-3 rounded-4"
                   style="height: 200px;" alt="Imagen producto" />
              <div class="card-body">
                <h5 class="card-title">{{ producto.nombre }}</h5>
                <span v-if="modeloTieneDescuento(producto) && !producto.descuento" class="badge bg-success mb-2">
                  <i class="fas fa-tag me-1"></i> Modelo con descuento
                </span>
                <p class="text-white-50 small mb-1">{{ producto.marca || 'Sin marca' }}</p>
                <p class="card-text">Precio: ${{ producto.precio.toLocaleString() }}</p>
                <p class="card-text">
                  Descuento:
                  <span v-if="producto.descuento">
                    {{ producto.porcentajeDescuento }}%
                    <br />
                    <small :class="[
                      'd-block',
                      mostrarFechaVencimientoAmarilla(producto.fechaYHoraVencimiento)
                        ? 'text-warning fw-bold'
                        : 'text-white-50'
                    ]">
                      <i class="fas fa-clock me-1"></i>
                      Vence: {{ formatFechaHora(producto.fechaYHoraVencimiento) || 'Indefinido' }}
                    </small>
                  </span>
                  <span v-else class="text-white-50">No</span>
                </p>
                <button class="btn btn-outline-warning w-100 mt-2" @click="abrirModal(producto)">
                  Editar descuento
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <hr class="separador" />

      <!-- Sección para agregar nuevos descuentos -->
      <section class="seccion-glass">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h2 class="subtitulo">➕ Agregar Descuento</h2>
          <i class="fa-solid fa-percent text-white-50 fs-3"></i>
        </div>
        <p class="descripcion">Seleccioná un producto y aplicá un descuento fijo o porcentual.</p>

        <div v-if="productosSinDescuento.length === 0" class="placeholder text-center text-white-50 py-5">
          <i class="fa-solid fa-circle-info me-2"></i>
          Todos los productos tienen descuentos activos.
        </div>

        <div v-else class="row g-4">
          <div v-for="producto in productosSinDescuento" :key="producto.id" class="col-md-6 col-lg-4">
            <div class="card bg-dark text-white h-100 shadow-lg">
              <img :src="producto.imagen || producto.imagenCarrusel?.[0]"
                   class="card-img-top object-fit-contain p-3 rounded-4"
                   style="height: 200px;" alt="Imagen producto" />
              <div class="card-body">
                <h5 class="card-title">{{ producto.nombre }}</h5>
                <p class="text-white-50 small mb-1">{{ producto.marca || 'Sin marca' }}</p>
                <p class="card-text">Precio: ${{ producto.precio.toLocaleString() }}</p>
                <button class="btn btn-outline-success w-100 mt-2" @click="abrirModal(producto)">
                  Agregar descuento
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>

  <ModalEditarDescuento
    :producto="productoEditado"
    ref="modalEditar"
    @guardar="guardarCambios"
    @solicitar-confirmacion="abrirModalConfirmacion"
  />

  <ModalConfirmacion
    ref="modalConfirmacionRef"
    :mensaje="mensajeConfirmacion"
    colorBoton="btn-warning"
    @confirmar="eliminarDescuento"
  />

  <SpinnerCarga ref="refSpinner" mensaje="Cargando productos..." />
  <ToastNotificaciones ref="toastRef" />
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'

import ModalEditarDescuento from '../components/Modals/ModalEditarDescuento.vue'
import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'
import ToastNotificaciones from '../components/ToastNotificacion.vue'

const productosConDescuento = ref([])
const productosSinDescuento = ref([])
const productoEditado = ref({})

const modalEditar = ref(null)
const refSpinner = ref(null)
const refToast = ref(null)
const modalConfirmacionRef = ref(null)

const mensajeConfirmacion = ref('')

const obtenerProductosConDescuento = async () => {
  try {
    refSpinner.value?.mostrar()
    const { data } = await axios.get('http://localhost:5000/api/products')
    const ahora = new Date()

    const tieneDescuentoProducto = (prod) => {
      const vencimiento = prod.fechaYHoraVencimiento ? new Date(prod.fechaYHoraVencimiento) : null
      return (
        prod.descuento &&
        ((prod.porcentajeDescuento ?? 0) > 0 || (prod.montoDescuento ?? 0) > 0) &&
        (!vencimiento || vencimiento > ahora)
      )
    }

    const tieneModelosConDescuento = (prod) => {
      if (!Array.isArray(prod.modelos)) return false
      return prod.modelos.some(m =>
        m.descuento &&
        ((m.porcentajeDescuento ?? 0) > 0 || (m.montoDescuento ?? 0) > 0) &&
        m.fechaYHoraVencimiento &&
        new Date(m.fechaYHoraVencimiento) > ahora
      )
    }

    const noTieneDescuentoNiModelos = (prod) => {
      const vencimiento = prod.fechaYHoraVencimiento ? new Date(prod.fechaYHoraVencimiento) : null
      const productoSinDescuento =
        !prod.descuento ||
        ((prod.porcentajeDescuento ?? 0) <= 0 && (prod.montoDescuento ?? 0) <= 0) ||
        (vencimiento && vencimiento <= ahora)

      const modelosSinDescuento = Array.isArray(prod.modelos)
        ? prod.modelos.every(m =>
            !m.descuento ||
            ((m.porcentajeDescuento ?? 0) <= 0 && (m.montoDescuento ?? 0) <= 0) ||
            !m.fechaYHoraVencimiento ||
            new Date(m.fechaYHoraVencimiento) <= ahora
          )
        : true

      return productoSinDescuento && modelosSinDescuento
    }

    productosConDescuento.value = data.filter(prod =>
      tieneDescuentoProducto(prod) || tieneModelosConDescuento(prod)
    )

    productosSinDescuento.value = data.filter(prod =>
      noTieneDescuentoNiModelos(prod)
    )
  } catch (err) {
    console.error('❌ Error al cargar productos:', err)
    refToast.value?.mostrar('Error', 'Hubo un problema al cargar los productos', 'error')
  } finally {
    refSpinner.value?.ocultar()
  }
}


const abrirModal = (producto) => {
  productoEditado.value = {
    ...producto,
    descuentoOriginal: producto.descuento
  }
  nextTick(() => {
    modalEditar.value?.show()
  })
}

const abrirModalConfirmacion = () => {
  modalEditar.value?.hide()
  mensajeConfirmacion.value = '¿Eliminar descuento de este producto?'
  nextTick(() => {
    modalConfirmacionRef.value?.abrir()
  })
}

const guardarCambios = async () => {
  try {
    const prod = productoEditado.value
    const antesTeniaDescuento = prod.descuentoOriginal
    const ahoraTieneDescuento = prod.descuento

    if (prod.descuento) {
      if (prod.tipoDescuento === 'porcentaje' && (!prod.porcentajeDescuento || prod.porcentajeDescuento === 0)) {
        refToast.value?.mostrar('Advertencia', 'Tenés que ingresar un porcentaje mayor a 0', 'info')
        return
      }
      if (prod.tipoDescuento === 'monto' && (!prod.montoDescuento || prod.montoDescuento === 0)) {
        refToast.value?.mostrar('Advertencia', 'Tenés que ingresar un monto mayor a 0', 'info')
        return
      }
    } else {
      prod.porcentajeDescuento = 0
      prod.montoDescuento = 0
      prod.tipoDescuento = null
      prod.fechaYHoraVencimiento = null
    }

    if (Array.isArray(prod.modelos)) {
      prod.modelos = prod.modelos.map(modelo => {
        if (modelo.descuento) {
          const tienePorcentaje = modelo.tipoDescuento === 'porcentaje' && modelo.porcentajeDescuento > 0
          const tieneMonto = modelo.tipoDescuento === 'monto' && modelo.montoDescuento > 0
          if (!tienePorcentaje && !tieneMonto) {
            modelo.descuento = false
          }
        } else {
          modelo.tipoDescuento = ''
          modelo.porcentajeDescuento = 0
          modelo.montoDescuento = 0
          modelo.fechaYHoraVencimiento = null
        }
        return modelo
      })
    }

    await axios.put(`http://localhost:5000/api/product/${prod.id}`, prod)

    if (!antesTeniaDescuento && ahoraTieneDescuento) {
      refToast.value?.mostrar('✅ Descuento agregado', 'Se agregó un nuevo descuento', 'success')
    } else {
      refToast.value?.mostrar('✅ Actualizado', 'Producto actualizado correctamente', 'success')
    }

    modalEditar.value?.hide()

    const productoActualizado = { ...productoEditado.value }

    productosConDescuento.value = productosConDescuento.value.filter(p => p.id !== productoActualizado.id)
    productosSinDescuento.value = productosSinDescuento.value.filter(p => p.id !== productoActualizado.id)

    const ahora = new Date()
    const vencimiento = productoActualizado.fechaYHoraVencimiento
      ? new Date(productoActualizado.fechaYHoraVencimiento)
      : null

    const tieneDescuentoProducto =
      productoActualizado.descuento &&
      ((productoActualizado.porcentajeDescuento ?? 0) > 0 ||
        (productoActualizado.montoDescuento ?? 0) > 0) &&
      (!vencimiento || vencimiento > ahora)

    const tieneModelosConDescuento = Array.isArray(productoActualizado.modelos)
      ? productoActualizado.modelos.some(m =>
          m.descuento &&
          ((m.porcentajeDescuento ?? 0) > 0 || (m.montoDescuento ?? 0) > 0) &&
          m.fechaYHoraVencimiento &&
          new Date(m.fechaYHoraVencimiento) > ahora
        )
      : false

    if (tieneDescuentoProducto || tieneModelosConDescuento) {
      productosConDescuento.value.push(productoActualizado)
    } else {
      productosSinDescuento.value.push(productoActualizado)
    }

  } catch (err) {
    console.error('❌ Error al guardar cambios:', err)
    refToast.value?.mostrar('Error', 'Hubo un error al guardar los cambios', 'error')
  }
}

const eliminarDescuento = async () => {
  productoEditado.value.descuento = false
  productoEditado.value.tipoDescuento = null
  productoEditado.value.porcentajeDescuento = 0
  productoEditado.value.montoDescuento = 0
  productoEditado.value.fechaYHoraVencimiento = null
  await guardarCambios()
}

onMounted(async () => {
  await axios.post('http://localhost:5000/api/desactivar-descuentos-vencidos')
  await obtenerProductosConDescuento()
})

setInterval(async () => {
  await axios.post('http://localhost:5000/api/desactivar-descuentos-vencidos')
  await obtenerProductosConDescuento()
}, 60000)

const formatInput = (event, campo) => {
  const valor = Number(event.target.value.replace(/\D/g, ''))
  productoEditado.value[campo] = valor
}

const formatNumber = (valor) => {
  if (!valor && valor !== 0) return ''
  return valor.toLocaleString('es-AR')
}

const formattedPrecio = computed(() => formatNumber(productoEditado.value.precio))
const formattedMontoDescuento = computed(() => formatNumber(productoEditado.value.montoDescuento))

const precioConDescuento = computed(() => {
  if (!productoEditado.value.descuento || !productoEditado.value.precio) {
    return formatNumber(productoEditado.value.precio)
  }
  let precio = productoEditado.value.precio
  if (productoEditado.value.tipoDescuento === 'porcentaje') {
    precio -= (precio * (productoEditado.value.porcentajeDescuento || 0)) / 100
  } else {
    precio -= productoEditado.value.montoDescuento || 0
  }
  return formatNumber(Math.max(0, precio))
})

const formatFechaHora = (fechaISO) => {
  if (!fechaISO) return null
  const fecha = new Date(fechaISO)
  return fecha.toLocaleString('es-AR', {
    dateStyle: 'short',
    timeStyle: 'short'
  })
}

const mostrarFechaVencimientoAmarilla = (fechaISO) => {
  if (!fechaISO) return false
  const hoy = new Date()
  const vencimiento = new Date(fechaISO)
  const diferenciaMs = vencimiento - hoy
  const diferenciaDias = diferenciaMs / (1000 * 60 * 60 * 24)
  return diferenciaDias <= 3 && diferenciaDias > 0
}

const modeloTieneDescuento = (producto) => {
  if (!producto.modelos || !Array.isArray(producto.modelos)) return false
  const ahora = new Date()
  return producto.modelos.some(m =>
    m.descuento === true &&
    ((m.porcentajeDescuento ?? 0) > 0 || (m.montoDescuento ?? 0) > 0) &&
    m.fechaYHoraVencimiento && new Date(m.fechaYHoraVencimiento) > ahora
  )
}
</script>

<style scoped>
.admin-descuentos {
  background: linear-gradient(135deg, #111, #1f1f1f);
  min-height: 100vh;
  color: white;
}

.titulo {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: var(--main-color, #00d1b2);
}

.subtitulo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
}

.descripcion {
  color: #bbb;
  margin-bottom: 1rem;
}

.seccion-glass {
  background: rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 1.5rem;
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.placeholder {
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 2rem;
  font-style: italic;
}

.card {
  display: flex;
  flex-direction: column;
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.modal-content {
  border-radius: 1rem;
  background: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.modal-title {
  font-weight: bold;
  font-size: 1.25rem;
  color: var(--main-color, #00d1b2);
}

.formularioCampo {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-label {
  font-weight: 500;
  color: #ccc;
}

input.form-control,
select.form-select {
  background-color: #2b2b2b;
  border: 1px solid #444;
  color: #fff;
  border-radius: 0.5rem;
}

input.form-control:focus,
select.form-select:focus {
  outline: none;
  border-color: var(--main-color, #ffffff);
  box-shadow: 0 0 0 0.15rem rgba(255, 255, 255, 0.25);
}

.titulo {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: var(--main-color, var(--colorTerciario));
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.icono-titulo {
  font-size: 2.2rem;
  color: var(--main-color, #ffffff);
  animation: rebote 1s infinite alternate;
}

.separador {
  border: none;
  border-top: 1px solid rgba(248, 245, 245, 0.411);
  margin: 3rem 0;
}
</style>
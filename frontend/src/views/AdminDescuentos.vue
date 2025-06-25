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
          <h2 class="subtitulo">🛍 Productos con Descuento</h2>
          <i class="fa-solid fa-tags me-2 icono-titulo" title="Descuentos activos"></i>

        </div>
        <p class="descripcion">Editá o eliminá los descuentos activos en productos y sus modelos.</p>

        <!-- Placeholder de productos con descuento -->
        <div v-if="productosConDescuento.length === 0" class="placeholder text-center text-white-50 py-5">
          <i class="fa-solid fa-circle-info me-2"></i>
          No hay descuentos activos por el momento.
        </div>

        <div v-else class="row g-4">
          <div v-for="producto in productosConDescuento" :key="producto.id" class="col-md-6 col-lg-4">
            <div class="card bg-dark text-white h-100 shadow-lg">
              <img :src="producto.imagen || producto.imagenCarrusel?.[0]"
                class="card-img-top object-fit-contain p-3 rounded-4" style="height: 200px;" alt="Imagen producto" />
              <div class="card-body">
                <h5 class="card-title">{{ producto.nombre }}</h5>
                <p class="text-white-50 small mb-1">{{ producto.marca || 'Sin marca' }}</p>

                <p class="card-text">Precio: ${{ producto.precio.toLocaleString() }}</p>
                <p class="card-text">
                  Descuento:
                  <span v-if="producto.descuento">
                    {{ producto.porcentajeDescuento }}%
                    <br />
                    <small class="text-white-50">
                      Vence:
                      {{ formatFechaHora(producto.fechaYHoraVencimiento) || 'Indefinido' }}
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

        <!-- Si no hay productos sin descuento -->
        <div v-if="productosSinDescuento.length === 0" class="placeholder text-center text-white-50 py-5">
          <i class="fa-solid fa-circle-info me-2"></i>
          Todos los productos tienen descuentos activos.
        </div>

        <!-- Lista de productos sin descuento -->
        <div v-else class="row g-4">
          <div v-for="producto in productosSinDescuento" :key="producto.id" class="col-md-6 col-lg-4">
            <div class="card bg-dark text-white h-100 shadow-lg">
              <img :src="producto.imagen || producto.imagenCarrusel?.[0]"
                class="card-img-top object-fit-contain p-3 rounded-4" style="height: 200px;" alt="Imagen producto" />
              <div class="card-body">
                <h5 class="card-title">{{ producto.nombre }}</h5>
                <p class="text-white-50 small mb-1">{{ producto.marca || 'Sin marca' }}</p>

                <p class="card-text">
                  Precio: ${{ producto.precio.toLocaleString() }}
                </p>
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


  <ModalEditarDescuento :producto="productoEditado" ref="modalEditar" @guardar="guardarCambios" />
  <SpinnerCarga ref="refSpinner" mensaje="Cargando productos..." />
  <ToastNotificaciones ref="toastRef" />


</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import ModalEditarDescuento from '../components/Modals/ModalEditarDescuento.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'
import ToastNotificaciones from '../components/ToastNotificacion.vue'

const productosConDescuento = ref([])
const productosSinDescuento = ref([])
const productoEditado = ref({})
const modalEditar = ref(null)
const refSpinner = ref(null)
const refToast = ref(null) // ✅ Notificaciones

// 🔁 Obtener productos y clasificarlos
const obtenerProductosConDescuento = async () => {
  try {
    refSpinner.value?.mostrar()
    const { data } = await axios.get('http://localhost:5000/api/products')
    const ahora = new Date()

    productosConDescuento.value = data.filter(prod => {
      const vencimiento = prod.fechaYHoraVencimiento ? new Date(prod.fechaYHoraVencimiento) : null

      const descuentoActivo = prod.descuento === true &&
        ((prod.porcentajeDescuento ?? 0) > 0 || (prod.montoDescuento ?? 0) > 0) &&
        vencimiento && vencimiento > ahora

      const modelosConDescuento = Array.isArray(prod.modelos)
        ? prod.modelos.some(m =>
          m.descuento === true &&
          ((m.porcentajeDescuento ?? 0) > 0 || (m.montoDescuento ?? 0) > 0) &&
          m.fechaYHoraVencimiento && new Date(m.fechaYHoraVencimiento) > ahora
        )
        : false

      return descuentoActivo || modelosConDescuento
    })

    productosSinDescuento.value = data.filter(prod => {
      const vencimiento = prod.fechaYHoraVencimiento ? new Date(prod.fechaYHoraVencimiento) : null

      const sinDescuento =
        (!prod.descuento || prod.descuento === false) ||
        ((prod.porcentajeDescuento ?? 0) <= 0 && (prod.montoDescuento ?? 0) <= 0) ||
        (vencimiento && vencimiento <= ahora)

      const modelosSinDescuento = Array.isArray(prod.modelos)
        ? prod.modelos.every(m =>
          !m.descuento ||
          ((m.porcentajeDescuento ?? 0) <= 0 && (m.montoDescuento ?? 0) <= 0) ||
          !m.fechaYHoraVencimiento || new Date(m.fechaYHoraVencimiento) <= ahora
        )
        : true

      return sinDescuento && modelosSinDescuento
    })

  } catch (err) {
    console.error('❌ Error al cargar productos:', err)
    refToast.value?.mostrar('Error', 'Hubo un problema al cargar los productos', 'error')
  } finally {
    refSpinner.value?.ocultar()
  }
}

// 🧩 Abrir modal
const abrirModal = (producto) => {
  productoEditado.value = {
    ...producto,
    descuentoOriginal: producto.descuento // 👈 Guardamos el estado anterior
  }
  nextTick(() => {
    modalEditar.value?.show()
  })
}

// 💾 Guardar cambios con validación y notificación
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

    await axios.put(`http://localhost:5000/api/product/${prod.id}`, prod)

    // ✅ Notificación según el tipo de cambio
    if (!antesTeniaDescuento && ahoraTieneDescuento) {
      refToast.value?.mostrar('✅ Descuento agregado', 'Se agregó un nuevo descuento', 'success')
    } else {
      refToast.value?.mostrar('✅ Actualizado', 'Producto actualizado correctamente', 'success')
    }

    modalEditar.value?.hide()
    await obtenerProductosConDescuento()
  } catch (err) {
    console.error('❌ Error al guardar cambios:', err)
    refToast.value?.mostrar('Error', 'Hubo un error al guardar los cambios', 'error')
  }
}

// 🚀 Inicialización
onMounted(async () => {
  await axios.post('http://localhost:5000/api/desactivar-descuentos-vencidos')
  await obtenerProductosConDescuento()
})

// 🔁 Intervalo automático cada 60s
setInterval(async () => {
  await axios.post('http://localhost:5000/api/desactivar-descuentos-vencidos')
  await obtenerProductosConDescuento()
}, 60000)

// 📦 Utilidades
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
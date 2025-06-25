<template>
  <div class="contenedorVistaPrevia">
    <!-- Producto -->
    <div class="cardProducto" :class="{ nuevo: product.nuevo }">
      <!-- Etiquetas -->
      <div v-if="product.etiquetas.length" class="contenedorEtiquetas">
        <span v-for="(etiqueta, index) in product.etiquetas" :key="index" class="etiqueta">
          {{ etiqueta }}
          <button class="btnEliminar" @click="eliminarEtiqueta(index)">
            <i class="fas fa-trash"></i>
          </button>
        </span>
      </div>

      <!-- Marca y categoría -->
      <div class="informacionProducto">
        <p><strong>{{ product.marca || "Logitech" }}</strong> | {{ product.categoria || "--" }}</p>
      </div>

      <!-- Nombre -->
      <h3 class="nombreProducto">{{ modeloEnVistaPrevia.nombre || product.nombre || "Nombre" }}</h3>

      <!-- Carrusel -->
      <div class="contador-carrusel">
        {{ currentSlideIndex }} / {{ imagenesCarruselModelo.length }}
      </div>
      <swiper :modules="[Navigation, Pagination]" :slides-per-view="1" :navigation="true"
        :pagination="{ clickable: true }" @slideChange="updateSlideIndex" class="swiper-container">
        <swiper-slide v-for="(img, index) in imagenesCarruselModelo || []" :key="index">
          <img v-if="img" :src="img" alt="Imagen del carrusel" class="carruselImagen" />
        </swiper-slide>
      </swiper>

      <!-- Precios -->
      <div class="contenedorPrecios">
        <div class="contenedorPrecioOriginal">
          <p v-if="modeloEnVistaPrevia.descuento" class="precioOriginal">{{ calcularPrecioSinDescuento() }}</p>
        </div>
        <div class="contenedorPrecioDescuento">
          <p class="precioDescuento">
            {{ calcularPrecioModelo() }}
            <span v-if="modeloEnVistaPrevia.descuento" class="badgeDescuento">
              <template v-if="modeloEnVistaPrevia.tipoDescuento === 'porcentaje'">
                {{ modeloEnVistaPrevia.porcentajeDescuento }}% OFF
              </template>
              <template v-else>
                - {{ formatNumber(modeloEnVistaPrevia.montoDescuento) }}
              </template>
            </span>

          </p>
        </div>
      </div>

      <!-- Vencimiento del descuento -->
      <div v-if="modeloEnVistaPrevia.descuento && descuentoActivo" :class="['vencimientoDescuento', claseVencimiento]">
        <i class="fas fa-clock iconoReloj"></i>
        <div class="contenidoVencimiento">
          <span class="textoVencimiento">
            Válido hasta:
            <strong>
              {{
                formatearFechaHora(
                  modeloEnVistaPrevia.fechaVencimientoDescuento || product.fechaVencimientoDescuento,
                  modeloEnVistaPrevia.horaVencimientoDescuento || product.horaVencimientoDescuento
              )
              }}
            </strong>


          </span>
        </div>
      </div>


      <!-- Color -->
      <p class="modeloColor"><strong>Colores:</strong> {{ modeloEnVistaPrevia.color || "Sin color" }}</p>

      <!-- Modelos -->
      <!-- Mostrar las cards si hay al menos un modelo (el base ya está incluido) -->
      <div class="cardsModeloGeneral" v-if="modelosUnificados.length > 0">
        <div class="cardsModelo">
          <div v-for="(modelo, index) in modelosUnificados" :key="index" class="cardModelo"
            :class="{ activo: modeloSeleccionado === index }" @click="seleccionarModelo(index)">
            <img :src="modelo.imagen" alt="Imagen del modelo" v-if="modelo.imagen" />
          </div>
        </div>
      </div>



      <!-- Botón consultar -->
      <div class="contenedorBotonInteractuar">
        <button class="btnConsultar">Consultar</button>
      </div>
    </div>

    <!-- Stock -->
    <div class="contenedorStock">
      <p>
        <strong>Stock Disponible:</strong>
        {{
          modeloEnVistaPrevia.stockDisponible !== undefined
            ? modeloEnVistaPrevia.stockDisponible > 0
              ? modeloEnVistaPrevia.stockDisponible
              : "Sin stock"
            : product.stockDisponible > 0
              ? product.stockDisponible
              : "Sin stock"
        }}
      </p>
    </div>

    <!-- Descripción -->
    <div class="contenedorDescripcion">
      <p class="descripcion">{{ product.descripcion || "Descripción del producto." }}</p>
    </div>

    <!-- Detalles técnicos -->
    <div v-for="(item, index) in product.detallesTecnicos" :key="index" class="vistaPreviaAcordeon">
      <div class="vistaPreviaHeader" @click="toggle(index)">
        <h5>{{ item.titulo }}</h5>
        <i :class="['fa-solid', 'fa-chevron-down', { rotarFlecha: item.abierto }]" class="iconoFlecha"></i>
      </div>
      <transition name="accordion">
        <div v-if="item.abierto" class="vistaPreviaBody">
          <ul>
            <li v-for="(detalle, i) in item.detalles" :key="i">
              <strong>{{ detalle.clave }}</strong>: {{ detalle.valor }}
            </li>
          </ul>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import { Navigation, Pagination } from 'swiper/modules'

// Props
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

// Estado
const modeloSeleccionado = ref(0)
const currentSlideIndex = ref(1)
const descuentoActivo = ref(true)
const claseVencimiento = ref('vencimientoOk')
let intervaloActualizacion = null
modeloSeleccionado.value = 0 // Forzar recomputación del modelo base

// Computed
const modelosUnificados = computed(() => {
  const base = {
    nombre: props.product.nombre,
    color: props.product.colorPrincipal,
    imagen: props.product.imagen,
    precio: props.product.precio,
    imagenCarrusel: props.product.imagenCarrusel || [],
    descuento: props.product.descuento,
    tipoDescuento: props.product.tipoDescuento,
    porcentajeDescuento: props.product.porcentajeDescuento,
    montoDescuento: props.product.montoDescuento,
    stockDisponible: props.product.stockDisponible,
  }

  const modelos = Array.isArray(props.product.modelos) ? props.product.modelos : []

  return [base, ...modelos]
})





const modeloEnVistaPrevia = computed(() => modelosUnificados.value[modeloSeleccionado.value] || {})

const imagenesCarruselModelo = computed(() => {
  const portada = modeloEnVistaPrevia.value?.imagen
  const carrusel = modeloEnVistaPrevia.value?.imagenCarrusel || []
  const imagenes = [portada, ...carrusel].filter(Boolean)

  // Eliminar duplicados (por si la portada está en el carrusel)
  return [...new Set(imagenes)]
})


// Métodos
function seleccionarModelo(index) {
  modeloSeleccionado.value = index
}

function updateSlideIndex(swiper) {
  currentSlideIndex.value = swiper.activeIndex + 1
}

function formatNumber(value) {
  return value
    ? new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
    : '$0'
}

function calcularPrecioModelo() {
  const modelo = modeloEnVistaPrevia.value
  if (!modelo?.precio) return formatNumber(props.product.precio)

  let precio = modelo.precio

  if (modelo.descuento) {
    if (modelo.tipoDescuento === 'porcentaje') {
      precio -= (precio * modelo.porcentajeDescuento) / 100
    } else if (modelo.tipoDescuento === 'monto') {
      precio -= modelo.montoDescuento
    }
  }

  return formatNumber(precio)
}

function calcularPrecioSinDescuento() {
  const modelo = modeloEnVistaPrevia.value
  const precioOriginal = modelo.precioOriginal || modelo.precio
  return formatNumber(precioOriginal)
}

function eliminarEtiqueta(index) {
  props.product.etiquetas.splice(index, 1)
}

function toggle(index) {
  props.product.detallesTecnicos[index].abierto =
    !props.product.detallesTecnicos[index].abierto
}

function formatearFechaHora(fecha, hora) {
  if (!fecha) return "Sin fecha definida";
  try {
    const partes = fecha.split("-");
    const fechaFormateada = `${partes[2]}/${partes[1]}/${partes[0]}`;
    return hora ? `${fechaFormateada} a las ${hora}` : fechaFormateada;
  } catch {
    return "Fecha inválida";
  }
}


// 🧠 Lógica de vencimiento y eliminación del descuento
async function actualizarEstadoDescuento() {
  const { descuento, fechaVencimientoDescuento, horaVencimientoDescuento } = props.product

  if (!descuento || !fechaVencimientoDescuento) {
    descuentoActivo.value = false
    return
  }

  const ahora = new Date()
  const vencimiento = new Date(`${fechaVencimientoDescuento}T${horaVencimientoDescuento || '23:59'}`)
  const minutosRestantes = (vencimiento - ahora) / 1000 / 60

  if (ahora > vencimiento) {
    props.product.descuento = false
    props.product.tipoDescuento = null
    props.product.porcentajeDescuento = 0
    props.product.montoDescuento = 0
    props.product.fechaVencimientoDescuento = null
    props.product.horaVencimientoDescuento = null

    localStorage.setItem(`producto-${props.product.id}`, JSON.stringify(props.product))
    modeloSeleccionado.value = 0

    try {
      await axios.put(`http://localhost:5000/api/products/${props.product.id}`, props.product)
      console.log("✅ Descuento eliminado automáticamente del backend")
    } catch (err) {
      console.error("❌ Error al eliminar el descuento:", err)
    }

    return
  }

  descuentoActivo.value = true
  claseVencimiento.value = minutosRestantes <= 60 ? 'vencimientoCercano' : 'vencimientoOk'
}

// 🚀 Guardar producto en localStorage al montar
onMounted(() => {
  actualizarEstadoDescuento()
  localStorage.setItem(`producto-${props.product.id}`, JSON.stringify(props.product))
  intervaloActualizacion = setInterval(actualizarEstadoDescuento, 10000) // cada 10s
})

// 🧹 Limpiar intervalo al desmontar
onBeforeUnmount(() => {
  clearInterval(intervaloActualizacion)
})

// Inicializar selección de modelo
seleccionarModelo(0)
</script>






<style scoped>
.contenedorVistaPrevia {
  flex: 1;
  overflow-y: auto;
  height: 95vh;
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: var(--fuentePrincipal);
}

.cardProducto {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px;
  width: 100%;
  max-width: 600px;
  min-height: 450px;
  font-family: var(--fuentePrincipal);
}

.contenedorEtiquetas {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-width: 100%;
  padding: 10px;
  justify-content: flex-start;
}

.etiqueta {
  background-color: var(--colorSecundario);
  color: white;
  font-size: 0.9rem;
  font-weight: bold;
  padding: 6px 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.informacionProducto {
  align-self: flex-start;
  font-size: 15px;
}

.nombreProducto {
  text-align: left;
  font-size: 1.3rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  width: 100%;
  max-width: 100%;
}

.swiper-container {
  width: 100%;
  max-width: 500px;
  height: 300px;
  border-radius: 10px;
  overflow: hidden;
}

.carruselImagen {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.contador-carrusel {
  position: relative;
  top: 10px;
  right: 225px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  z-index: 10;
}

.contenedorPrecios {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 30px;
  align-items: flex-start;
}

.precioOriginal {
  font-size: 1.1rem;
  text-decoration: line-through;
  text-align: left;
  width: 100%;
  white-space: normal;
  word-wrap: break-word;
}

.contenedorPrecioDescuento {
  display: flex;
  align-items: baseline;
  width: 100%;
}

.badgeDescuento {
  background-color: #e6f4ea;
  /* verde clarito */
  color: #1e8e3e;
  /* verde fuerte */
  font-size: 0.9rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  margin-left: 12px;
  display: inline-block;
  line-height: 1;
}


.precioDescuento {
  display: flex;
  text-align: left;
  margin-top: -20px;
  margin-left: 5px;
  font-size: 2rem;
  font-weight: 700;
  align-items: center;
}

.precioDescuento span {
  font-size: 1.2rem;
  color: var(--colorExito);
  margin-left: 8px;
  font-weight: normal;
}

.modeloColor {
  align-self: flex-start !important;
  text-align: left !important;
}

.cardsModeloGeneral {
  padding: 12px;
  max-height: 250px;
  overflow-y: auto;
}

.cardsModelo {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.cardModelo {
  width: 60px;
  height: 90px;
  border-radius: 20px;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 4px;
  transition: border 0.2s ease-in-out;
  cursor: pointer;
}

.cardModelo.activo {
  border: 2px solid #0050ff;
}

.cardModelo img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.contenedorBotonInteractuar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  width: 100%;
}

.btnConsultar {
  background-color: var(--colorPrincipal);
  padding: 20px;
  border-radius: 20px;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btnConsultar:hover {
  background-color: var(--colorPrincipalHover);
  color: var(--colorTextoSecundario);
  transform: scale(1.05);
}

.contenedorDescripcion {
  width: 100%;
  display: flex;
}

.descripcion {
  text-align: left;
  width: 100%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}

.vistaPreviaHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f7f7f7;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
}

.vistaPreviaHeader:hover {
  background: #ececec;
}

.iconoFlecha {
  transition: transform 0.3s ease;
  font-size: 1rem;
  color: #333;
}

.rotarFlecha {
  transform: rotate(180deg);
}

.vistaPreviaBody {
  padding: 1rem 1.5rem;
  background-color: #fafafa;
  animation: fadeInVistaPrevia 0.3s ease-in-out;
}

.vistaPreviaBody ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.vistaPreviaBody li {
  padding: 0.5rem 0;
  font-size: 0.95rem;
  border-bottom: 1px solid #eaeaea;
}

.vistaPreviaBody li:last-child {
  border-bottom: none;
}

.accordion-enter-active,
.accordion-leave-active {
  transition: max-height 0.3s ease, opacity 0.3s ease, padding 0.3s ease;
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  max-height: 0;
  opacity: 0;
  padding: 0 1.5rem;
}

.accordion-enter-to,
.accordion-leave-from {
  max-height: 500px;
  opacity: 1;
  padding: 1rem 1.5rem;
}

.vencimientoDescuento {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  margin-top: 2px;
  margin-bottom: 27px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  width: fit-content;
  border: 1px solid;
}

.vencimientoOk {
  background: #e6f4ea;
  border-color: #1e8e3e;
}

.vencimientoCercano {
  background: #fff8e1;
  border-color: #f4c430;
}

.oculto {
  display: none;
}
</style>

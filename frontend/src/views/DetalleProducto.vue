<template>
  <teleport to="body">
    <div class="noti-container" v-show="mostrarToast" aria-live="polite">
      <div :class="['noti-toast', toastTipo]">
        <i class="icono" :class="iconoToast"></i>
        <div class="contenido">
          <span class="titulo">Producto agregado al carrito</span>
          <p class="mensaje">Podés verlo en tu carrito</p>
          <span class="tiempo">Ahora</span>
        </div>
        <button class="btn-cerrar" @click="cerrarToast" aria-label="Cerrar notificación">&times;</button>
      </div>
    </div>
  </teleport>

  <div class="contenedorGeneral">
    <div v-if="producto" class="contenedor-producto">
      <!-- Columna izquierda: Carrusel Bootstrap -->
      <div class="columna izquierda">
        <div class="contenedor-imagenes">
          <!-- Miniaturas a la izquierda -->
          <div class="miniaturas-vertical">
            <img v-for="(img, index) in producto.imagenCarrusel" :key="'miniatura-' + index" :src="img"
              class="miniatura-vertical" alt="Miniatura" @click="seleccionarSlide(index)" />
          </div>

          <!-- Carrusel principal -->
          <div id="carouselProducto" class="carousel slide carrusel-principal" data-bs-ride="carousel">
            <div class="carousel-inner">
              <div v-for="(img, index) in producto.imagenCarrusel" :key="index"
                :class="['carousel-item', { active: index === 0 }]">
                <div class="contenedor-imagen">
                  <img :src="img" class="imagen-principal" alt="Imagen del producto" />
                </div>
              </div>
            </div>
            <!-- Flecha izquierda -->
            <button class="carousel-control-prev custom-flecha" type="button" data-bs-target="#carouselProducto"
              data-bs-slide="prev">
              <i class="fa-solid fa-chevron-left"></i>
            </button>

            <!-- Flecha derecha -->
            <button class="carousel-control-next custom-flecha" type="button" data-bs-target="#carouselProducto"
              data-bs-slide="next">
              <i class="fa-solid fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
      <!-- Derecha: Detalles del producto -->
      <div class="columna derecha">
        <div class="fila-superior">
          <p class="marca-categoria">
            <strong>{{ producto.marca || 'Logitech' }}</strong> | {{ producto.categoria || '--' }}
          </p>

          <div v-if="producto.etiquetas?.length" class="contenedor-etiquetas">
            <span v-for="(etiqueta, index) in producto.etiquetas" :key="index" class="etiqueta-producto">
              {{ etiqueta }}
            </span>
          </div>
        </div>

        <div class="encabezado-nombre-favorito">
          <h3 class="nombre-producto">{{ producto.nombre }}</h3>
          <button v-if="producto !== null" @click="toggleFavorito" class="btn-favorito-fijo">
            <i :class="esFavorito ? 'fas fa-heart' : 'far fa-heart'"></i>
          </button>
        </div>

        <p v-if="!modoPreview" class="metricas">
          <i class="fa-solid fa-eye"></i> {{ metricasFalsas.vistas }} vistas –
          <i class="fa-brands fa-whatsapp"></i> {{ metricasFalsas.consultas }} consultas –
          <i class="fa-solid fa-cart-shopping"></i> {{ metricasFalsas.compras }} compras
        </p>


        <div class="precio-producto">
          <span v-if="producto.descuento > 0" class="precio-original">
            {{ formatPrice(producto.precio) }}
          </span>

          <div class="precio-final-con-descuento">
            <span class="precio-final">
              {{ formatPrice(producto.precioConDescuento || producto.precio) }}
            </span>
            <span v-if="producto.porcentajeDescuento" class="etiqueta-descuento">
              -{{ producto.porcentajeDescuento }}% OFF
            </span>
          </div>

          <div v-if="producto.descuento && fechaDescuento && !descuentoVencido" class="bloque-descuento-mejorado">

            <div class="linea-fecha">
              <i class="fa-regular fa-clock icono-fecha"></i>
              <span class="texto-fecha">
                <strong>Válido hasta {{ fechaDescuento }}</strong>
              </span>
            </div>
            <div v-if="!descuentoVencido" class="linea-dias">
              <i class="fa-solid fa-hourglass-half icono-dia"></i>
              <span class="texto-dias">
                Quedan <strong>{{ diasRestantes }}</strong> día<span v-if="diasRestantes !== 1">s</span> de descuento
              </span>
            </div>
          </div>
        </div>



        <div v-if="producto.modelos?.length" class="cardsModeloGeneral">
          <h5 class="titulo-modelos">| Colores: {{ modeloSeleccionado.color }}</h5>
          <div class="cardsModelo">
            <div v-for="(modelo, index) in producto.modelos" :key="modelo.id"
              :class="['cardModelo', { activo: modeloSeleccionado?.id === modelo.id }]"
              @click="seleccionarModelo(modelo)">
              <img :src="modelo.imagenMiniatura || modelo.imagenCarrusel?.[0]" alt="Modelo" />
            </div>
          </div>
        </div>


        <div class="stock-info">
          <div class="stock-cabecera">
            <i class="fa-solid fa-boxes-stacked icono-stock"></i>
            <h5 class="titulo-stock">Stock: {{ stockDisponible }} disponible<span v-if="stockDisponible !== 1">s</span>
            </h5>
          </div>

          <div class="selector-cantidad">
            <label for="cantidad" class="label-cantidad">Cantidad:</label>
            <select v-model="cantidadSeleccionada" @change="verificarCantidad" class="select-cantidad">
              <option v-for="n in 5" :key="n" :value="n">{{ n }} unidad<span v-if="n > 1">es</span></option>
              <option value="custom">+6 unidades</option>
            </select>

            <input v-if="mostrarInputCustom" type="number" min="6" :max="stockDisponible"
              v-model.number="cantidadCustom" placeholder="Ingresá la cantidad" class="input-custom" />
          </div>
        </div>

        <div class="botones-modernos">
          <button class="btn-comprar" @click="registrarCompra">Comprar ahora</button>

          <div class="botones-acciones">
            <button class="btn-icono" @click="consultarPorWhatsApp">
              <i class="fab fa-whatsapp"></i>
            </button>

            <button class="btn-icono" @click="agregarAlCarrito">
              <i class="fas fa-cart-plus"></i>
            </button>

          </div>
        </div>

      </div>

      <div class="columna descripcion-detalle">
        <div class="descripcion-producto" :class="{ expandida: descripcionExpandida }">
          <p class="descripcion-texto" ref="descripcionTexto">{{ producto.descripcion }}</p>
          <div class="fade-descripcion" v-if="!descripcionExpandida && mostrarFade"></div>


        </div>

        <!-- Botón fuera del contenedor que tiene overflow -->
        <button v-if="mostrarFade" class="boton-ver-mas" @click="descripcionExpandida = !descripcionExpandida">
          {{ descripcionExpandida ? 'Ver menos' : 'Ver más' }}
          <i :class="[descripcionExpandida ? 'fa-chevron-up' : 'fa-chevron-down', 'fa-solid']"></i>
        </button>

        <div v-for="(item, index) in producto.detallesTecnicos" :key="index" class="acordeon">
          <div class="acordeon-header" @click="toggle(index)">
            <h4 class="titulo-acordeon">{{ item.titulo }}</h4>
            <i :class="['fa-solid', { 'fa-chevron-down': !item.abierto, 'fa-chevron-up': item.abierto }]"
              class="icono-flecha"></i>
          </div>
          <transition name="fade-acordeon">
            <div v-if="item.abierto" class="acordeon-cuerpo">
              <ul>
                <li v-for="(detalle, i) in item.detalles" :key="i" class="item-detalle">
                  <span class="detalle-clave">{{ detalle.clave }}:</span> {{ detalle.valor }}
                </li>
              </ul>
            </div>
          </transition>
        </div>


      </div>
    </div>


    <div v-else class="cargando">
      <p>Cargando producto...</p>
    </div>
  </div>

  <Notificacion ref="refNoti" />

</template>

<script setup>
// 📦 Imports
import { ref, computed, onMounted, watch, nextTick, watchEffect } from 'vue'
import { auth, db } from '../firebase'
import { doc, getDoc, setDoc, updateDoc, increment } from 'firebase/firestore'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Notificacion from '../components/ToastNotificacion.vue'

// 📥 Props y rutas
const props = defineProps({ producto: Object, modoPreview: Boolean })
const route = useRoute()

// 🧠 Estado reactivo
const producto = ref(null)
const modeloSeleccionado = ref(null)
const imagenSeleccionada = ref('')
const originalImagenesProducto = ref([])
const cantidadSeleccionada = ref(1)
const cantidadCustom = ref(null)
const mostrarInputCustom = ref(false)
const cantidadFinal = ref(1)
const stockDisponible = ref(0)
const descripcionExpandida = ref(false)
const mostrarFade = ref(false)
const descripcionTexto = ref(null)
const esFavorito = ref(false)
const metricasFalsas = ref({ vistas: 0, consultas: 0, compras: 0 })


// 🔔 Notificaciones
const refNoti = ref(null)

// 🚀 Carga inicial
onMounted(async () => {
  if (props.modoPreview && props.producto) {
    // 👀 Vista previa (no incrementa vistas reales)
    procesarProducto(props.producto)
  } else {
    try {
      const res = await axios.get(`http://localhost:5000/api/product/${route.params.id}`)
      procesarProducto(res.data)
      console.log('📦 Producto completo recibido:', res.data)
    } catch (err) {
      console.error('Error al obtener producto:', err)
    }
  }

  // ❤️ Verifica si está en favoritos
  if (producto.value?.id) {
    const user = auth.currentUser
    if (user) {
      const docSnap = await getDoc(doc(db, 'usuarios', user.uid))
      if (docSnap.exists()) {
        const favoritos = docSnap.data().favoritos || []
        esFavorito.value = favoritos.includes(producto.value.id)
      }
    }
  }
})


// 📱 Consultas por WhatsApp
async function consultarPorWhatsApp() {
  if (!producto.value?.id) return
  const docRef = doc(db, 'productos', producto.value.id)
  await updateDoc(docRef, { consultas: increment(1) })

  const telefono = '5491151083065'
  const mensaje = `Hola, quería consultar por el producto: ${producto.value.nombre}`
  window.open(`https://wa.me/${telefono}?text=${encodeURIComponent(mensaje)}`, '_blank')
}

// 🛒 Registrar compra
async function registrarCompra() {
  if (!producto.value?.id) return
  const docRef = doc(db, 'productos', producto.value.id)
  await updateDoc(docRef, { compras: increment(1) })

  refNoti.value?.mostrar('Gracias por tu compra', 'Tu orden fue registrada', 'success')
}


watch(producto, (nuevoProducto) => {
  if (nuevoProducto?.id) {
    const favs = JSON.parse(localStorage.getItem('favoritos')) || []
    esFavorito.value = favs.some(f => f.id === nuevoProducto.id)
  }
})

watch([cantidadSeleccionada, cantidadCustom, mostrarInputCustom], () => {
  cantidadFinal.value = mostrarInputCustom.value
    ? cantidadCustom.value || 6
    : cantidadSeleccionada.value

  if (cantidadFinal.value > stockDisponible.value) {
    cantidadFinal.value = stockDisponible.value
    cantidadCustom.value = stockDisponible.value
  }

  if (modeloSeleccionado.value) {
    modeloSeleccionado.value.cantidad = cantidadFinal.value
  }
})

// ✅ Utilidades
const formatPrice = value =>
  new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(value || 0)

const calcularPrecioConDescuento = (precio, tipo, valor) => {
  if (!valor || !precio) return precio
  return tipo === 'porcentaje'
    ? precio - (precio * valor / 100)
    : precio - valor
}

function formatearFecha(fecha) {
  if (!fecha) return '';
  const fechaObj = new Date(fecha);
  return fechaObj.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
}

const fechaDescuento = computed(() => {
  const fecha = modeloSeleccionado.value?.fechaYHoraVencimiento || producto.value?.fechaYHoraVencimiento;
  return fecha ? formatearFecha(fecha) : '';
});

const descuentoVencido = computed(() => {
  const fecha = modeloSeleccionado.value?.fechaYHoraVencimiento || producto.value?.fechaYHoraVencimiento
  if (!fecha) return false
  return new Date(fecha) < new Date()
})


const diasRestantes = computed(() => {
  const fechaRaw = modeloSeleccionado.value?.fechaYHoraVencimiento || producto.value?.fechaYHoraVencimiento
  if (!fechaRaw) return 0

  const ahora = new Date()
  const vencimiento = new Date(fechaRaw)

  // Redondeamos a la medianoche para evitar errores por horas
  const soloFechaHoy = new Date(ahora.getFullYear(), ahora.getMonth(), ahora.getDate())
  const soloFechaVenc = new Date(vencimiento.getFullYear(), vencimiento.getMonth(), vencimiento.getDate())

  const diferenciaMs = soloFechaVenc - soloFechaHoy
  return Math.max(Math.ceil(diferenciaMs / (1000 * 60 * 60 * 24)), 0)
})





// 🧩 Procesar producto
function procesarProducto(data) {
  const imagenesCarrusel = [...(data.imagenCarrusel || [])]
  if (data.imagenPortada && !imagenesCarrusel.includes(data.imagenPortada)) {
    imagenesCarrusel.unshift(data.imagenPortada)
  }

  const tipo = data.tipoDescuento
  const valor = tipo === 'porcentaje' ? data.porcentajeDescuento : data.montoDescuento
  const precioConDescuento = calcularPrecioConDescuento(data.precio, tipo, valor)

  const modelosConId = (data.modelos || []).map((modelo, index) => ({
    ...modelo,
    id: modelo.id || `modelo-${index}`
  }))

  producto.value = {
    id: data.id || route.params.id || '',
    ...data,
    imagenCarrusel: imagenesCarrusel,
    etiquetas: data.etiquetas || [],
    detallesTecnicos: data.detallesTecnicos || [],
    modelos: modelosConId,
    descuento: Number(data.descuento) || 0,
    precio: data.precio,
    precioConDescuento,
    porcentajeDescuento: data.porcentajeDescuento ?? 0,
    stockDisponible: data.stockDisponible || 0
  }

  const modeloBase = {
    id: `base-${data.id || 'default'}`,
    nombre: data.nombre,
    imagenMiniatura: data.imagen || data.imagenCarrusel?.[0],
    imagenCarrusel: [data.imagen, ...(data.imagenCarrusel || [])].filter(Boolean),
    precio: data.precio,
    descuento: Number(data.descuento) || 0,
    tipoDescuento: data.tipoDescuento,
    porcentajeDescuento: data.porcentajeDescuento,
    montoDescuento: data.montoDescuento,
    stockDisponible: data.stockDisponible || 0,
    color: data.colorPrincipal || 'Sin color'
  }

  producto.value.modelos.unshift(modeloBase)
  originalImagenesProducto.value = [...producto.value.imagenCarrusel]
  imagenSeleccionada.value = producto.value.imagenCarrusel[0] || ''
  stockDisponible.value = producto.value.stockDisponible

  if (producto.value.modelos.length > 0) {
    seleccionarModelo(producto.value.modelos[0])
  }

  producto.value.detallesTecnicos.forEach(detalle => detalle.abierto = false)

  nextTick(() => {
    if (descripcionTexto.value) {
      mostrarFade.value = descripcionTexto.value.scrollHeight > 120
    }
  })

  // 👁‍🗨 Incrementar vista real (solo si no es preview)
  if (!props.modoPreview && producto.value.id) {
    const docRef = doc(db, 'productos', producto.value.id)
    updateDoc(docRef, { vistas: increment(1) }).catch(err => {
      console.warn('No se pudo incrementar la vista:', err)
    })
  }

  metricasFalsas.value = { ...generarMetricasPorId(producto.value.id) }
}


// 🔧 Otros handlers
function seleccionarSlide(index) {
  const carousel = document.querySelector('#carouselProducto')
  const bsCarousel = bootstrap.Carousel.getInstance(carousel) || new bootstrap.Carousel(carousel)
  bsCarousel.to(index)
}

function seleccionarModelo(modelo) {
  modeloSeleccionado.value = modelo
  producto.value.nombre = modelo.nombre ?? producto.value.nombre
  imagenSeleccionada.value = modelo.imagenCarrusel?.[0] || producto.value.imagenCarrusel[0] || ''
  producto.value.imagenCarrusel = modelo.imagenCarrusel?.length
    ? [...modelo.imagenCarrusel]
    : [...originalImagenesProducto.value]

  producto.value.precio = modelo.precio ?? producto.value.precio
  producto.value.descuento = Number(modelo.descuento) || 0
  producto.value.tipoDescuento = modelo.tipoDescuento
  producto.value.porcentajeDescuento = modelo.porcentajeDescuento ?? 0
  producto.value.montoDescuento = modelo.montoDescuento

  const tipo = modelo.tipoDescuento
  const valor = tipo === 'porcentaje' ? modelo.porcentajeDescuento : modelo.montoDescuento
  producto.value.precioConDescuento = calcularPrecioConDescuento(modelo.precio, tipo, valor)

  producto.value.stockDisponible = modelo.stockDisponible ?? producto.value.stockDisponible
  stockDisponible.value = producto.value.stockDisponible

  if (modelo.cantidad && modelo.cantidad >= 6) {
    cantidadSeleccionada.value = 'custom'
    mostrarInputCustom.value = true
    cantidadCustom.value = modelo.cantidad
  } else {
    cantidadSeleccionada.value = modelo.cantidad || 1
    mostrarInputCustom.value = false
    cantidadCustom.value = null
  }

  cantidadFinal.value = modelo.cantidad || 1
}

// 🛒 Carrito
function agregarAlCarrito() {
  const productoAGuardar = {
    id: modeloSeleccionado.value?.id || producto.value.id,
    nombre: modeloSeleccionado.value?.nombre || producto.value.nombre,
    imagen: modeloSeleccionado.value?.imagen
      || modeloSeleccionado.value?.imagenMiniatura
      || modeloSeleccionado.value?.imagenCarrusel?.[0]
      || producto.value.imagenCarrusel?.[0],
    precio: producto.value.precioConDescuento || producto.value.precio,
    cantidad: cantidadFinal.value || 1,
    color: modeloSeleccionado.value?.color || producto.value.colorPrincipal || 'Sin color'
  }

  let carrito = JSON.parse(localStorage.getItem('carrito')) || []
  const indexExistente = carrito.findIndex(item =>
    item.id === productoAGuardar.id && item.color === productoAGuardar.color
  )

  if (indexExistente !== -1) {
    carrito[indexExistente].cantidad += productoAGuardar.cantidad
  } else {
    carrito.push(productoAGuardar)
  }

  localStorage.setItem('carrito', JSON.stringify(carrito))
  window.dispatchEvent(new Event('storage'))

  refNoti.value?.mostrar('Producto agregado al carrito', 'Podés verlo en tu carrito', 'success')
}

// ❤️ Favoritos
async function toggleFavorito() {
  if (!producto.value?.id) return

  const user = auth.currentUser
  if (!user) {
    refNoti.value?.mostrar('Iniciá sesión', 'Tenés que iniciar sesión para usar favoritos', 'error')
    return
  }

  const idProducto = producto.value.id
  const userRef = doc(db, 'usuarios', user.uid)
  let favoritos = []

  const docSnap = await getDoc(userRef)
  if (docSnap.exists()) favoritos = docSnap.data().favoritos || []

  const yaExiste = favoritos.includes(idProducto)

  if (yaExiste) {
    favoritos = favoritos.filter(id => id !== idProducto)
    esFavorito.value = false
    refNoti.value?.mostrar('Eliminado de favoritos', 'Ya no está en tu lista', 'info')
  } else {
    favoritos.push(idProducto)
    esFavorito.value = true
    refNoti.value?.mostrar('¡Agregado a favoritos!', 'Se añadió a tu lista', 'success')
  }

  await setDoc(userRef, { favoritos }, { merge: true })

  if (window?.cargarProductosFavoritos) window.cargarProductosFavoritos()
}

function toggle(index) {
  producto.value.detallesTecnicos[index].abierto = !producto.value.detallesTecnicos[index].abierto
}

function generarMetricasPorId(id) {
  const hash = Array.from(id).reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return {
    vistas: 100 + (hash % 100),
    consultas: 50 + (hash % 60),
    compras: 10 + (hash % 20)
  }
}

const metricasIniciales = computed(() => {
  if (!producto.value?.id) return { vistas: 0, consultas: 0, compras: 0 }

  // 🧠 Generar base si falta algún valor
  const base = generarMetricasPorId(producto.value.id)
  return {
    vistas: producto.value.vistas ?? base.vistas,
    consultas: producto.value.consultas ?? base.consultas,
    compras: producto.value.compras ?? base.compras
  }
})

// ⚙️ Cargar en onMounted o cuando el producto esté disponible
watchEffect(() => {
  if (producto.value?.id) {
    metricasFalsas.value = { ...metricasIniciales.value }
  }
})



</script>




<style scoped>
/* ======================= */
/* 🔷 ESTRUCTURA GENERAL 🔷 */
/* ======================= */

.contenedorGeneral {
  background: var(--colorFondoPrincipal);
  padding: 2rem 1rem;
}

.contenedor-producto {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  max-width: 1200px;
  margin: auto;
  background: var(--colorFondoPrincipal);
  color: var(--colorTextoPrincipal);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  column-gap: 3rem;
}

.columna.derecha {
  border-left: 1px solid #e5e7eb;
  padding-left: 2rem;
}

.columna {
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.descripcion-detalle {
  flex: 1 1 100%;
}

.fila-superior {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}


/* ========================= */
/* 🟦 MODELOS DE PRODUCTO 🟦 */
/* ========================= */

.cardsModeloGeneral {
  padding: 12px;
  overflow-x: auto;
  white-space: nowrap;
}

.cardsModelo {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.cardModelo {
  width: 70px;
  height: 70px;
  border-radius: 16px;
  border: 2px solid transparent;
  overflow: hidden;
  cursor: pointer;
  transition: border 0.2s ease-in-out;
  flex-shrink: 0;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: none;
  transition: box-shadow 0.2s ease;
}

.cardModelo img {
  width: auto;
  height: 100%;
  max-width: 100%;
  object-fit: contain;
  padding: 6px;
  background-color: white;
}


.cardModelo.activo {
  border: 2px solid var(--colorPrincipal);
}

.descripcion-producto {
  position: relative;
  max-height: 7.5em;
  overflow: hidden;
  transition: max-height 0.3s ease;
  padding-bottom: 3.5rem;
  /* más espacio para el botón */
  z-index: 1;
  /* asegura que esté encima */
}


.descripcion-producto.expandida {
  max-height: none;
  padding-bottom: 0;
}


.fade-descripcion {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3em;
  background: linear-gradient(to top, var(--colorFondoPrincipal), transparent);
}

/* ======================== */
/* 🟢 BOTONES DE ACCIÓN 🟢 */
/* ======================== */

.botones-accion-unificados {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.boton-comprar-grande {
  flex: 1;
  padding: 1rem;
  background-color: var(--colorPrincipal);
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  border: none;
  border-radius: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.boton-comprar-grande:hover {
  opacity: 0.85;
}

.acciones-secundarias {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.boton-icono {
  background-color: var(--colorTerciario);
  color: white;
  border: none;
  width: 52px;
  height: 52px;
  border-radius: 12px;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.boton-icono:hover {
  opacity: 0.85;
}

.boton-icono:first-child {
  background-color: #25D366;
  /* WhatsApp verde */
}

.botones-modernos {
  max-width: 600px;
  /* Más ancho */
  width: 100%;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.btn-comprar {
  width: 100%;
  padding: 1.2rem 2rem;
  background: #111827;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.btn-comprar:hover {
  background: #1f2937;
  transform: translateY(-2px);
}

.botones-acciones {
  display: flex;
  justify-content: space-between;
  gap: 1.2rem;
}

.btn-icono {
  flex: 1;
  padding: 1rem 0;
  font-size: 1.4rem;
  border: none;
  border-radius: 12px;
  background: #f3f4f6;
  color: #111827;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.btn-icono:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.boton-ver-mas {
  background: none;
  border: none;
  color: var(--colorPrincipal);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.25rem 0;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: color 0.2s ease;
}

.boton-ver-mas:hover {
  color: var(--colorPrincipalHover);
}




/* ======================== */
/* 🖼️ CARRUSEL DE IMÁGENES 🖼️ */
/* ======================== */

.contenedor-imagenes {
  display: flex;
  gap: 1rem;
}

.carrusel-principal {
  flex: 1;
}

.contenedor-imagen {
  width: 100%;
  height: 450px;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 1rem;
  overflow: hidden;
}

.imagen-principal {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.custom-flecha {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--colorFondoSecundario);
  padding: 0 1rem;
  z-index: 2;
}


/* ============================ */
/* 🔳 MINIATURAS LATERALES 🔳 */
/* ============================ */

.miniaturas-vertical {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.miniatura-vertical {
  width: 60px;
  height: 60px;
  object-fit: contain;
  padding: 4px;
  background-color: white;
  border-radius: 0.5rem;
  border: 2px solid transparent;
  cursor: pointer;
}


.miniatura-vertical:hover {
  border-color: var(--colorPrincipal);
}


/* ============================ */
/* 🏷️ INFORMACIÓN DEL PRODUCTO */
/* ============================ */

.marca-categoria {
  font-size: 0.9rem;
  color: var(--colorSecundario);
  margin: 0;
}

.nombre-producto {
  font-size: 1.8rem;
  font-weight: 500;
  font-family: var(--fuenteTerciario);
  color: var(--colorTextoPrincipal);
  margin-bottom: 0.5rem;
  padding-bottom: 0.4rem;
}

.encabezado-nombre-favorito {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.btn-favorito-fijo {
  background: none;
  margin-bottom: 15px;
  border: none;
  font-size: 1.6rem;
  color: #e63946;
  /* rojo corazón */
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}

.btn-favorito-fijo:hover {
  transform: scale(1.15);
  color: #c21807;
  /* rojo más oscuro al pasar el mouse */
}




/* 💰 PRECIO */
.precio-producto {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin: 0.5rem 0 1rem;
}

.precio-original {
  font-size: 1rem;
  color: #888;
  text-decoration: line-through;
}

.precio-final-con-descuento {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.precio-final {
  font-size: 2.2rem;
  font-weight: 600;
  color: var(--colorFondoSecundario);
}

.etiqueta-descuento {
  font-size: 1rem;
  font-weight: 600;
  color: #00a650;
  background-color: #e6f6ec;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  text-transform: uppercase;
}


/* ========================= */
/* 🟣 ETIQUETAS DEL PRODUCTO */
/* ========================= */

.contenedor-etiquetas {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.etiqueta-producto {
  background-color: var(--colorTerciario);
  color: #fff;
  padding: 0.25rem 0.75rem;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}


/* 🎨 COLOR DEL PRODUCTO */

.color-circulo {
  width: 25px;
  height: 25px;
  background: var(--colorPrincipal);
  border-radius: 50%;
}


/* ======================== */
/* ➕ CANTIDAD Y BOTONES 🛒 */
/* ======================== */

.control-cantidad {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.boton-cantidad {
  width: 30px;
  height: 30px;
  background: var(--colorSecundario);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  cursor: pointer;
}

.boton-agregar {
  background: var(--colorTerciario);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  font-weight: bold;
  margin-top: 1.5rem;
  transition: background 0.3s ease;
  cursor: pointer;
}

.boton-agregar:hover {
  background: var(--colorTerciarioHover);
}



.stock-info {
  background: #f7f7f7;
  padding: 1rem;
  border-radius: 1rem;
  margin: 1rem 0;
  color: #333;
  border: 1px solid #ddd;
}



.stock-cabecera {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.icono-stock {
  font-size: 1.4rem;
  color: var(--colorPrincipal);
}

.titulo-stock {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.selector-cantidad {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

.select-cantidad,
.input-custom {
  width: 30%;
}

.label-cantidad {
  font-weight: 600;
}

.select-cantidad {
  padding: 0.5rem;
  border-radius: 0.5rem;
  border: none;
  background: white;
  color: #333;
  font-weight: bold;
}

.input-custom {
  padding: 0.5rem;
  border-radius: 0.5rem;
  border: 2px solid var(--colorPrincipal);
  background: #fff;
  color: #333;
  font-weight: 500;
}



/* =================== */
/* 📋 ACORDEÓN TÉCNICO */
/* =================== */

.acordeon {
  border-top: 1px solid #e5e7eb;
  margin-top: 1rem;
  padding-top: 1rem;
}

.acordeon-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 0.8rem 0;
  transition: color 0.3s ease;
}

.acordeon-header:hover {
  color: var(--colorPrincipal);
}

.titulo-acordeon {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
  color: var(--colorPrincipal);
}

.icono-flecha {
  font-size: 1.2rem;
  color: var(--colorPrincipal);
  transition: transform 0.3s ease;
}

.acordeon-cuerpo {
  margin-top: 0.5rem;
  padding-left: 1rem;
}

.acordeon-cuerpo ul {
  columns: 2;
  column-gap: 2rem;
}


.item-detalle {
  margin-bottom: 0.4rem;
}

.detalle-clave {
  font-weight: 600;
  margin-right: 0.5rem;
  color: #111827;
}

/* Animación */
.fade-acordeon-enter-active,
.fade-acordeon-leave-active {
  transition: all 0.3s ease;
}

.fade-acordeon-enter-from,
.fade-acordeon-leave-to {
  opacity: 0;
  max-height: 0;
}

.fade-acordeon-enter-to,
.fade-acordeon-leave-from {
  opacity: 1;
  max-height: 300px;
}

/* Notificación toast */
.noti-container {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 999999;
}

.noti-toast {
  background-color: #212529;
  color: white;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  min-width: 280px;
  max-width: 350px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  gap: 12px;
  animation: slideIn 0.3s ease-out;
}

.noti-toast.success {
  border-left: 5px solid #28a745;
}

.noti-toast.error {
  border-left: 5px solid #dc3545;
}

.noti-toast.info {
  border-left: 5px solid #17a2b8;
}

.icono {
  margin-top: 2px;
  font-size: 1.2rem;
  color: white;
}

.contenido {
  flex: 1;
  color: white;
}

.titulo {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
}

.tiempo {
  font-size: 0.75rem;
  color: #ccc;
  margin-top: 4px;
  display: block;
}


.mensaje {
  margin: 0;
  font-size: 0.9rem;
  color: #f1f1f1;
}

.btn-cerrar {
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

@keyframes slideIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.bloque-descuento-mejorado {
  background-color: #ecfdf5;
  /* Verde suave */
  border-left: 5px solid var(--colorExito, #22c55e);
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  margin: 1.5rem 0;
  color: #065f46;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  animation: aparecerSuave 0.3s ease-out;
  font-size: 0.95rem;
}

.linea-fecha,
.linea-dias {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.icono-fecha {
  color: #10b981;
  font-size: 1.1rem;
}

.icono-dia {
  color: #f59e0b;
  font-size: 1.1rem;
}

.texto-fecha strong,
.texto-dias strong {
  font-weight: 600;
  color: #065f46;
}

@keyframes aparecerSuave {
  from {
    opacity: 0;
    transform: translateY(6px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}


/* ============= */
/* ⏳ CARGANDO... */
/* ============= */

.cargando {
  text-align: center;
  padding: 2rem;
  color: var(--colorSecundario);
}


/* ======================= */
/* 📱 MEDIA QUERIES 📱 */
/* ======================= */

/* Ajustes para pantallas menores a 992px (tablet) */
/* 📱 Adaptación total para móviles y tablets */
/* 📱 Mejoras UX/UI para móviles y tablets */
/* 📱 Mejoras UX/UI respetando estructura vertical SIEMPRE */
@media (max-width: 991px) {

  html,
  body {
    width: 100%;
    overflow-x: hidden;
  }

  .contenedorGeneral,
  .contenedor-producto,
  .columna {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  .contenedor-producto {
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 1rem;
    gap: 2rem;
  }

  .contenedor-imagenes {
    display: flex;
    flex-direction: row;
    /* Mantenemos miniaturas a la izquierda SIEMPRE */
    align-items: flex-start;
    gap: 1rem;
    width: 100%;
  }

  .miniaturas-vertical {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    max-height: 350px;
    overflow-y: auto;
    /* Si hay muchas miniaturas */
  }

  .miniatura-vertical {
    width: 55px;
    height: 55px;
    object-fit: contain;
    border-radius: 0.5rem;
    cursor: pointer;
  }

  .carrusel-principal {
    flex: 1;
  }

  .contenedor-imagen {
    width: 100%;
    height: 300px;
    border-radius: 0.75rem;
  }

  /* 🎯 Texto centrado */
  .nombre-producto,
  .precio-producto {
    text-align: center;
  }

  .nombre-producto {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .precio-producto {
    margin-bottom: 1.5rem;
  }

  /* 🛒 Botones cómodos */
  .btn-comprar,
  .btn-icono {
    padding: 1.2rem 2rem;
    font-size: 1.2rem;
  }

  .btn-comprar:hover,
  .btn-icono:hover {
    transform: translateY(-2px);
    opacity: 0.9;
  }

  .botones-modernos {
    width: 100%;
    max-width: 500px;
    margin: 1rem auto;
  }

  .cardsModelo {
    justify-content: center;
    gap: 1rem;
    padding: 0.5rem 0;
  }

  .selector-cantidad {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }

  .select-cantidad,
  .input-custom {
    width: 100%;
  }

  .descripcion-producto {
    max-height: none;
    padding-bottom: 2rem;
  }

  .stock-info {
    padding: 1rem;
    margin-top: 1rem;
    width: 100%;
  }

  .acordeon-cuerpo ul {
    columns: 1;
  }
}

/* 📱 Ajustes extras para celulares muy chicos */
@media (max-width: 575px) {
  .miniatura-vertical {
    width: 45px;
    height: 45px;
  }

  .contenedor-imagen {
    height: 250px;
  }

  .nombre-producto {
    font-size: 1.3rem;
  }

  .precio-final {
    font-size: 1.6rem;
  }

  .cardModelo {
    width: 50px;
    height: 50px;
  }
}



@media (max-width: 439px) {
  .contenedor-producto {
    flex-direction: column;
    padding: 1rem;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  .columna {
    flex: 1 1 100%;
    padding: 0;
  }

  .contenedor-imagen {
    height: 250px;
    width: 100%;
    border-radius: 0.75rem;
  }

  .miniaturas-vertical {
    flex-direction: row;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .carrusel-principal {
    width: 100%;
  }

  .descripcion-producto {
    max-height: none;
    padding-bottom: 2rem;
  }

  .botones-modernos {
    width: 100%;
    margin-top: 1rem;
  }

  .acordeon-cuerpo ul {
    columns: 1;
  }
}
</style>

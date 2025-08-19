<template>
  <div class="admin-carga container-fluid py-5 text-white">
    <h1 class="titulo-principal text-center mb-4">
      <i class="fas fa-file-import me-2 text-white"></i>
      Carga Masiva de Productos
    </h1>


    <!-- 📂 Subida de archivo -->
    <div class="mb-4 text-center">
      <button class="btn btn-outline-info mb-2" @click="descargarPlantilla">
        <i class="fas fa-file-download me-2"></i> Descargar plantilla
      </button>
      <br />
      <input type="file" @change="handleArchivo" accept=".xlsx, .xls" class="form-control w-auto d-inline-block"
        :disabled="isCargando" />
      <p class="mt-2 small text-secondary">Subí un archivo Excel con tus productos</p>
    </div>


    <!-- 🔍 Vista previa -->
    <div v-if="productos.length > 0" class="table-responsive mt-4">
      <!-- ☁️ Botón de carga + vaciar -->
      <div class="d-flex justify-content-between align-items-center mt-4">
        <h5 class="mb-0 text-warning">
          <i class="fas fa-eye me-1"></i> Vista previa
        </h5>
        <div class="text-muted small mb-3 ps-1 d-flex align-items-center gap-3">
          <span>
            <i class="fas fa-box-open me-1"></i>
            <strong>{{ cantidadBase }}</strong> productos base
          </span>
          <span>
            <i class="fas fa-cubes me-1"></i>
            <strong>{{ cantidadModelos }}</strong> modelos
          </span>
        </div>

        <button class="btn-vaciar" :disabled="isCargando || productos.length === 0" @click="vaciarProductos">
          <i class="fas fa-trash-alt me-2"></i>
          Vaciar Productos
        </button>
      </div>


      <table class="table table-dark table-striped table-bordered">
        <thead>
          <tr>
            <th v-for="(col, index) in columnasVisibles" :key="index">{{ col }}</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prod, idx) in productos" :key="idx">
            <td v-for="col in columnasVisibles" :key="col">
              <span v-if="col === 'descripcion' && prod[col]" class="truncado" @click="abrirDescripcion(prod[col])"
                style="cursor: pointer;" :title="prod[col]">
                {{ prod[col] }}
              </span>

              <span v-else>
                {{ prod[col] }}
              </span>
            </td>

            <td>
              <button class="btn btn-sm btn-warning" @click="abrirModal(prod)">
                <i class="fas fa-pencil-alt me-1"></i> Completar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- ☁️ Botón de carga -->
      <div class="text-center mt-4">
        <button class="btn-cargar-firebase me-2" :disabled="isCargando" @click="cargarProductos">
          <i class="fas me-2" :class="isCargando ? 'fa-spinner fa-spin' : 'fa-cloud-upload-alt'"></i>
          {{ isCargando ? 'Subiendo...' : 'Subir Productos' }}
        </button>
      </div>

    </div>

    <!-- ❌ Aún no se subió archivo -->
    <div v-else class="text-center mt-5 text-muted">
      <i class="fas fa-file-excel fa-3x mb-3 text-secondary"></i>
      <p>No se ha subido ningún archivo aún.</p>
    </div>
  </div>

  <!-- 🧩 Modal de edición -->
  <ModalCompletar ref="modalCompletar" :producto="productoSeleccionado" @guardado="actualizarProducto" />
  <SpinnerCarga ref="spinnerRef" mensaje="Subiendo productos..." />

  <div v-if="mostrarDescripcion" class="modal-descripcion" @click="mostrarDescripcion = false">
    <div class="contenido" @click.stop>
      <h5 class="mb-2">📝 Descripción completa</h5>
      <p>{{ descripcionExpandida }}</p>
      <button class="btn btn-sm btn-outline-light mt-3" @click="mostrarDescripcion = false">Cerrar</button>
    </div>
  </div>

  <!-- 🚀 Progreso de carga -->
<div v-if="isCargando" class="progreso-carga mt-4">
  <div class="barra-externa">
    <div class="barra-interna" :style="{ width: progreso + '%' }"></div>
  </div>
  <p class="text-center mt-2">{{ progreso }}% cargado ({{ cargados }} de {{ productos.length }})</p>
</div>





  <ToastNotificacion ref="toastRef" />

</template>



<script setup>
import { ref, nextTick, onMounted, watch, computed } from 'vue'
import * as XLSX from 'xlsx'
import axios from 'axios'


import ModalCompletar from '../components/Modals/ModalCompletar.vue'
import SpinnerCarga from '../components/SpinnerCarga.vue'
import ToastNotificacion from '../components/ToastNotificacion.vue'

// Refs principales
const productos = ref([])
const columnas = ref([])
const nombresExistentesEnDB = ref([])
const isCargando = ref(false)
const toastRef = ref(null)
const spinnerRef = ref(null)
const mostrarDescripcion = ref(false)
const descripcionExpandida = ref('')
const progreso = ref(0)
const cargados = ref(0)



// Modal completar
const mostrarModalCompletar = ref(false)
const modalCompletarRef = ref(null)
const productoSeleccionado = ref(null)

const columnasVisibles = ref([
  'nombre', 'marca', 'color', 'descripcion', 'etiqueta', 'precio'
])

const actualizarProducto = (productoActualizado) => {
  const index = productos.value.findIndex(p => p.nombre === productoActualizado.nombre)
  if (index !== -1) {
    productos.value[index] = productoActualizado
  }
}



const modalCompletar = ref(null)

const abrirModal = (producto) => {
  productoSeleccionado.value = producto
  modalCompletar.value?.abrir()
}

const cantidadBase = computed(() => productos.value.length)

const cantidadModelos = computed(() =>
  productos.value.reduce((acc, p) => acc + (Array.isArray(p.modelos) ? p.modelos.length : 0), 0)
)

// Función para descargar plantilla Excel
const descargarPlantilla = () => {
  const encabezados = [
    'nombre', 'marca', 'color', 'descripcion', 'etiqueta',
    'precio', 'tipoDescuento', 'porcentajeDescuento',
    'montoDescuento', 'modeloDe', 'completado'
  ]

  const ejemplo = [{
    nombre: 'Auricular Gamer X',
    marca: 'Redragon',
    color: 'Negro',
    descripcion: 'Auricular con sonido 7.1 y micrófono',
    etiqueta: 'nuevo',
    precio: 12999,
    tipoDescuento: 'porcentaje',
    porcentajeDescuento: 15,
    montoDescuento: '',
    modeloDe: '',
    completado: false
  }]

  const hoja = XLSX.utils.json_to_sheet(ejemplo, { header: encabezados })
  const libro = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(libro, hoja, 'Productos')
  XLSX.writeFile(libro, 'PlantillaProductos.xlsx')
}

// Abrir modal completar
const abrirModalCompletar = (producto) => {
  productoSeleccionado.value = producto
  nextTick(() => {
    modalCompletarRef.value?.abrir()
  })
}

// Callback al guardar en el modal completar
const productoActualizado = (producto) => {
  toastRef.value?.mostrar('✅ Producto actualizado', `"${producto.nombre}" fue completado correctamente.`, 'success')
}

// Manejar carga de archivo Excel
const handleArchivo = (e) => {
  const file = e.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (evt) => {
    const data = new Uint8Array(evt.target.result)
    const workbook = XLSX.read(data, { type: 'array' })
    const sheet = workbook.Sheets[workbook.SheetNames[0]]
    let json = XLSX.utils.sheet_to_json(sheet)

    const columnasRequeridas = [
      'nombre', 'marca', 'color', 'descripcion', 'etiqueta', 'precio',
      'tipoDescuento', 'porcentajeDescuento', 'montoDescuento', 'modeloDe', 'completado'
    ]

    const columnasArchivo = Object.keys(json[0] || {})
    const faltantes = columnasRequeridas.filter(col => !columnasArchivo.includes(col))
    if (faltantes.length > 0) {
      toastRef.value?.mostrar('❌ Plantilla incorrecta', `Faltan columnas:\n• ${faltantes.join('\n• ')}`, 'error')
      e.target.value = ''
      return
    }

    json = json.filter(p => p.nombre && p.precio).map(p => {
      const estaCompleto = p.nombre && p.precio && p.marca && p.color && p.descripcion && p.etiqueta
      return {
        ...p,
        completado: false,
        oculto: !estaCompleto,
        imagen: p.imagen || (!estaCompleto ? '/Img/imagenNoDisponible.jpg' : '')
      }
    })

    const nombresActuales = productos.value.map(p => p.nombre?.trim().toLowerCase())
    const productosBase = []
    const productosModelos = []
    const duplicados = []

    for (const prod of json) {
      const nombre = prod.nombre?.trim()
      const nombreLower = nombre?.toLowerCase()
      const modeloDe = typeof prod.modeloDe === 'string' ? prod.modeloDe.trim().toLowerCase() : ''
      const esModelo = modeloDe.length > 0

      if (!nombre) continue

      const yaCargado =
        nombresActuales.includes(nombreLower) ||
        productosBase.some(p => p.nombre?.trim().toLowerCase() === nombreLower) ||
        nombresExistentesEnDB.value.includes(nombreLower)

      if (yaCargado) {
        duplicados.push(nombre)
        continue
      }

      if (esModelo) {
        productosModelos.push({ ...prod, modeloDe })
      } else {
        productosBase.push({ ...prod, modelos: [] })
      }
    }

    for (const modelo of productosModelos) {
      const base = productosBase.find(p => p.nombre?.trim().toLowerCase() === modelo.modeloDe)
      const estaCompleto = modelo.nombre && modelo.precio && modelo.color
      const modeloObj = {
        nombre: modelo.nombre,
        color: modelo.color,
        imagen: modelo.imagen || (!estaCompleto ? '/Img/imagenNoDisponible.jpg' : ''),
        imagenCarrusel: [],
        precio: modelo.precio || 0,
        descuento: modelo.descuento || false,
        tipoDescuento: modelo.tipoDescuento || '',
        porcentajeDescuento: modelo.porcentajeDescuento || 0,
        montoDescuento: modelo.montoDescuento || 0,
        stockDisponible: modelo.stockDisponible || 0,
        stockFisico: modelo.stockFisico || 0,
        oculto: !estaCompleto,
        completado: estaCompleto
      }

      if (base) {
        base.modelos.push(modeloObj)
      } else {
        toastRef.value?.mostrar('⚠️ Modelo sin producto base', `El modelo "${modelo.nombre}" no tiene producto base válido ("${modelo.modeloDe}") y fue ignorado.`, 'warning')
      }
    }

    if (duplicados.length > 0) {
      toastRef.value?.mostrar('⚠️ Productos duplicados detectados', `Ya estaban cargados o se repiten:\n• ${duplicados.join('\n• ')}`, 'warning')
    }

    if (productosBase.length > 0) {
      toastRef.value?.mostrar('✅ Nuevos productos cargados', `Se agregaron ${productosBase.length} producto(s) base.`, 'success')
      productos.value.push(...productosBase)
      columnas.value = Object.keys(productos.value[0] || {})
    }

    e.target.value = ''
  }

  reader.readAsArrayBuffer(file)
}

// Cargar productos a DB
const cargarProductos = async () => {
  if (!productos.value.length) {
    toastRef.value?.mostrar('⚠️ Sin productos', 'No hay productos para cargar.', 'error')
    return
  }

  isCargando.value = true
  cargados.value = 0
  progreso.value = 0
  spinnerRef.value?.mostrar()

  const loteSize = 20
  const total = productos.value.length

  const productosValidos = productos.value.filter(p => p.nombre && p.precio)
  const productosInvalidos = productos.value.filter(p => !p.nombre && !p.precio)

  try {
    for (let i = 0; i < productosValidos.length; i += loteSize) {
      const lote = productosValidos.slice(i, i + loteSize)

      await Promise.all(
        lote.map(prod => axios.post('http://localhost:5000/api/products', prod))
      )

      cargados.value += lote.length
      progreso.value = Math.min(Math.round((cargados.value / productosValidos.length) * 100), 100)

      toastRef.value?.mostrar(
        '📦 Subiendo productos...',
        `${cargados.value} de ${productosValidos.length} cargados (${progreso.value}%)`,
        'info'
      )
    }

    // Mensaje final
    toastRef.value?.mostrar(
      '✅ Productos cargados',
      `Se subieron ${productosValidos.length} productos.`,
      'success'
    )

    // Si hay productos inválidos, los dejamos en la tabla
    if (productosInvalidos.length > 0) {
      toastRef.value?.mostrar(
        '⚠️ Productos incompletos',
        `${productosInvalidos.length} productos no se subieron porque no tienen nombre ni precio.`,
        'warning'
      )
    }

    // Actualiza la lista: deja solo los inválidos en la tabla
    productos.value = productosInvalidos
    columnas.value = Object.keys(productos.value[0] || {})
    localStorage.setItem('productosExcel', JSON.stringify(productos.value))

  } catch (error) {
    console.error('Error al cargar productos:', error)
    toastRef.value?.mostrar('❌ Error durante la carga', 'Ocurrió un error al cargar los productos.', 'error')

  } finally {
    isCargando.value = false
    progreso.value = 0
    cargados.value = 0
    spinnerRef.value?.ocultar()
  }
}





// Vaciar lista
const vaciarProductos = () => {
  productos.value = []
  columnas.value = []
  localStorage.removeItem('productosExcel')
  toastRef.value?.mostrar('🧹 Productos eliminados', 'Se vació la lista de productos.', 'info')
}



// On mounted
onMounted(async () => {
  const data = localStorage.getItem('productosExcel')
  if (data) {
    try {
      const json = JSON.parse(data)
      productos.value = json
      columnas.value = Object.keys(productos.value[0] || {})
      toastRef.value?.mostrar('📁 Productos restaurados', 'Recuperamos los productos antes de recargar.', 'info')
    } catch (err) {
      console.error('Error al leer localStorage:', err)
    }
  }

  try {
    const res = await axios.get('http://localhost:5000/api/products')
    nombresExistentesEnDB.value = res.data.map(p => p.nombre?.trim().toLowerCase())
  } catch (err) {
    console.error('Error al obtener productos existentes:', err)
  }

  // 👇 Agregá esto al final de onMounted
  nextTick(() => {
    const thElems = document.querySelectorAll('th')
    thElems.forEach((th) => {
      const resizer = document.createElement('div')
      resizer.style.width = '5px'
      resizer.style.height = '100%'
      resizer.style.position = 'absolute'
      resizer.style.right = '0'
      resizer.style.top = '0'
      resizer.style.cursor = 'col-resize'
      resizer.style.userSelect = 'none'

      th.style.position = 'relative'
      th.appendChild(resizer)

      let startX, startWidth
      resizer.addEventListener('mousedown', (e) => {
        startX = e.pageX
        startWidth = th.offsetWidth
        document.documentElement.addEventListener('mousemove', doDrag)
        document.documentElement.addEventListener('mouseup', stopDrag)
      })

      const doDrag = (e) => {
        th.style.width = startWidth + e.pageX - startX + 'px'
      }

      const stopDrag = () => {
        document.documentElement.removeEventListener('mousemove', doDrag)
        document.documentElement.removeEventListener('mouseup', stopDrag)
      }
    })
  })
})

const abrirDescripcion = (texto) => {
  descripcionExpandida.value = texto
  nextTick(() => {
    mostrarDescripcion.value = true
  })
}



// Guardar productos en localStorage en tiempo real
watch(productos, (nuevos) => {
  if (nuevos.length > 0) {
    localStorage.setItem('productosExcel', JSON.stringify(nuevos))
  }
}, { deep: true })


</script>






<style scoped>
.titulo-principal {
  font-size: 2.8rem;
  font-weight: 800;
  color: var(--colorTerciario);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
}

.admin-carga {
  background-color: #121212;
  min-height: 100vh;
  overflow-x: hidden;
  /* 👈 Evita scroll horizontal por efecto hover */
  padding-bottom: 80px;
  /* 👈 Da espacio para el botón al final */
}

input[type='file'] {
  background-color: #1f1f1f;
  color: white;
  border: 1px solid #666;
  padding: 6px 10px;
  border-radius: 6px;
}

.progreso-carga .barra-externa {
  background: #333;
  border-radius: 10px;
  height: 24px;
  width: 100%;
  overflow: hidden;
  margin-top: 10px;
}

.progreso-carga .barra-interna {
  background: linear-gradient(90deg, #ffc107, #ff9800);
  height: 100%;
  transition: width 0.3s ease-in-out;
}


.table {
  font-size: 0.9rem;
}

.truncado {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  max-width: 180px;
}

.modal-descripcion {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-descripcion .contenido {
  background: #222;
  color: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}


.btn-cargar-firebase {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
  transition: all 0.3s ease;
  min-width: 220px;
  height: 50px;
  /* 👈 Evita cambios de altura en hover */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-cargar-firebase:hover {
  background-color: #218838;
  transform: scale(1.03);
  box-shadow: 0 6px 16px rgba(40, 167, 69, 0.5);
}

.text-muted {
  color: #bcbcbc !important;
}


.btn-cargar-firebase:disabled {
  background-color: #444 !important;
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: none;
}

.btn-cargar-firebase:focus,
.btn-cargar-firebase:active {
  outline: none;
  box-shadow: none;
}

.btn-vaciar {
  background: linear-gradient(135deg, #ff3c3c, #c80000);
  color: #fff;
  border: none;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(255, 60, 60, 0.3);
  transition: all 0.3s ease;
  height: 50px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
  margin-bottom: 10px;
}

.btn-vaciar::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  transition: left 0.3s ease;
}

.btn-vaciar:hover::after {
  left: 0;
}

.btn-vaciar:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(255, 60, 60, 0.4);
  background: linear-gradient(135deg, #ff1f1f, #a80000);
}

.btn-vaciar:disabled {
  background: #444 !important;
  opacity: 0.6;
  box-shadow: none;
  cursor: not-allowed;
}



@media (max-width: 576px) {
  .table {
    font-size: 0.75rem;
  }

  th,
  td {
    padding: 0.4rem;
  }

  .btn-cargar-firebase {
    width: 100%;
    min-width: unset;
  }
}
</style>

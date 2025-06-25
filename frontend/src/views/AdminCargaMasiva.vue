<template>
    <div class="admin-carga container-fluid py-5 text-white">
        <h1 class="titulo-principal text-center mb-4">
            <i class="fas fa-file-import me-2 text-white"></i>
            Carga Masiva de Productos
        </h1>
        

        <!-- 📂 Subida de archivo -->
        <div class="mb-4 text-center">
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

                <button class="btn-vaciar" :disabled="isCargando || productos.length === 0" @click="vaciarProductos">
                    <i class="fas fa-trash-alt me-2"></i>
                    Vaciar Productos
                </button>
            </div>


            <table class="table table-dark table-striped table-bordered">
                <thead>
                    <tr>
                        <th v-for="(col, index) in columnas" :key="index">{{ col }}</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(prod, idx) in productos" :key="idx">
                        <td v-for="col in columnas" :key="col">{{ prod[col] }}</td>
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
    <ModalEditarProducto v-if="mostrarModal" ref="modalEditarRef" :producto="productoSeleccionado"
        @guardar="guardarProducto" />

    <ToastNotificacion ref="toastRef" />

</template>



<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import * as XLSX from 'xlsx'
import axios from 'axios'
import ModalEditarProducto from '../components/Modals/ModalEditarProducto.vue'
import ToastNotificacion from '../components/ToastNotificacion.vue'

const productos = ref([])
const columnas = ref([])
const mostrarModal = ref(false)
const productoSeleccionado = ref({})
const modalEditarRef = ref(null)
const isCargando = ref(false)
const toastRef = ref(null)
const nombresExistentesEnDB = ref([])

const abrirModal = (producto) => {
  const copia = JSON.parse(JSON.stringify(producto))
  if (!copia.imagenCarrusel) copia.imagenCarrusel = []
  if (!copia.modelos) copia.modelos = []
  if (!copia.color) copia.color = ''
  if (!copia.precio) copia.precio = 0
  if (!copia.nombre) copia.nombre = ''
  if (!copia.descuento) copia.descuento = false
  if (!copia.tipoDescuento) copia.tipoDescuento = ''
  if (!copia.porcentajeDescuento) copia.porcentajeDescuento = 0
  if (!copia.montoDescuento) copia.montoDescuento = 0

  if (copia.modelos.length === 0) {
    copia.modelos.push({
      nombre: '',
      color: '',
      imagen: '',
      imagenCarrusel: [],
      precio: copia.precio || 0,
      descuento: false,
      tipoDescuento: '',
      porcentajeDescuento: 0,
      montoDescuento: 0,
      stockDisponible: 0,
      stockFisico: 0,
      oculto: false
    })
  }

  productoSeleccionado.value = copia
  mostrarModal.value = true

  nextTick(() => {
    modalEditarRef.value?.abrir?.()
  })
}

const handleArchivo = (e) => {
  const file = e.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (evt) => {
    const data = new Uint8Array(evt.target.result)
    const workbook = XLSX.read(data, { type: 'array' })
    const sheet = workbook.Sheets[workbook.SheetNames[0]]
    const json = XLSX.utils.sheet_to_json(sheet)

    const nombresActuales = productos.value.map(p => p.nombre?.trim().toLowerCase())
    const productosBase = []
    const productosModelos = []
    const duplicados = []

    for (const prod of json) {
      const nombre = prod.nombre?.trim()
      const nombreLower = nombre?.toLowerCase()
      const modeloDe = prod.modeloDe?.trim()?.toLowerCase()

      if (!nombre) continue

      const yaCargado =
        nombresActuales.includes(nombreLower) ||
        productosBase.some(p => p.nombre?.trim().toLowerCase() === nombreLower) ||
        nombresExistentesEnDB.value.includes(nombreLower)

      if (yaCargado) {
        duplicados.push(nombre)
        continue
      }

      if (modeloDe) {
        productosModelos.push({ ...prod, modeloDe })
      } else {
        productosBase.push({
          ...prod,
          modelos: []
        })
      }
    }

    for (const modelo of productosModelos) {
      const base = productosBase.find(p => p.nombre?.trim().toLowerCase() === modelo.modeloDe)
      const modeloObj = {
        nombre: modelo.nombre,
        color: modelo.color,
        imagen: modelo.imagen,
        imagenCarrusel: [],
        precio: modelo.precio || 0,
        descuento: modelo.descuento || false,
        tipoDescuento: modelo.tipoDescuento || '',
        porcentajeDescuento: modelo.porcentajeDescuento || 0,
        montoDescuento: modelo.montoDescuento || 0,
        stockDisponible: modelo.stockDisponible || 0,
        stockFisico: modelo.stockFisico || 0,
        oculto: false
      }

      if (base) {
        base.modelos.push(modeloObj)
      } else {
        productosBase.push({
          nombre: modelo.modeloDe,
          modelos: [modeloObj]
        })
      }
    }

    if (duplicados.length > 0) {
      toastRef.value.mostrar(
        '⚠️ Productos duplicados detectados',
        `Ya estaban cargados o se repiten:\n• ${duplicados.join('\n• ')}`,
        'warning'
      )
    }

    if (productosBase.length > 0) {
      toastRef.value.mostrar(
        '✅ Nuevos productos cargados',
        `Se agregaron ${productosBase.length} producto(s) base.`,
        'success'
      )
      productos.value.push(...productosBase)
      columnas.value = Object.keys(productos.value[0] || {})
    }

    e.target.value = ''
  }

  reader.readAsArrayBuffer(file)
}

const guardarProducto = async (productoActualizado) => {
  try {
    if (productoActualizado.id) {
      await axios.patch(`http://localhost:5000/api/products/${productoActualizado.id}`, productoActualizado)
    } else {
      await axios.post('http://localhost:5000/api/products', productoActualizado)
    }

    const index = productos.value.findIndex(p => p.nombre === productoActualizado.nombre)
    if (index !== -1) {
      productos.value[index] = JSON.parse(JSON.stringify(productoActualizado))
    }

    modalEditarRef.value?.cerrar?.()
    mostrarModal.value = false
    toastRef.value?.mostrar('✅ Producto actualizado', 'El producto fue guardado correctamente.', 'success')
  } catch (err) {
    console.error('Error al guardar producto:', err)
    toastRef.value?.mostrar('❌ Error', 'Hubo un problema al guardar el producto.', 'error')
  }
}

const cargarProductos = async () => {
  if (!productos.value.length) {
    toastRef.value?.mostrar('⚠️ Sin productos', 'No hay productos para cargar.', 'error')
    return
  }

  isCargando.value = true
  try {
    for (const producto of productos.value) {
      if (!producto.nombre || !producto.precio) {
        console.warn(`Producto incompleto:`, producto)
        continue
      }
      await axios.post('http://localhost:5000/api/products', producto)
    }

    toastRef.value?.mostrar('✅ Productos cargados', 'Todos los productos se cargaron exitosamente.', 'success')
    productos.value = []
    columnas.value = []
    localStorage.removeItem('productosExcel')
  } catch (error) {
    console.error('Error al cargar productos:', error)
    toastRef.value?.mostrar('❌ Error al cargar', 'Ocurrió un error al cargar los productos.', 'error')
  } finally {
    isCargando.value = false
  }
}

const vaciarProductos = () => {
  productos.value = []
  columnas.value = []
  localStorage.removeItem('productosExcel')
  toastRef.value?.mostrar('🧹 Productos eliminados', 'Se vació la lista de productos.', 'info')
}

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
})

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

.table {
    font-size: 0.9rem;
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

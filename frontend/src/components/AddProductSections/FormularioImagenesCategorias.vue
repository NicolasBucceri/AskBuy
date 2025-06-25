<template>
  <div>
    <div class="contenedorTituloSeccion">
      <h2 class="tituloFormulario">Imágenes y Categorías</h2>
    </div>

    <!-- Imagen principal -->
    <div class="formularioCampo">
      <label>Imagen Portada</label>
      <div class="contenedorBotonAgregar">
        <input type="text" v-model="product.imagen" placeholder="URL de la imagen principal"
          @input="actualizarVistaPreviaPortada" />
        <input type="file" ref="inputPortada" @change="subirImagenPortada" accept="image/*" hidden />
        <button class="btnAgregar" v-if="!product.imagen" @click="seleccionarImagenPortada">
          <i class="fas fa-upload"></i>
        </button>
        <button class="btnEliminar" v-if="product.imagen" @click="borrarImagenPortada">
          <i class="fas fa-trash"></i>
        </button>
      </div>
    </div>

    <!-- Carrusel -->
    <div class="formularioCampo">
      <label>Imágenes del Carrusel</label>
      <div v-for="(img, index) in product.imagenCarrusel" :key="index" class="input-group">
        <div class="contenedorBotonAgregar">
          <input type="text" v-model="product.imagenCarrusel[index]" placeholder="URL de la imagen secundaria" />
          <input type="file" :ref="el => inputImagenCarruselRefs[index] = el"
            @change="subirImagenCarrusel($event, index)" accept="image/*" hidden />

          <button class="btnAgregar" @click="seleccionarImagenCarruselProductoBase(index)">
            <i class="fas fa-upload"></i>
          </button>
          <button class="btnEliminar" @click="eliminarCampo(index)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
      <div class="btnAgregarCarrusel">
        <button v-if="product.imagenCarrusel.length < 6" class="btnAgregarImg" @click="agregarImagenCarrusel">
          <i class="fas fa-plus"></i> Agregar Imagen
        </button>
        <p class="limiteCarrusel">{{ product.imagenCarrusel.length }} / 6 imágenes agregadas</p>
      </div>
    </div>

    <!-- Categoría -->
    <div class="formularioCampo">
      <label>Categoría:</label>
      <div class="contenedorSelector">
        <select v-model="product.categoria" :key="selectKey">
          <option v-for="cat in categorias" :key="cat.nombre" :value="cat.nombre">
            {{ cat.nombre }}
          </option>
        </select>
        <button class="btnAgregar" data-bs-toggle="modal" data-bs-target="#modalAgregarCategoria">
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>


    <!-- Etiquetas -->
    <div class="formularioCampo">
      <label>Etiquetas:</label>
      <div class="contenedorSelector">
        <select v-model="nuevaEtiquetaSeleccionada" @change="agregarEtiqueta">
          <option disabled value="">Selecciona una etiqueta</option>
          <option v-for="etiqueta in etiquetasDisponibles" :key="etiqueta.nombre || etiqueta" :value="etiqueta">
            {{ etiqueta.nombre || "Etiqueta sin nombre" }}
          </option>
        </select>
        <button class="btnAgregar" data-bs-toggle="modal" data-bs-target="#modalAgregarEtiqueta">
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>

    <!-- Botones -->
    <div class="contenedorBoton">
      <button class="btnFormulario btnAtras" @click="$emit('volver')">Atrás</button>
      <button class="btnFormulario btnSiguiente" @click="$emit('siguiente')">Siguiente</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps({
  product: Object,
})

// Refs
const categorias = ref([])
const etiquetasDisponibles = ref([])
const nuevaEtiquetaSeleccionada = ref("")
const selectKey = ref(0)
const inputImagenCarruselRefs = ref([])
const inputPortada = ref(null)

// 📥 API: Categorías
const fetchCategorias = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/categorias")
    categorias.value = res.data.map(cat => ({ nombre: cat.nombre || cat }))
  } catch (err) {
    console.error("Error cargando categorías", err)
  }
}

// 📥 API: Etiquetas
const fetchEtiquetas = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/etiquetas")
    etiquetasDisponibles.value = res.data
  } catch (err) {
    console.error("Error cargando etiquetas", err)
  }
}

// ➕ Agregar etiqueta al producto
const agregarEtiqueta = () => {
  const nombreEtiqueta = nuevaEtiquetaSeleccionada.value?.nombre
  if (nombreEtiqueta && !props.product.etiquetas.includes(nombreEtiqueta)) {
    props.product.etiquetas.push(nombreEtiqueta)
  }
  nuevaEtiquetaSeleccionada.value = ""
}

// 📤 Imagen portada
const seleccionarImagenPortada = () => inputPortada.value?.click()
const subirImagenPortada = (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    props.product.imagen = reader.result
  }
  reader.readAsDataURL(file)
}
const borrarImagenPortada = () => {
  props.product.imagen = ""
  if (inputPortada.value) inputPortada.value.value = null
}

// 🎠 Carrusel imágenes
const seleccionarImagenCarruselProductoBase = (index) => {
  const input = inputImagenCarruselRefs.value[index]
  if (input) input.click()
}
const subirImagenCarrusel = (event, index) => {
  const file = event.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    props.product.imagenCarrusel[index] = reader.result
  }
  reader.readAsDataURL(file)
}
const eliminarCampo = (index) => {
  props.product.imagenCarrusel.splice(index, 1)
}
const agregarImagenCarrusel = () => {
  if (props.product.imagenCarrusel.length < 6) {
    props.product.imagenCarrusel.push("")
  }
}

// 🔁 Actualizar al cerrar modales
onMounted(async () => {
  await fetchCategorias()
  await fetchEtiquetas()

  await nextTick()

  // 🔄 Modal Categoría
  const modalCategoria = document.getElementById('modalAgregarCategoria')
  if (modalCategoria) {
    modalCategoria.addEventListener('hidden.bs.modal', async () => {
      await fetchCategorias()
      selectKey.value++ // Re-render de select de categorías
    })
  }

  // 🔄 Modal Etiqueta
  const modalEtiqueta = document.getElementById('modalAgregarEtiqueta')
  if (modalEtiqueta) {
    modalEtiqueta.addEventListener('hidden.bs.modal', async () => {
      await fetchEtiquetas()
    })
  }
})
</script>



<style scoped>
.contenedorTituloSeccion {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -30px;
  margin-bottom: 20px;
}

.tituloFormulario {
  font-size: 1.25rem;
  text-align: center;
  margin-bottom: 1rem;
  color: var(--colorTextoSecundario);
}

.formularioCampo {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 20px;
}

.formularioCampo label {
  font-weight: bold;
  font-size: 1rem;
  color: var(--colorTextoSecundario);
}

.formularioCampo input[type="text"],
.formularioCampo select {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fff;
}

.formularioCampo input:focus,
.formularioCampo select:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 8px rgba(226, 211, 74, 0.3);
  outline: none;
}

.formularioCampo select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-color: #fff;
  background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23FFC107' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
  padding-right: 2.5rem;
  color: #333;
}

.formularioCampo select:hover,
.formularioCampo select:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.3);
  outline: none;
}

.formularioCampo select option {
  padding: 10px;
}

.contenedorSelector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contenedorSelector select {
  flex: 1;
  padding: 10px 14px;
  border-radius: 10px;
  border: 2px solid #ddd;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.contenedorSelector select:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 5px rgba(226, 211, 74, 0.3);
  outline: none;
}

.contenedorBotonAgregar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btnAgregar,
.btnEliminar {
  padding: 8px 12px;
  font-size: 0.9rem;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.btnAgregar {
  background-color: var(--colorSecundario);
  color: white;
}

.btnAgregar:hover {
  background-color: var(--colorSecundarioHover);
}

.btnEliminar {
  background-color: var(--colorError);
  color: white;
}

.btnEliminar:hover {
  background-color: var(--colorErrorHover);
}

.btnAgregarImg {
  background-color: var(--colorTerciario);
  color: white;
  font-weight: 600;
  padding: 10px 16px;
  border: none;
  border-radius: 25px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btnAgregarImg:hover {
  background-color: var(--colorTerciarioHover);
}

.btnAgregarCarrusel {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
  gap: 5px;
}

.limiteCarrusel {
  margin-top: 10px;
  color: white;
}

.contenedorBoton {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  gap: 20px;
}

.btnFormulario {
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btnFormulario.btnAtras {
  background-color: var(--colorSecundario);
  color: white;
}

.btnFormulario.btnAtras:hover {
  background-color: var(--colorSecundarioHover);
}

.btnFormulario.btnSiguiente {
  background-color: var(--colorTerciario);
  color: white;
}

.btnFormulario.btnSiguiente:hover {
  background-color: var(--colorTerciarioHover);
}

</style>
<template>
  <div class="form-edicion">

    <!-- Imagen Portada -->
    <div class="campo-form full-width">
      <label>Imagen Portada:</label>
      <div class="input-con-botones">
        <input type="text" v-model="modelo.imagen" placeholder="URL de imagen" />
        <button @click="abrirInputImagenPortada" class="btnAgregar" title="Subir imagen">
          <i class="fas fa-upload"></i>
        </button>
        <button @click="borrarImagenPortada" class="btnEliminar" title="Eliminar imagen">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <input type="file" :ref="'fileInputEditar' + index" @change="subirImagenModeloEditar" hidden accept="image/*" />
    </div>

    <!-- Carrusel -->
    <div class="campo-form full-width">
      <label>Imágenes Carrusel:</label>
      <div v-for="(img, i) in modelo.imagenCarrusel" :key="i" class="input-carrusel">
        <input type="text" v-model="modelo.imagenCarrusel[i]" placeholder="URL carrusel" />
        <button @click.prevent="abrirInputImagenCarrusel(i)" class="btnAgregar" title="Subir">
          <i class="fas fa-upload"></i>
        </button>
        <input type="file" ref="fileInput" style="display: none" @change="(e) => cargarImagenCarrusel(i, e)"
          accept="image/*" />
        <button @click="modelo.imagenCarrusel.splice(i, 1)" class="btnEliminar" title="Eliminar">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <div class="btnAgregarCarrusel">
        <button @click="modelo.imagenCarrusel.push('')" class="btnAgregarImg">+ Agregar Imagen</button>
      </div>
    </div>

    <!-- Fila 1 -->
    <div class="grid-row">
      <div class="campo-form">
        <label>Nombre:</label>
        <input type="text" v-model="modelo.nombre" />
      </div>
      <div class="campo-form">
        <label>Color:</label>
        <input type="text" v-model="modelo.color" />
      </div>
      <div class="campo-form">
        <label>Precio:</label>
        <input type="text" :value="formatPrecio(modelo.precio)" @input="actualizarPrecio($event.target.value)"
          inputmode="numeric" />
      </div>

      <div class="custom-checkbox">
        <input type="checkbox" id="aplicaDescuento" v-model="modelo.aplicaDescuento" />
        <label for="aplicaDescuento">
          <span class="checkbox-icon"></span>
          Aplicar Descuento
        </label>
      </div>


    </div>

    <!-- Fila 2 -->
    <div class="grid-row" v-if="modelo.aplicaDescuento">
      <div class="campo-form">
        <label>Tipo de Descuento:</label>
        <select v-model="modelo.tipoDescuento">
          <option value="porcentaje">Porcentaje (%)</option>
          <option value="monto">Monto Fijo ($)</option>
        </select>
      </div>
      <div class="campo-form" v-if="modelo.tipoDescuento === 'porcentaje'">
        <label>Porcentaje:</label>
        <input type="number" v-model.number="modelo.porcentajeDescuento" min="0" max="100" />
      </div>
      <div class="campo-form" v-if="modelo.tipoDescuento === 'monto'">
        <label>Monto Fijo:</label>
        <input type="number" v-model.number="modelo.montoDescuento" min="0" />
      </div>
      <div class="campo-form">
        <label>Precio con Descuento:</label>
        <input type="text" :value="precioConDescuento(modelo)" readonly />

      </div>
    </div>

    <!-- Fila 3 -->
    <div class="fila-stock">
      <div class="campo-form">
        <label>Stock Disponible:</label>
        <input type="number" v-model.number="modelo.stockDisponible" @blur="$emit('validar-stock', modelo)" />
      </div>
      <div class="campo-form">
        <label>Stock Físico:</label>
        <input type="number" v-model.number="modelo.stockFisico" @blur="$emit('validar-stock', modelo)" />
      </div>
      <div class="campo-form switch-container">
        <label class="switch-label">
          <input type="checkbox" v-model="modelo.oculto"
            @change="$emit('toggle-ocultar', index, $event.target.checked)" />
          <span class="switch-slider"></span>
          Ocultar Modelo
        </label>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'

const props = defineProps({
  modelo: Object,
  index: Number,
  precioConDescuento: Function
})

const modelo = props.modelo
const index = props.index
const precioConDescuento = props.precioConDescuento

const { proxy } = getCurrentInstance()

const emit = defineEmits([
  'seleccionar-imagen-principal',
  'subir-imagen',
  'abrir-explorador',
  'cargar-imagen',
  'validar-stock',
  'toggle-ocultar'
])

// ✅ Eliminar imagen portada
function borrarImagenPortada() {
  modelo.imagen = ''

  // Limpiar input file (por si se subió desde archivo)
  const refKey = `fileInputEditar${index}`
  const input = proxy?.$refs?.[refKey]
  if (input) input.value = ''

  mostrarToast('🗑️ Imagen portada eliminada.')
}

// ✅ Subir imagen en base64
function subirImagenModeloEditar(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    modelo.imagen = e.target.result
  }
  reader.readAsDataURL(file)
}

function abrirInputImagenCarrusel(i) {
  const input = proxy?.$refs?.fileInput?.[i]
  if (input) input.click()
  else mostrarToast('⚠️ No se pudo acceder al input de imagen carrusel.')
}


function cargarImagenCarrusel(i, event) {
  const file = event?.target?.files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      modelo.imagenCarrusel.splice(i, 1, e.target.result)
    }
    reader.readAsDataURL(file)
  }
}

// ✅ Validar stock
function validarStockModelo(modelo) {
  if (modelo.stockDisponible > modelo.stockFisico) {
    modelo.stockDisponible = modelo.stockFisico
    mostrarToast('⚠️ El stock disponible no puede superar el stock físico')
  }
}

// ✅ Toggle ocultar modelo
function toggleOcultarModelo(index, oculto) {
  const mensaje = oculto
    ? '👻 Modelo ocultado correctamente.'
    : '👁️ Modelo ahora es visible en la tienda.'

  mostrarToast(mensaje)
}


// ✅ Formatear moneda ARS
function formatNumber(value) {
  return value ? new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value) : "$0"
}

// ✅ Toast visual
function mostrarToast(mensaje) {
  const toastEl = document.getElementById('liveToast')
  if (!toastEl) return
  const toastBody = toastEl.querySelector('.toast-body')
  if (toastBody) toastBody.textContent = mensaje

  toastEl.classList.remove('text-bg-success', 'text-bg-danger', 'text-bg-warning')
  toastEl.classList.add('text-bg-dark')

  const toast = new bootstrap.Toast(toastEl)
  toast.show()
}



function abrirInputImagenPortada() {
  const refKey = `fileInputEditar${index}`
  const input = proxy?.$refs?.[refKey]
  if (input) input.click()
}

function formatPrecio(valor) {
  if (!valor) return ''
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0
  }).format(valor)
}

function actualizarPrecio(valor) {
  // Elimina cualquier caracter que no sea número
  const soloNumeros = valor.replace(/\D/g, '')
  modelo.precio = parseInt(soloNumeros) || 0
}


</script>



<style scoped>
.form-edicion {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6);
  color: var(--colorTextoSecundario);
  width: 100%;
}

/* Campos */
.campo-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.campo-form label {
  font-weight: 600;
  font-size: 14px;
  color: var(--colorTerciario);
}

input[type="text"],
input[type="number"],
select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  padding: 10px 14px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  transition: border-color 0.3s;
  width: 100%;
}

input:focus,
select:focus {
  border-color: var(--colorTerciario);
  outline: none;
}

/* Botones */
.btnAgregar,
.btnAgregarImg,
.btnEliminar {
  background-color: var(--colorTerciario);
  border: none;
  color: var(--colorTextoPrincipal);
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.btnAgregar:hover,
.btnAgregarImg:hover {
  background-color: var(--colorTerciarioHover);
}

.btnEliminar {
  background-color: var(--colorError);
  color: white;
}

.btnEliminar:hover {
  background-color: var(--colorErrorHover);
}

/* Carrusel */
.input-carrusel {
  display: flex;
  gap: 10px;
  align-items: center;
}

.input-carrusel input[type="text"] {
  flex: 1;
}

/* Carrusel grupo */
.btnAgregarCarrusel {
  display: flex;
  justify-content: flex-start;
  margin-top: 10px;
}

/* Switch Ocultar */
.switch-container {
  display: flex;
  align-items: center;
  /* centra verticalmente */
  height: 100%;
  /* asegura que tome el alto del contenedor */
  margin-top: 14%;
  /* elimina margen innecesario */
}


.switch-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.switch-label input[type="checkbox"] {
  display: none;
}

.switch-slider {
  position: relative;
  width: 52px;
  height: 28px;
  background-color: #555;
  border-radius: 34px;
  transition: background-color 0.3s ease;
}

.switch-slider::before {
  content: "";
  position: absolute;
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

input[type="checkbox"]:checked+.switch-slider {
  background-color: var(--colorTerciario);
}

input[type="checkbox"]:checked+.switch-slider::before {
  transform: translateX(24px);
}

/* Grillas internas */
.grid-row,
.fila-stock {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.input-con-botones {
  display: flex;
  align-items: center;
  gap: 10px;
  /* <-- aumentamos esto */
}

.custom-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--colorTextoSecundario);
  cursor: pointer;
  user-select: none;
}

.custom-checkbox input[type="checkbox"] {
  display: none;
}

.custom-checkbox label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-icon {
  width: 20px;
  height: 20px;
  border: 2px solid var(--colorTerciario);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  transition: background-color 0.2s, border-color 0.2s;
  position: relative;
}

input[type="checkbox"]:checked + label .checkbox-icon {
  background-color: var(--colorTerciario);
  border-color: var(--colorTerciario);
}

.checkbox-icon::after {
  content: '';
  width: 10px;
  height: 5px;
  border-left: 2px solid rgb(0, 0, 0);
  border-bottom: 2px solid rgb(0, 0, 0);
  transform: rotate(-45deg);
  opacity: 0;
  transition: opacity 0.2s ease;
}

input[type="checkbox"]:checked + label .checkbox-icon::after {
  opacity: 1;
}

</style>

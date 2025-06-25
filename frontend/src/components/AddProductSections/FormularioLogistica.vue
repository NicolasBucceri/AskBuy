<template>
  <div>
    <div class="contenedorTituloSeccion">
      <h2 class="tituloFormulario">Logística</h2>
    </div>

    <!-- Stock Físico -->
    <div class="formularioCampo">
      <label>Stock Físico:</label>
      <input type="number" v-model.number="product.stockFisico" @blur="validarStockProducto" class="form-control" />
    </div>

    <!-- Stock Disponible -->
    <div class="formularioCampo">
      <label>Stock Disponible:</label>
      <input type="number" v-model.number="product.stockDisponible" @blur="validarStockProducto" class="form-control" />
    </div>

    <div class="campo-form ocultar-modelo-centrado">
      <label class="switch-label texto-blanco">
        <input type="checkbox" v-model="product.ocultar" class="switch-input"
          @change="toggleOcultarModeloTemporal($event.target.checked)" />
        <span class="switch-slider"></span>
        Ocultar Publicación
      </label>
    </div>

    <div class="contenedorBoton">
      <button v-if="activeSection > 1" class="btnFormulario btnAtras" @click="$emit('volver')">
        Atrás
      </button>
      <button class="btnFormulario" @click="emit('submit')">
        Agregar Producto
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:product', 'submit'])

// Actualiza stock disponible si supera al físico
watch(() => props.product.stockDisponible, (nuevo) => {
  if (nuevo > props.product.stockFisico) {
    props.product.stockDisponible = props.product.stockFisico
    statusMessage.value = '⚠️ El stock disponible no puede ser mayor al stock físico'
  } else {
    statusMessage.value = ''
  }
})

const validarStockProducto = () => {
  if (props.product.stockDisponible > props.product.stockFisico) {
    props.product.stockDisponible = props.product.stockFisico
    statusMessage.value = '⚠️ El stock disponible no puede superar el stock físico'
  } else {
    statusMessage.value = ''
  }
}

const toggleOcultarModeloTemporal = (nuevoValor) => {
  const mensaje = nuevoValor
    ? "👻 Este modelo será ocultado cuando lo publiques."
    : "👁️ Este modelo será visible para los usuarios.";
  emit('toast', mensaje);
}

</script>


<style scoped>
.formularioCampo {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 15px;
}

.formularioCampo label {
  font-weight: bold;
  font-size: 1rem;
  color: var(--colorTextoSecundario);
}

.formularioCampo input,
.formularioCampo select,
.formularioCampo textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fff;
}

.formularioCampo input:focus,
.formularioCampo select:focus,
.formularioCampo textarea:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 8px rgba(226, 211, 74, 0.3);
  outline: none;
}

.switch-label {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.4rem;
  font-weight: 600;
  cursor: pointer;
}

.switch-label input[type="checkbox"] {
  display: none;
}

.switch-slider {
  position: relative;
  width: 60px;
  height: 30px;
  background-color: #ccc;
  border-radius: 34px;
  transition: background-color 0.3s;
}

.switch-slider::before {
  content: "";
  position: absolute;
  height: 26px;
  width: 26px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
}

.switch-label input[type="checkbox"]:checked+.switch-slider {
  background-color: var(--colorTerciario);
}

.switch-label input[type="checkbox"]:checked+.switch-slider::before {
  transform: translateX(30px);
}

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
}

.contenedorBoton {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  width: 100%;
}

.btnFormulario {
  background-color: var(--colorTerciario);
  padding: 12px;
  border-radius: 10px;
  color: white;
  transition: all 0.3s ease;
  font-weight: bold;
}

.btnFormulario:hover {
  background-color: var(--colorTerciarioHover);
}

.btnAtras {
  background-color: var(--colorSecundario);
}

.btnAtras:hover {
  background-color: var(--colorSecundarioHover);
}

.status-message {
  margin-top: 10px;
  font-weight: 500;
  color: var(--colorSecundario);
}

.texto-blanco {
  color: var(--colorTextoSecundario);
  /* o #ffc107 si querés a mano */
  font-weight: 500;
}
</style>

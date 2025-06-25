<template>
  <div>
    <div class="contenedorTituloSeccion">
      <h2 class="tituloFormulario">Información del Producto</h2>
    </div>

    <div class="formularioCampo">
      <label>Marca:</label>
      <input type="text" v-model="product.marca" required />
    </div>

    <div class="formularioCampo">
      <label>Nombre:</label>
      <input type="text" v-model="product.nombre" required />
    </div>

    <div class="formularioCampo">
      <label>Color:</label>
      <input type="text" v-model="product.colorPrincipal" placeholder="Ejemplo: Rojo, Azul, Negro" required />
    </div>

    <div class="formularioCampo">
      <label>Precio:</label>
      <input type="text" :value="formattedPrecio" @input="formatInput($event, 'precio')" required />
    </div>



    <div class="formularioCampo filaCheckbox">
      <label for="checkboxDescuento">Aplicar Descuento:</label>
      <input id="checkboxDescuento" type="checkbox" v-model="product.descuento" class="checkboxDescuento" />
    </div>

    <!-- SOLO SE MUESTRA SI HAY DESCUENTO ACTIVADO -->
    <div v-if="product.descuento">
      <div class="filaDescuento">
        <div class="formularioCampo">
          <label>Descuento:</label>
          <select v-model="product.tipoDescuento">
            <option value="porcentaje">Porcentaje (%)</option>
            <option value="monto">Monto Fijo ($)</option>
          </select>
        </div>

        <div class="formularioCampo" v-if="product.tipoDescuento === 'porcentaje'">
          <label>Porcentaje:</label>
          <input type="number" v-model.number="product.porcentajeDescuento" />
        </div>

        <div class="formularioCampo" v-if="product.tipoDescuento === 'monto'">
          <label>Monto:</label>
          <input type="text" :value="formattedMontoDescuento" @input="formatInput($event, 'montoDescuento')" />
        </div>

        <div class="formularioCampo precioFinal">
          <label>Total:</label>
          <input type="text" :value="precioConDescuento" readonly />
        </div>
      </div>

      <div class="filaFechaHora">
        <div class="formularioCampo">
          <label>Válido hasta (fecha):</label>
          <input type="date" v-model="product.fechaVencimientoDescuento" />
        </div>

        <div class="formularioCampo">
          <label>Hora límite:</label>
          <input type="time" v-model="product.horaVencimientoDescuento" />
        </div>
      </div>

    </div>

    <div class="contenedorBoton">
      <button class="btnFormulario" @click="$emit('irSiguiente')">
        Siguiente
      </button>
    </div>
  </div>

</template>

<script setup>
import { computed } from 'vue';
// En script setup
const props = defineProps({
  product: Object,
});

function formatInput(event, field) {
  let value = event.target.value.replace(/\D/g, "");
  props.product[field] = Number(value) || 0;
}

const formattedPrecio = computed(() => formatNumber(props.product.precio));
const formattedMontoDescuento = computed(() =>
  formatNumber(props.product.montoDescuento)
);
const precioConDescuento = computed(() => {
  if (!props.product.descuento || !props.product.precio) {
    return formatNumber(props.product.precio);
  }
  let precioFinal = props.product.precio;
  if (
    props.product.tipoDescuento === "porcentaje" &&
    props.product.porcentajeDescuento
  ) {
    precioFinal -=
      (props.product.precio * props.product.porcentajeDescuento) / 100;
  } else if (
    props.product.tipoDescuento === "monto" &&
    props.product.montoDescuento
  ) {
    precioFinal -= props.product.montoDescuento;
  }
  return formatNumber(precioFinal);
});

function formatNumber(value) {
  return value
    ? new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: "ARS",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
    : "$0";
}
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
  gap: 5px;
  margin-bottom: 15px;
}

.formularioCampo label {
  font-weight: bold;
  font-size: 1rem;
  color: var(--colorTextoSecundario);
}

.formularioCampo input,
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

.contenedorBoton {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
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

.contenedorCheckbox {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 1rem;
  color: #3a3a3a;
  width: 100%;
}

.checkboxDescuento {
  width: 18px;
  height: 18px;
  accent-color: var(--colorTerciario);
  cursor: pointer;
}

.filaCheckbox {
  flex-direction: row !important;
  align-items: center;
  justify-content: space-between;
  display: flex;
  gap: 20px;
  /* Espacio entre texto y checkbox */
}

.filaCheckbox label {
  margin: 0;
  white-space: nowrap;
  flex: 1;
  /* Ocupa todo el ancho disponible a la izquierda */
}

.filaCheckbox .checkboxDescuento {
  width: 18px;
  height: 18px;
  margin-right: 10px;
}


.filaDescuento,
.filaFechaHora {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filaDescuento {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filaDescuento .formularioCampo {
  flex: 1 1 30%;
  min-width: 150px;
}

/* Si querés que "Precio con Descuento" pese menos */
.filaDescuento .precioFinal {
  flex: 1 1 25%;
}
</style>

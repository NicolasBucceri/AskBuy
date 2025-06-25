<template>
  <div v-if="activeSection === 4">
    <div class="contenedorTituloSeccion">
      <h2 class="tituloFormulario">Variaciones del Producto</h2>
    </div>

    <!-- Nombre -->
    <div class="formularioCampo">
      <label>Nombre:</label>
      <input type="text" v-model="modeloTemporal.nombre" class="form-control" placeholder="Ejemplo: Modelo Pro" />
    </div>

    <!-- Color -->
    <div class="formularioCampo">
      <label>Color:</label>
      <input type="text" v-model="modeloTemporal.color" class="form-control" placeholder="Ejemplo: Negro Mate" />
    </div>

    <!-- Imagen Principal -->
    <div class="formularioCampo">
      <label>Imagen Portada:</label>
      <div class="contenedorBotonAgregar">
        <input type="text" v-model="modeloTemporal.imagen" class="form-control" placeholder="URL de la imagen" />
        <input type="file" ref="inputImagenModelo" @change="handleImagenModeloPrincipal" accept="image/*" hidden />
        <button @click="seleccionarImagenModeloPrincipal" class="btnAgregar btnImagenPortada">
          <i class="fas fa-upload"></i>
        </button>
        <button v-if="modeloTemporal.imagen" @click="eliminarImagenModelo" class="btnEliminar">
          <i class="fas fa-trash"></i>
        </button>
      </div>
    </div>

    <!-- Carrusel -->
    <div class="formularioCampo">
      <label>Imágenes del Carrusel:</label>
      <div v-for="(img, index) in modeloTemporal.imagenCarrusel" :key="index" class="contenedorImagenCarrusel">
        <input type="text" v-model="modeloTemporal.imagenCarrusel[index]" class="form-control" placeholder="URL" />
        <input type="file" :ref="'inputModeloCarrusel' + index" @change="subirImagenCarruselModelo($event, index)"
          accept="image/*" hidden />
        <button @click="seleccionarImagenCarruselModelo(index)" class="btnAgregar btnCarrusel">
          <i class="fas fa-upload"></i>
        </button>
        <button @click="modeloTemporal.imagenCarrusel.splice(index, 1)" class="btnEliminar">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <div class="btnAgregarCarrusel">
        <button v-if="modeloTemporal.imagenCarrusel.length < 6" @click="modeloTemporal.imagenCarrusel.push('')"
          class="btnAgregar btnCarrusel mt-2">
          <i class="fas fa-plus"></i> Agregar Imagen
        </button>
        <p class="limiteImagenes">{{ modeloTemporal.imagenCarrusel.length }} / 6 imágenes agregadas</p>
      </div>
    </div>

    <!-- Precio -->
    <div class="formularioCampo">
      <label>Precio:</label>
      <input type="text" :value="formatNumber(modeloTemporal.precio)" @input="formatModeloPrecio($event)"
        class="form-control" placeholder="Ejemplo: 10.000" />
    </div>

    <!-- Descuento -->
    <div class="formularioCampo filaCheckbox">
      <label for="checkboxDescuento">Aplicar Descuento:</label>
      <input id="checkboxDescuento" type="checkbox" v-model="modeloTemporal.descuento" class="checkboxDescuento" />
    </div>

    <div v-if="modeloTemporal.descuento">
      <div class="filaDescuento">
        <div class="formularioCampo">
          <label>Descuento:</label>
          <select v-model="modeloTemporal.tipoDescuento">
            <option value="porcentaje">Porcentaje (%)</option>
            <option value="monto">Monto Fijo ($)</option>
          </select>
        </div>

        <div class="formularioCampo" v-if="modeloTemporal.tipoDescuento === 'porcentaje'">
          <label>Porcentaje:</label>
          <input type="number" v-model.number="modeloTemporal.porcentajeDescuento" />
        </div>

        <div class="formularioCampo" v-if="modeloTemporal.tipoDescuento === 'monto'">
          <label>Monto:</label>
          <input type="text" :value="formattedMontoDescuentoModelo"
            @input="formatInputModelo($event, 'montoDescuento')" />
        </div>

        <div class="formularioCampo precioFinal">
          <label>Total:</label>
          <input type="text" :value="precioConDescuentoModelo(modeloTemporal)" readonly />
        </div>
      </div>

      <div class="filaFechaHora">
        <div class="formularioCampo">
          <label>Válido hasta (fecha):</label>
          <input type="date" v-model="modeloTemporal.fechaVencimientoDescuento" />
        </div>

        <div class="formularioCampo">
          <label>Hora límite:</label>
          <input type="time" v-model="modeloTemporal.horaVencimientoDescuento" />
        </div>
      </div>
    </div>

    <!-- Stock -->
    <div class="formularioCampo">
      <label>Stock Físico:</label>
      <input type="number" v-model.number="modeloTemporal.stockFisico" min="0" @blur="validarStock('fisico')"
        class="form-control" />
    </div>

    <div class="formularioCampo">
      <label>Stock Disponible:</label>
      <input type="number" v-model.number="modeloTemporal.stockDisponible" min="0" @blur="validarStock('disponible')"
        class="form-control" />
    </div>

    <!-- Ocultar -->
<label class="switch-label">
  <input type="checkbox" v-model="modeloTemporal.oculto" class="switch-input"
    @change="toggleOcultarModeloTemporal($event.target.checked)" />
  <span class="switch-slider"></span>
  <span class="texto-ocultar">Ocultar Modelo</span>
</label>


    <!-- Botones -->
    <div class="contenedorBoton">
      <button class="btnVerModelos" data-bs-toggle="modal" data-bs-target="#modalModelos">Ver Modelos</button>
      <button class="btn agregarModelos" @click="agregarModelo">Agregar Modelo</button>
    </div>

    <div class="contenedorBoton">
      <button class="btnFormulario btnAtras" @click="$emit('volver')">Atrás</button>
      <button class="btnFormulario" @click="$emit('siguiente')">Siguiente</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    activeSection: Number,
    product: Object,
    modeloTemporal: Object,
    modeloSeleccionado: Number,
    formattedMontoDescuentoModelo: String
  },
  emits: ['volver', 'siguiente', 'toast'],
  watch: {
    modeloTemporal: {
      handler(newVal) {
        localStorage.setItem("draft.modeloTemporal", JSON.stringify(newVal));
      },
      deep: true
    }
  },
  mounted() {
    const borrador = localStorage.getItem("draft.modeloTemporal");
    if (borrador) {
      Object.assign(this.modeloTemporal, JSON.parse(borrador));
    }
  },
  methods: {
agregarModelo() {
  if (!this.modeloTemporal.nombre || !this.modeloTemporal.precio) {
    alert("Debes completar todos los campos del modelo.");
    return;
  }

  if (
    this.modeloTemporal.descuento &&
    (!this.modeloTemporal.fechaVencimientoDescuento || !this.modeloTemporal.horaVencimientoDescuento)
  ) {
    alert("Por favor completá la fecha y hora del vencimiento del descuento.");
    return;
  }

  // 🧠 Le asignás un ID único
  const nuevoModelo = {
    ...this.modeloTemporal,
    id: crypto.randomUUID(), // <- Esto es lo que te faltaba
    imagenCarrusel: [...this.modeloTemporal.imagenCarrusel],
  };

  this.product.modelos.push(nuevoModelo);
  this.$emit('toast', "✅ Modelo agregado");
  this.resetearModeloTemporal();
},
    resetearDescuento() {
      if (this.modeloTemporal.descuento) {
        this.modeloTemporal.tipoDescuento = "porcentaje";
        this.modeloTemporal.porcentajeDescuento = 0;
        this.modeloTemporal.montoDescuento = 0;
      }
    },
    formatModeloPrecio(event) {
      const rawValue = event.target.value.replace(/\D/g, "");
      this.modeloTemporal.precio = Number(rawValue) || 0;
    },
    formatInputModelo(event, field) {
      let rawValue = event.target.value.replace(/\D/g, "");
      let numericValue = Number(rawValue);
      this.modeloTemporal[field] = numericValue;
      event.target.value = this.formatNumber(numericValue);
    },
    precioConDescuentoModelo(modelo) {
      if (!modelo.descuento || !modelo.precio) {
        return this.formatNumber(modelo.precio);
      }

      let precio = modelo.precio;

      if (modelo.tipoDescuento === "porcentaje") {
        precio -= (precio * modelo.porcentajeDescuento) / 100;
      } else if (modelo.tipoDescuento === "monto") {
        precio -= modelo.montoDescuento;
      }

      return this.formatNumber(precio);
    },
    formatNumber(value) {
      return value
        ? new Intl.NumberFormat("es-AR", {
          style: "currency",
          currency: "ARS",
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }).format(value)
        : "$0";
    },
    validarStock(tipo) {
      const disponible = this.modeloTemporal.stockDisponible || 0;
      const fisico = this.modeloTemporal.stockFisico || 0;
      if (disponible > fisico) {
        this.modeloTemporal.stockDisponible = fisico;
        this.$emit('toast', "⚠️ El stock disponible no puede superar al stock físico.");
      }
    },
    toggleOcultarModeloTemporal(nuevoValor) {
      const mensaje = nuevoValor
        ? "👻 Este modelo será ocultado cuando lo publiques."
        : "👁️ Este modelo será visible para los usuarios.";
      this.$emit('toast', mensaje);
    },
    seleccionarImagenModeloPrincipal() {
      this.$refs.inputImagenModelo.click();
    },
    handleImagenModeloPrincipal(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        this.modeloTemporal.imagen = reader.result;
      };
      reader.readAsDataURL(file);
    },
    eliminarImagenModelo() {
      this.modeloTemporal.imagen = "";
    },
    subirImagenCarruselModelo(event, index) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        this.modeloTemporal.imagenCarrusel[index] = reader.result;
      };
      reader.readAsDataURL(file);
    },
    seleccionarImagenCarruselModelo(index) {
      const ref = this.$refs[`inputModeloCarrusel${index}`];
      if (Array.isArray(ref)) {
        ref[0]?.click();
      } else {
        ref?.click();
      }
    },
    resetearModeloTemporal() {
      Object.assign(this.modeloTemporal, {
        nombre: "",
        color: "",
        imagen: "",
        precio: 0,
        descuento: false,
        tipoDescuento: "porcentaje",
        porcentajeDescuento: 0,
        montoDescuento: 0,
        imagenCarrusel: [],
        stockDisponible: 0,
        stockFisico: 0,
        oculto: false,
        fechaVencimientoDescuento: "",
        horaVencimientoDescuento: "",
      });

      localStorage.removeItem("draft.modeloTemporal");
    }


  }
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
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  width: 100%;
}

.btnVerModelos {
  background: var(--colorSecundario);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.3s ease;
}

.btnVerModelos:hover {
  background: var(--colorSecundarioHover);
}

.agregarModelos {
  background: var(--colorTerciario);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.3s ease;
}

.agregarModelos:hover {
  background: var(--colorTerciarioHover);
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

.contenedorBotonAgregar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contenedorBotonAgregar input {
  flex: 1;
}

.btnAgregar {
  background-color: var(--colorTerciario);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  gap: 10px;
  display: flex;
  align-items: center;
}

.btnAgregar:hover {
  background-color: var(--colorTerciarioHover);
}

.btnEliminar {
  background-color: var(--colorError);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btnEliminar:hover {
  background-color: var(--colorErrorHover);
}

.limiteImagenes {
  color: white;
  margin-top: 20px;
}

.contenedorImagenCarrusel {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contenedorImagenCarrusel input {
  flex: 1;
}

.btnAgregarCarrusel {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}

.contenedorTituloSeccion {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  margin-top: -30px;
}

.contenedorDescuento {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-direction: row;
}

.campoDescuento {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.ocultar-modelo-centrado {
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.switch-label {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.2rem;
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

.texto-ocultar {
  color: var(--colorTextoSecundario); /* o #ffc107 si querés a mano */
  font-weight: 500;
}


.contenedorBoton {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
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

.contenedorBoton {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  width: 100%;
}

.btnImagenPortada {
  background-color: var(--colorTerciario); /* Amarillo */
}

.btnImagenPortada:hover {
  background-color: var(--colorTerciarioHover);
}

.btnCarrusel {
  background-color: var(--colorSecundario); /* Cian (por ejemplo) */
}

.btnCarrusel:hover {
  background-color: var(--colorSecundarioHover);
}

</style>

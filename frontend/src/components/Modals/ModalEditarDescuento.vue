<template>
  <div class="modal fade" ref="modalRef" tabindex="-1">
    <div class="modal-dialog modal-xl modal-dialog-centered">
      <div class="modal-content bg-dark text-white">
        <div class="modal-header">
          <div class="d-flex align-items-center gap-3">
            <img :src="producto.imagen || producto.imagenCarrusel?.[0]" alt="Imagen del producto"
              style="width: 60px; height: 60px; object-fit: contain; border-radius: 0.5rem; border: 1px solid #444;" />
            <h1 class="modal-title fs-5">Editar Descuento - {{ producto.nombre }}</h1>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <!-- Tabs -->
          <ul class="nav nav-tabs mb-3" id="descuentoTab" role="tablist">
            <li class="nav-item" role="presentation">
              <button class="nav-link active" id="producto-tab" data-bs-toggle="tab"
                data-bs-target="#producto" type="button" role="tab">Producto</button>
            </li>
            <li class="nav-item" role="presentation">
              <button class="nav-link" id="modelos-tab" data-bs-toggle="tab" data-bs-target="#modelos"
                type="button" role="tab">Modelos</button>
            </li>
          </ul>

          <div class="tab-content">
            <!-- Producto Tab -->
            <div class="tab-pane fade show active" id="producto" role="tabpanel">
              <div class="row g-3">
                <!-- ✅ Checkbox para aplicar descuento al producto base -->
                <div class="col-12">
                  <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" v-model="producto.descuento" id="check-base">
                    <label class="form-check-label" for="check-base">
                      Aplicar descuento
                    </label>
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Precio:</label>
                  <input type="text" class="form-control" :value="formattedPrecio"
                    @input="formatInput($event, 'precio')" />
                </div>

                <div class="col-md-6">
                  <label class="form-label">Precio con descuento:</label>
                  <input type="text" class="form-control" :value="precioFinal" readonly />
                </div>

                <!-- Solo mostrar los campos si se activa el checkbox -->
                <template v-if="producto.descuento">
                  <div class="col-md-6">
                    <label class="form-label">Tipo de descuento:</label>
                    <select v-model="producto.tipoDescuento" class="form-select">
                      <option disabled value="">Seleccioná un tipo...</option>
                      <option value="porcentaje">Porcentaje (%)</option>
                      <option value="monto">Monto Fijo ($)</option>
                    </select>
                  </div>

                  <div class="col-md-6" v-if="producto.tipoDescuento === 'porcentaje'">
                    <label class="form-label">Porcentaje:</label>
                    <input type="number" class="form-control"
                      v-model.number="producto.porcentajeDescuento" min="0" max="100" />
                  </div>

                  <div class="col-md-6" v-else>
                    <label class="form-label">Monto de Descuento:</label>
                    <input type="text" class="form-control" :value="formattedMonto"
                      @input="formatInput($event, 'montoDescuento')" />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Vencimiento:</label>
                    <input type="datetime-local" v-model="producto.fechaYHoraVencimiento"
                      class="form-control" :min="minFechaActual" />
                  </div>
                </template>
              </div>
            </div>

            <!-- Modelos Tab -->
            <div class="tab-pane fade" id="modelos" role="tabpanel">
              <div v-if="producto.modelos?.length">
                <div v-for="(modelo, index) in producto.modelos" :key="index" class="border-top pt-3 mt-3">
                  <div class="d-flex align-items-center gap-3 mb-3">
                    <img :src="modelo.imagen || modelo.imagenCarrusel?.[0] || 'https://via.placeholder.com/60x60?text=Sin+imagen'"
                      alt="Imagen modelo"
                      style="width: 60px; height: 60px; object-fit: contain; border-radius: 0.5rem; border: 1px solid #555;" />
                    <h6 class="text-info m-0">Modelo: {{ modelo.nombre || 'Sin nombre' }}</h6>
                  </div>

                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Precio:</label>
                      <input type="text" class="form-control" :value="formatNumber(modelo.precio)"
                        @input="formatModeloInput($event, modelo, 'precio')" />
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">Precio con descuento:</label>
                      <input type="text" class="form-control"
                        :value="formatPrecioFinalModelo(modelo)" readonly />
                    </div>

                    <div class="form-check mb-3">
                      <input class="form-check-input" type="checkbox" v-model="modelo.descuento"
                        :id="'check-descuento-' + index">
                      <label class="form-check-label" :for="'check-descuento-' + index">
                        Aplicar descuento a este modelo
                      </label>
                    </div>

                    <template v-if="modelo.descuento">
                      <div class="col-md-6">
                        <label class="form-label">Tipo de Descuento:</label>
                        <select v-model="modelo.tipoDescuento" class="form-select">
                          <option value="">Seleccioná...</option>
                          <option value="porcentaje">Porcentaje (%)</option>
                          <option value="monto">Monto Fijo ($)</option>
                        </select>
                      </div>

                      <div class="col-md-6" v-if="modelo.tipoDescuento === 'porcentaje'">
                        <label class="form-label">Porcentaje (%):</label>
                        <input type="number" class="form-control"
                          v-model.number="modelo.porcentajeDescuento" min="0" max="100" />
                      </div>

                      <div class="col-md-6" v-else>
                        <label class="form-label">Monto ($):</label>
                        <input type="text" class="form-control"
                          :value="formatNumber(modelo.montoDescuento)"
                          @input="formatModeloInput($event, modelo, 'montoDescuento')" />
                      </div>

                      <div class="col-md-6">
                        <label class="form-label">Vencimiento:</label>
                        <input type="datetime-local" class="form-control"
                          v-model="modelo.fechaYHoraVencimiento" />
                      </div>
                    </template>
                  </div>
                </div>
              </div>

              <div v-else class="text-white-50">Este producto no tiene modelos configurados.</div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
          <button v-if="producto.descuento" type="button" class="btn btn-outline-danger me-auto"
            @click="emit('solicitar-confirmacion')">
            Eliminar descuento
          </button>
          <button type="button" class="btn btn-success" @click="guardar">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  producto: Object
})

const emit = defineEmits(['guardar', 'solicitar-confirmacion'])
const modalRef = ref(null)

const show = () => {
  // Reset del producto base si no tiene descuento
  if (!props.producto.descuento) {
    props.producto.tipoDescuento = null
    props.producto.porcentajeDescuento = 0
    props.producto.montoDescuento = 0
    props.producto.fechaYHoraVencimiento = null
  } else {
    // Aseguramos que tenga al menos un tipo de descuento definido
    if (!props.producto.tipoDescuento) {
      props.producto.tipoDescuento = 'porcentaje'
    }
  }

  const modal = new bootstrap.Modal(modalRef.value)
  nextTick(() => modal.show())
}

const hide = () => {
  const modal = bootstrap.Modal.getInstance(modalRef.value)
  modal?.hide()
}

defineExpose({ show, hide })

watch(() => props.producto.descuento, (activo) => {
  if (activo && !props.producto.tipoDescuento) {
    props.producto.tipoDescuento = 'porcentaje'
  }
})

// 💸 Formateo de inputs
const formatInput = (e, campo) => {
  const valor = Number(e.target.value.replace(/\D/g, ''))
  props.producto[campo] = valor
}

const formatModeloInput = (e, modelo, campo) => {
  const valor = Number(e.target.value.replace(/\D/g, ''))
  modelo[campo] = valor
}

const formatNumber = val => (val || val === 0) ? val.toLocaleString('es-AR') : ''

const formattedPrecio = computed(() => formatNumber(props.producto.precio))
const formattedMonto = computed(() => formatNumber(props.producto.montoDescuento))

// 💰 Precio con descuento del producto base
const precioFinal = computed(() => {
  if (!props.producto.precio) return formattedPrecio.value

  let precio = props.producto.precio
  if (props.producto.tipoDescuento === 'porcentaje') {
    precio -= (precio * (props.producto.porcentajeDescuento || 0)) / 100
  } else {
    precio -= props.producto.montoDescuento || 0
  }
  return formatNumber(Math.max(0, precio))
})

const minFechaActual = computed(() => {
  const ahora = new Date()
  ahora.setSeconds(0, 0)
  return ahora.toISOString().slice(0, 16)
})

// 📦 Para cada modelo
const calcularPrecioFinalModelo = (modelo) => {
  if (!modelo.precio) return modelo.precio || 0

  let precio = modelo.precio
  if (modelo.tipoDescuento === 'porcentaje') {
    precio -= (precio * (modelo.porcentajeDescuento || 0)) / 100
  } else {
    precio -= modelo.montoDescuento || 0
  }
  return Math.max(0, precio)
}

const formatPrecioFinalModelo = (modelo) => {
  return formatNumber(calcularPrecioFinalModelo(modelo))
}

// 🧹 Eliminar descuento base
const confirmarEliminacion = () => {
  const confirmacion = window.confirm('¿Estás seguro de que querés eliminar el descuento de este producto?')
  if (confirmacion) {
    props.producto.descuento = false
    props.producto.tipoDescuento = null
    props.producto.porcentajeDescuento = 0
    props.producto.montoDescuento = 0
    props.producto.fechaYHoraVencimiento = null
    guardar()
  }
}

// 💾 Guardar
const guardar = () => {
  // Limpieza de modelos sin descuento
  if (props.producto.modelos && Array.isArray(props.producto.modelos)) {
    props.producto.modelos.forEach(modelo => {
      if (!modelo.descuento) {
        modelo.tipoDescuento = null
        modelo.porcentajeDescuento = 0
        modelo.montoDescuento = 0
        modelo.fechaYHoraVencimiento = null
      } else {
        // Asegurar campos válidos por defecto
        if (!modelo.tipoDescuento) {
          modelo.tipoDescuento = 'porcentaje'
        }
      }
    })
  }

  emit('guardar')
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
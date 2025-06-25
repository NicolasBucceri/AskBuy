<template>
    <div class="modal fade" ref="modalRef" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content bg-dark text-white">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Editar Descuento</h1>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body d-grid gap-3" style="grid-template-columns: 1fr 1fr;">
                    <div class="formularioCampo" style="grid-column: span 2;">
                        <label class="form-label">Precio:</label>
                        <input type="text" class="form-control" :value="formattedPrecio"
                            @input="formatInput($event, 'precio')" />
                    </div>

                    <div class="formularioCampo">
                        <label class="form-label">Aplicar Descuento:</label>
                        <input type="checkbox" v-model="producto.descuento" class="form-check-input ms-1 mt-2" />
                    </div>

                    <div class="formularioCampo">
                        <label class="form-label">Tipo de descuento:</label>
                        <select v-model="producto.tipoDescuento" class="form-select" :disabled="!producto.descuento">
                            <option disabled value="">Seleccioná un tipo...</option>
                            <option value="porcentaje">Porcentaje (%)</option>
                            <option value="monto">Monto Fijo ($)</option>
                        </select>

                    </div>

                    <div class="formularioCampo" v-if="producto.tipoDescuento === 'porcentaje'">
                        <label class="form-label">Porcentaje:</label>
                        <input type="number" class="form-control" v-model.number="producto.porcentajeDescuento" min="0"
                            max="100" />
                    </div>

                    <div class="formularioCampo" v-else>
                        <label class="form-label">Monto de Descuento:</label>
                        <input type="text" class="form-control" :value="formattedMonto"
                            @input="formatInput($event, 'montoDescuento')" />
                    </div>

                    <div class="formularioCampo">
                        <label class="form-label">Precio con descuento:</label>
                        <input type="text" class="form-control" :value="precioFinal" readonly />
                    </div>

                    <div class="formularioCampo">
                        <label class="form-label">Vencimiento:</label>
                        <input type="datetime-local" v-model="producto.fechaYHoraVencimiento" class="form-control"
                            :min="minFechaActual" />

                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-success" @click="guardar">Guardar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
    producto: Object
})
const emit = defineEmits(['guardar'])

const modalRef = ref(null)

const show = () => {
    if (props.producto.descuento && !props.producto.tipoDescuento) {
        props.producto.tipoDescuento = 'porcentaje'
    }

    const modal = new bootstrap.Modal(modalRef.value)
    nextTick(() => modal.show())
}

const hide = () => {
    const modal = bootstrap.Modal.getInstance(modalRef.value)
    modal?.hide()
}

defineExpose({ show, hide })

// Watch opcional por si cambiás el checkbox sin abrir modal
watch(() => props.producto.descuento, (activo) => {
    if (activo && !props.producto.tipoDescuento) {
        props.producto.tipoDescuento = 'porcentaje'
    }
})

const formatInput = (e, campo) => {
    const valor = Number(e.target.value.replace(/\D/g, ''))
    props.producto[campo] = valor
}

const formatNumber = val => (val || val === 0) ? val.toLocaleString('es-AR') : ''

const formattedPrecio = computed(() => formatNumber(props.producto.precio))
const formattedMonto = computed(() => formatNumber(props.producto.montoDescuento))

const precioFinal = computed(() => {
    if (!props.producto.descuento || !props.producto.precio) return formattedPrecio.value
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
  ahora.setSeconds(0, 0) // saca los milisegundos
  return ahora.toISOString().slice(0, 16) // formato YYYY-MM-DDTHH:mm
})


const guardar = () => {
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
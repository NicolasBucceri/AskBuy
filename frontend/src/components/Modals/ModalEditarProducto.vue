<template>
    <div class="modal fade" id="modalEditarProducto" tabindex="-1" aria-hidden="true" ref="modalRef">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">✏️ Editar Producto</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div v-if="producto">

                        <!-- 🔁 Tabs -->
                        <ul class="nav nav-tabs" role="tablist">
                            <li class="nav-item">
                                <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#productoBase"
                                    type="button">
                                    Producto Base
                                </button>
                            </li>
                            <li class="nav-item">
                                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#modelos" type="button">
                                    Modelos
                                </button>
                            </li>
                        </ul>

                        <!-- 📦 Contenido tabs -->
                        <div class="tab-content mt-3">
                            <!-- 🧾 TAB: Producto Base -->
                            <div class="tab-pane fade show active" id="productoBase">
                                <div class="edicion-producto-wrapper">
                                    <!-- 🖼 Vista previa izquierda -->
                                    <div class="preview-portada-grande">
                                        <Swiper ref="swiperRef" :modules="[Navigation, Pagination]" :slides-per-view="1"
                                            :space-between="10" class="swiper-preview" :navigation="true"
                                            :pagination="{ clickable: true }">
                                            <SwiperSlide v-for="(img, i) in imagenesCombinadas" :key="'img-' + i">
                                                <img :src="img" alt="Imagen producto" class="img-slide-preview" />
                                            </SwiperSlide>
                                        </Swiper>
                                    </div>

                                    <!-- 🧾 Formulario de edición -->
                                    <div class="formulario-edicion">
                                        <!-- Imagen Portada -->
                                        <div class="campo-form full-width">
                                            <label>Imagen Portada:</label>
                                            <div class="input-con-botones">
                                                <input type="text" v-model="producto.imagen"
                                                    placeholder="URL de imagen" />
                                                <button @click="$refs.fileInputPortada.click()" class="btnAgregar"
                                                    title="Subir imagen">
                                                    <i class="fas fa-upload"></i>
                                                </button>
                                                <button @click="producto.imagen = ''" class="btnEliminar"
                                                    title="Eliminar imagen">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                            <input type="file" ref="fileInputPortada" @change="handleImagenPortada"
                                                hidden accept="image/*" />
                                        </div>

                                        <!-- Carrusel -->
                                        <div class="campo-form full-width">
                                            <label>Imágenes Carrusel:</label>
                                            <div v-for="(img, i) in producto.imagenCarrusel" :key="i"
                                                class="input-carrusel">
                                                <input type="text" v-model="producto.imagenCarrusel[i]"
                                                    placeholder="URL carrusel" />
                                                <button @click.prevent="abrirInputCarrusel(i)" class="btnAgregar"
                                                    title="Subir">
                                                    <i class="fas fa-upload"></i>
                                                </button>
                                                <input type="file" ref="fileInputCarrusel" ref-in-for :data-index="i"
                                                    @change="e => handleImagenCarrusel(e, i)" hidden accept="image/*" />
                                                <button @click="producto.imagenCarrusel.splice(i, 1)"
                                                    class="btnEliminar" title="Eliminar">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                            <div class="zona-agregar-img-horizontal">
                                                <button @click="agregarImagenCarrusel" class="boton-agregar-horizontal"
                                                    :disabled="producto.imagenCarrusel.length >= 6">
                                                    <i class="fas fa-plus"></i>
                                                    Agregar Imagen
                                                </button>
                                                <span class="contador-img">{{ producto.imagenCarrusel.length }} / 6
                                                    imágenes agregadas</span>
                                            </div>
                                        </div>

                                        <!-- Info -->
                                        <div class="grid-row">
                                            <div class="campo-form">
                                                <label>Nombre:</label>
                                                <input type="text" v-model="producto.nombre" />
                                            </div>
                                            <div class="campo-form">
                                                <label>Color:</label>
                                                <input type="text" v-model="producto.color" />
                                            </div>
                                            <div class="campo-form">
                                                <label>Precio:</label>
                                                <input type="text" :value="precioVisualSeguro"
                                                    @input="actualizarPrecioFormateado($event.target.value)"
                                                    inputmode="numeric" />
                                            </div>
                                            <div class="custom-checkbox">
                                                <input type="checkbox" id="modeloDescuento"
                                                    v-model="producto.descuento" />
                                                <label for="modeloDescuento">
                                                    <span class="checkbox-icon"></span>
                                                    Aplicar Descuento
                                                </label>
                                            </div>
                                        </div>

                                        <!-- Descuento -->
                                        <div class="grid-row" v-if="producto.descuento">
                                            <div class="campo-form">
                                                <label>Tipo de Descuento:</label>
                                                <select v-model="producto.tipoDescuento">
                                                    <option disabled value="">Seleccionar tipo</option>
                                                    <option value="porcentaje">Porcentaje (%)</option>
                                                    <option value="monto">Monto Fijo ($)</option>
                                                </select>
                                            </div>
                                            <div class="campo-form" v-if="modelo.tipoDescuento === 'porcentaje'">
                                                <label>Porcentaje:</label>
                                                <input type="number" v-model.number="modelo.porcentajeDescuento" min="0"
                                                    max="100" />
                                            </div>
                                            <div class="campo-form" v-if="modelo.tipoDescuento === 'monto'">
                                                <label>Monto Fijo:</label>
                                                <input type="number" v-model.number="modelo.montoDescuento" min="0" />
                                            </div>
                                            <div class="campo-form">
                                                <label>Precio con Descuento:</label>
                                                <input type="text"
                                                    :value="formatPrecio(calcularPrecioConDescuento(producto))"
                                                    readonly />
                                            </div>
                                        </div>

                                        <!-- Stock -->
                                        <div class="fila-stock">
                                            <div class="campo-form">
                                                <label>Stock Disponible:</label>
                                                <input type="number" v-model.number="modelo.stockDisponible"
                                                    @blur="$emit('validar-stock', modelo)" />
                                            </div>
                                            <div class="campo-form">
                                                <label>Stock Físico:</label>
                                                <input type="number" v-model.number="modelo.stockFisico"
                                                    @blur="$emit('validar-stock', modelo)" />
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
                                </div>
                            </div>

                            <!-- 🎨 TAB: Modelos -->
                            <div class="tab-pane fade" id="modelos">
                                <div v-if="producto.modelos?.length">
                                    <div v-for="(modelo, index) in producto.modelos" :key="index"
                                        class="modelo-card-grid">
                                        <!-- 🖼 Preview -->
                                        <div class="preview-modelo-swiper">
                                            <Swiper :modules="[Navigation, Pagination]" :slides-per-view="1"
                                                :space-between="10" :navigation="true"
                                                :pagination="{ clickable: true }">
                                                <SwiperSlide v-if="modelo.imagen">
                                                    <img :src="modelo.imagen" class="img-slide-preview"
                                                        alt="Imagen principal modelo" />
                                                </SwiperSlide>
                                                <SwiperSlide v-for="(img, i) in modelo.imagenCarrusel"
                                                    :key="'m-img-' + i">
                                                    <img :src="img" class="img-slide-preview"
                                                        alt="Imagen carrusel modelo" />
                                                </SwiperSlide>
                                            </Swiper>
                                        </div>

                                        <!-- 📝 Campos -->
                                        <div class="formulario-modelo-derecha">
                                            <!-- Imagen Portada -->
                                            <div class="campo-form full-width">
                                                <label>Imagen Portada:</label>
                                                <div class="input-con-botones">
                                                    <input type="text" v-model="modelo.imagen"
                                                        placeholder="URL imagen modelo" />
                                                    <button @click="() => $refs[`fileModelo${index}`]?.click()"
                                                        class="btnAgregar" title="Subir">
                                                        <i class="fas fa-upload"></i>
                                                    </button>
                                                    <input type="file" :ref="`fileModelo${index}`"
                                                        @change="e => handleImagenModelo(e, index)" hidden
                                                        accept="image/*" />
                                                    <button @click="modelo.imagen = ''" class="btnEliminar"
                                                        title="Eliminar">
                                                        <i class="fas fa-trash"></i>
                                                    </button>
                                                </div>
                                            </div>

                                            <!-- Carrusel -->
                                            <div class="campo-form full-width">
                                                <label>Imágenes Carrusel:</label>
                                                <div v-for="(img, i) in modelo.imagenCarrusel" :key="i"
                                                    class="input-carrusel">
                                                    <input type="text" v-model="modelo.imagenCarrusel[i]"
                                                        placeholder="URL carrusel" />
                                                    <button @click.prevent="abrirInputCarruselModelo(index, i)"
                                                        class="btnAgregar" title="Subir">
                                                        <i class="fas fa-upload"></i>
                                                    </button>
                                                    <input type="file" :ref="`fileCarruselModelo${index}-${i}`"
                                                        @change="e => handleImagenCarruselModelo(e, index, i)" hidden
                                                        accept="image/*" />
                                                    <button @click="modelo.imagenCarrusel.splice(i, 1)"
                                                        class="btnEliminar" title="Eliminar">
                                                        <i class="fas fa-trash"></i>
                                                    </button>
                                                </div>

                                                <div class="zona-agregar-img-horizontal">
                                                    <button @click="modelo.imagenCarrusel.push('')"
                                                        class="boton-agregar-horizontal"
                                                        :disabled="modelo.imagenCarrusel.length >= 6">
                                                        <i class="fas fa-plus"></i> Agregar Imagen
                                                    </button>
                                                    <span class="contador-img">{{ modelo.imagenCarrusel.length }} / 6
                                                        imágenes</span>
                                                </div>
                                            </div>

                                            <!-- Nombre, color, precio -->
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
                                                    <input type="text" :value="formatPrecio(modelo.precio)"
                                                        @input="actualizarPrecioModelo($event.target.value, index)"
                                                        inputmode="numeric" />
                                                </div>
                                            </div>

                                            <!-- Descuento -->
                                            <div class="custom-checkbox">
                                                <input type="checkbox" :id="'descuento-' + index"
                                                    v-model="modelo.descuento" />
                                                <label :for="'descuento-' + index">
                                                    <span class="checkbox-icon"></span> Aplicar Descuento
                                                </label>
                                            </div>

                                            <div class="grid-row" v-if="modelo.descuento">
                                                <div class="campo-form">
                                                    <label>Tipo de Descuento:</label>
                                                    <select v-model="modelo.tipoDescuento">
                                                        <option disabled value="">Seleccionar tipo</option>
                                                        <option value="porcentaje">Porcentaje (%)</option>
                                                        <option value="monto">Monto Fijo ($)</option>
                                                    </select>
                                                </div>

                                                <div class="campo-form" v-if="modelo.tipoDescuento === 'porcentaje'">
                                                    <label>Porcentaje:</label>
                                                    <input type="number" v-model.number="modelo.porcentajeDescuento"
                                                        min="0" max="100" />
                                                </div>

                                                <div class="campo-form" v-if="modelo.tipoDescuento === 'monto'">
                                                    <label>Monto Fijo:</label>
                                                    <input type="number" v-model.number="modelo.montoDescuento"
                                                        min="0" />
                                                </div>

                                                <div class="campo-form">
                                                    <label>Precio con Descuento:</label>
                                                    <input type="text"
                                                        :value="formatPrecio(calcularPrecioConDescuento(modelo))"
                                                        readonly />
                                                </div>
                                            </div>


                                            <!-- Stock -->
                                            <div class="grid-row">
                                                <div class="campo-form">
                                                    <label>Stock Disponible:</label>
                                                    <input type="number" v-model.number="modelo.stockDisponible" />
                                                </div>
                                                <div class="campo-form">
                                                    <label>Stock Físico:</label>
                                                    <input type="number" v-model.number="modelo.stockFisico" />
                                                </div>
                                                <div class="campo-form switch-container">
                                                    <label class="switch-label">
                                                        <input type="checkbox" v-model="modelo.oculto" />
                                                        <span class="switch-slider"></span>
                                                        Ocultar Modelo
                                                    </label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div v-else class="text-muted">No hay modelos cargados para este producto.</div>
                            </div>




                        </div>

                    </div>

                    <div v-else class="text-white p-4">
                        <p>Cargando producto...</p>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button class="btn btn-success" @click="emit('guardar', props.producto)">Guardar</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination } from 'swiper/modules'

import { computed, watch, ref, defineEmits, defineProps, onMounted, nextTick } from 'vue'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

const emit = defineEmits(['guardar', 'toggle-ocultar', 'validar-stock'])

const swiperRef = ref(null)
const fileInputCarrusel = ref([])

const props = defineProps({
    producto: Object,
    precioConDescuento: Function
})

const modalRef = ref(null)
let modalInstance = null
const modelo = computed(() => props.producto)


onMounted(() => {
    modalInstance = new bootstrap.Modal(modalRef.value)

    // 👇 Valor por defecto si no viene cargado
    if (props.producto && !props.producto.tipoDescuento) {
        props.producto.tipoDescuento = 'porcentaje'
    }

    nextTick(() => {
        swiperRef.value?.swiper?.update()
    })
})



// 🧠 Formatear precio
function formatPrecio(valor) {
    if (!valor) return ''
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0
    }).format(valor)
}

// 🧠 Actualizar precio desde input
function actualizarPrecio(valor) {
    const soloNumeros = valor.replace(/\D/g, '')
    if (props.producto) {
        props.producto.precio = parseInt(soloNumeros) || 0
    }
}

// 🖼 Imagen portada
function handleImagenPortada(e) {
    const file = e.target.files[0]
    if (file && props.producto) {
        const reader = new FileReader()
        reader.onload = (ev) => {
            props.producto.imagen = ev.target.result
        }
        reader.readAsDataURL(file)
    }
}

const precioFormateado = computed({
    get() {
        return formatPrecio(modelo.value.precio)
    },
    set(valor) {
        const soloNumeros = valor.replace(/\D/g, '')
        modelo.value.precio = parseInt(soloNumeros) || 0
    }
})


// Visual con formato de moneda
const precioVisual = computed(() => formatPrecio(modelo.value.precio))

// Al escribir, se actualiza como número
function actualizarPrecioModelo(valor, index) {
  const soloNumeros = valor.replace(/\D/g, '')
  if (props.producto.modelos[index]) {
    props.producto.modelos[index].precio = parseInt(soloNumeros) || 0
  }
}

const precioVisualSeguro = computed(() => {
    return modelo.value ? formatPrecio(modelo.value.precio) : ''
})



// 🖼 Imagen carrusel
function handleImagenCarrusel(e, index) {
    const file = e.target.files[0]
    if (file && props.producto) {
        const reader = new FileReader()
        reader.onload = (ev) => {
            props.producto.imagenCarrusel[index] = ev.target.result
        }
        reader.readAsDataURL(file)
    }
}

// ✅ Agregar imagen al carrusel
function agregarImagenCarrusel() {
    if (props.producto && props.producto.imagenCarrusel.length < 6) {
        props.producto.imagenCarrusel.push('')
    }
}

// ✅ Abrir input carrusel
function abrirInputCarrusel(i) {
    fileInputCarrusel.value?.[i]?.click()
}

// ✅ Abrir modal
function abrir() {
    modalInstance?.show()
    nextTick(() => {
        swiperRef.value?.swiper?.update()
    })
}

// ✅ Cerrar modal
function cerrar() {
    modalInstance?.hide()
}

// ✅ Computar imágenes combinadas
const imagenesCombinadas = computed(() => {
    if (!props.producto) return []
    return [props.producto.imagen, ...(props.producto.imagenCarrusel || [])]
        .filter(img => typeof img === 'string' && img.trim() !== '')
})

function calcularPrecioConDescuento(p) {
    if (!p) return 0
    if (p.descuento) {
        if (p.tipoDescuento === 'porcentaje') {
            return p.precio - (p.precio * (p.porcentajeDescuento || 0) / 100)
        } else if (p.tipoDescuento === 'monto') {
            return p.precio - (p.montoDescuento || 0)
        }
    }
    return p.precio
}



function handleImagenModelo(e, index) {
    const file = e.target.files[0]
    if (file && props.producto.modelos[index]) {
        const reader = new FileReader()
        reader.onload = (ev) => {
            props.producto.modelos[index].imagen = ev.target.result
        }
        reader.readAsDataURL(file)
    }
}

function handleImagenCarruselModelo(e, modeloIndex, imgIndex) {
    const file = e.target.files[0]
    if (file && props.producto.modelos[modeloIndex]) {
        const reader = new FileReader()
        reader.onload = (ev) => {
            props.producto.modelos[modeloIndex].imagenCarrusel[imgIndex] = ev.target.result
        }
        reader.readAsDataURL(file)
    }
}

function abrirInputCarruselModelo(modeloIndex, imgIndex) {
    const inputRef = `fileCarruselModelo${modeloIndex}-${imgIndex}`
    nextTick(() => {
        const input = refs[inputRef]
        if (input) input.click()
    })
}




watch(
    () => props.producto?.descuento,
    (nuevoValor) => {
        if (nuevoValor && !props.producto.tipoDescuento) {
            props.producto.tipoDescuento = 'porcentaje'
            console.log('🟡 Aplicar descuento activado, tipoDescuento seteado a porcentaje')
        }
    }
)




defineExpose({ abrir, cerrar })
</script>




<style scoped>
/* ==== Modal general ==== */
.modal-content {
    background-color: #1c1c1c;
    color: #fff;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    border: none;
}

.modal-header,
.modal-footer {
    border-color: #333;
}

.modal-title {
    font-weight: 600;
    font-size: 1.2rem;
    color: var(--colorTerciario);
}

/* ==== Layout general del modal ==== */
.edicion-producto-wrapper {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
    align-items: flex-start;
}

/* ==== Formulario === */
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

.campo-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    /* antes estaba en 8px o 4px según tus pruebas */
}


.campo-form label {
    font-weight: 600;
    font-size: 16px;
    color: var(--colorTerciario);
    display: inline-block;
}


input[type="text"],
input[type="number"],
select,
textarea {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #444;
    padding: 12px 14px;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    transition: border-color 0.3s;
    width: 100%;
    margin-top: -8px;
    margin-bottom: 10px;
}

input:focus,
select:focus,
textarea:focus {
    border-color: var(--colorTerciario);
    outline: none;
}

/* ==== Botones === */
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

.btnAgregar, .btnEliminar {
    margin-bottom: 20px;
}

.btnEliminar {
    background-color: var(--colorError);
    color: white;
}

.btnEliminar:hover {
    background-color: var(--colorErrorHover);
}

.btnAgregarImg {
    background: var(--colorTerciario);
    color: black;
}

.btn-close {
    filter: invert(1);
}


/* ==== Carrusel === */
.input-carrusel {
    display: flex;
    gap: 10px;
    align-items: center;
}

.input-carrusel input[type="text"] {
    flex: 1;
}

.swiper-preview {
    width: 100%;
    max-width: 280px;
    height: 280px;
    background-color: #fff;
    /* Fondo blanco para resaltar la imagen */
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 0 20px rgba(255, 193, 7, 0.15);
    /* Sombra dorada */
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.img-slide-preview {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 12px;
    transition: transform 0.3s ease;
}

::v-deep(.swiper-button-next),
::v-deep(.swiper-button-prev) {
    color: var(--colorTerciario);
}

::v-deep(.swiper-pagination-bullet) {
    background: #444;
    opacity: 1;
    width: 10px;
    height: 10px;
    margin: 0 5px;
    transition: background 0.3s, transform 0.3s;
}

::v-deep(.swiper-pagination-bullet-active) {
    background: var(--colorTerciario);
    transform: scale(1.2);
}

/* Grillas internas */
.grid-row,
.fila-stock {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 1rem;
}

.input-con-botones {
    display: flex;
    align-items: center;
    gap: 10px;
}

.custom-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    color: var(--colorTextoSecundario);
    cursor: pointer;
    user-select: none;
    margin-top: -10px;

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

input[type="checkbox"]:checked+label .checkbox-icon {
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

input[type="checkbox"]:checked+label .checkbox-icon::after {
    opacity: 1;
}

.zona-agregar-img-horizontal {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 14px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.boton-agregar-horizontal {
    background-color: var(--colorTerciario);
    color: #000;
    border: none;
    padding: 10px 16px;
    font-size: 15px;
    font-weight: 600;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background-color 0.3s ease;
}

.boton-agregar-horizontal:hover {
    background-color: var(--colorTerciarioHover);
}

.boton-agregar-horizontal:disabled {
    background-color: #666;
    cursor: not-allowed;
    opacity: 0.6;
}

.contador-img {
    font-size: 14px;
    font-weight: 500;
    color: var(--colorTextoSecundario);
}

.switch-container {
    display: flex;
    align-items: center;
    height: 100%;
    margin-top: 14%;

}

.switch-label {
    display: flex !important;
    align-items: center;
    gap: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    color: var(--colorTerciario);
    line-height: 1;
}



.switch-label input[type="checkbox"] {
    display: none;
}

.switch-slider {
    display: inline-block;
    /* 👈 Esto arregla todo */
    position: relative;
    width: 52px;
    height: 28px;
    background-color: #555 !important;
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

input[type="checkbox"]:checked+.switch-slider+.switch-text {
    color: var(--colorExito);
    /* Podés usar rojo si es para "oculto" */
    font-weight: bold;
}

.preview-modelo-img img {
    width: 120px;
    height: 120px;
    object-fit: contain;
    border-radius: 10px;
    border: 2px solid #444;
    background-color: #fff;
    padding: 6px;
}

.modelo-card-grid {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
    background: #1a1a1a;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 0 16px rgba(0, 0, 0, 0.3);
}



.formulario-modelo-derecha {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
</style>

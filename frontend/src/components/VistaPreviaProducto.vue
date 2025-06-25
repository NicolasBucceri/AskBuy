<template>
    <teleport to="body">
        <div class="modal fade" id="modalVistaPrevia" tabindex="-1" aria-labelledby="modalVistaPreviaLabel"
            aria-hidden="true" @hidden.bs.modal="$emit('cerrar')">
            <div class="modal-dialog modal-fullscreen">
                <div class="modal-content fondoModalPreview">

                    <div class="boton-cerrar-modal">
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                            aria-label="Cerrar"></button>
                    </div>


                    <div class="modal-body p-0">
                        <div class="contenedorGeneral">
                            <div v-if="producto" class="contenedor-producto">




                                <!-- Columna izquierda: Carrusel Bootstrap -->
                                <div class="columna izquierda">
                                    <div class="contenedor-imagenes">
                                        <!-- Miniaturas a la izquierda -->
                                        <div class="miniaturas-vertical">
                                            <!-- Imagen portada primero -->

                                            <!-- Luego las del carrusel -->
                                            <img v-for="(img, index) in imagenesCompletas" :key="'miniatura-' + index"
                                                :src="img" class="miniatura-vertical" alt="Miniatura"
                                                @click="seleccionarSlide(index)" />
                                        </div>

                                        <!-- Carrusel principal -->
                                        <div id="carouselProducto" class="carousel slide carrusel-principal"
                                            data-bs-ride="carousel">
                                            <div class="carousel-inner">
                                                <div v-for="(img, index) in imagenesCompletas"
                                                    :key="'carousel-' + index"
                                                    :class="['carousel-item', { active: index === 0 }]">
                                                    <div class="contenedor-imagen">
                                                        <img :src="img" class="imagen-principal"
                                                            :alt="'Imagen ' + (index + 1)" />
                                                    </div>
                                                </div>
                                            </div>


                                            <!-- Flecha izquierda -->
                                            <button class="carousel-control-prev custom-flecha" type="button"
                                                data-bs-target="#carouselProducto" data-bs-slide="prev">
                                                <i class="fa-solid fa-chevron-left"></i>
                                            </button>

                                            <!-- Flecha derecha -->
                                            <button class="carousel-control-next custom-flecha" type="button"
                                                data-bs-target="#carouselProducto" data-bs-slide="next">
                                                <i class="fa-solid fa-chevron-right"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Derecha: Detalles del producto -->
                                <div class="columna derecha">
                                    <div class="fila-superior">
                                        <p class="marca-categoria">
                                            <strong>{{ producto.marca || 'Logitech' }}</strong> | {{ producto.categoria
                                                || '--' }}
                                        </p>

                                        <div v-if="producto.etiquetas?.length" class="contenedor-etiquetas">
                                            <span v-for="(etiqueta, index) in producto.etiquetas" :key="index"
                                                class="etiqueta-producto">
                                                {{ etiqueta }}
                                            </span>
                                        </div>
                                    </div>


                                    <h3 class="nombre-producto">
                                        {{ producto.nombre }}
                                    </h3>

                                    <div class="precio-producto">
                                        <!-- Precio original tachado -->
                                        <span
                                            v-if="modeloSeleccionado?.tipoDescuento && calcularPrecioConDescuento(modeloSeleccionado) < modeloSeleccionado.precio"
                                            class="precio-original">
                                            {{ formatPrice(modeloSeleccionado.precio) }}
                                        </span>



                                        <!-- Precio con descuento aplicado -->
                                        <div class="precio-final-con-descuento">
                                            <span class="precio-final">
                                                {{ formatPrice(calcularPrecioConDescuento(modeloSeleccionado)) }}
                                            </span>

                                            <span v-if="modeloSeleccionado?.tipoDescuento === 'porcentaje'"
                                                class="etiqueta-descuento">
                                                -{{ modeloSeleccionado.porcentajeDescuento }}% OFF
                                            </span>

                                            <span v-if="modeloSeleccionado?.tipoDescuento === 'monto'"
                                                class="etiqueta-descuento">
                                                -{{ formatPrice(modeloSeleccionado.montoDescuento) }} OFF
                                            </span>

                                        </div>

                                        <p v-if="fechaDescuento" class="fecha-vencimiento">
                                            <i class="fa-regular fa-clock"></i> Descuento válido hasta {{ fechaDescuento
                                            }}
                                        </p>
                                    </div>




                                    <div v-if="modelosUnificados.length" class="cardsModeloGeneral">
                                        <h5 class="titulo-modelos">| Colores: {{ modeloSeleccionado?.color ||
                                            producto.colorPrincipal }}</h5>
                                        <div class="cardsModelo">
                                            <div v-for="(modelo, index) in modelosUnificados" :key="modelo.id"
                                                :class="['cardModelo', { activo: modeloSeleccionado?.id === modelo.id || (!modeloSeleccionado && modelo.id === 'base') }]"
                                                @click="seleccionarModelo(modelo)">
                                                <img :src="modelo.imagen || modelo.imagenPortada || producto.imagen"
                                                    alt="Modelo" />
                                            </div>
                                        </div>
                                    </div>


                                    <div class="stock-info">
                                        <div class="stock-cabecera">
                                            <i class="fa-solid fa-boxes-stacked icono-stock"></i>
                                            <h5 class="titulo-stock">Stock: {{ stockDisponible }} disponible<span
                                                    v-if="stockDisponible !== 1">s</span>
                                            </h5>
                                        </div>

                                        <div class="selector-cantidad">
                                            <label for="cantidad" class="label-cantidad">Cantidad:</label>
                                            <select v-model="cantidadSeleccionada" @change="verificarCantidad"
                                                class="select-cantidad">
                                                <option v-for="n in 5" :key="n" :value="n">{{ n }} unidad<span
                                                        v-if="n > 1">es</span></option>
                                                <option value="custom">+6 unidades</option>
                                            </select>

                                            <input v-if="mostrarInputCustom" type="number" min="6"
                                                :max="stockDisponible" v-model.number="cantidadCustom"
                                                placeholder="Ingresá la cantidad" class="input-custom" />
                                        </div>
                                    </div>

                                    <div class="botones-modernos">
                                        <button class="btn-comprar">Comprar ahora</button>
                                        <div class="botones-acciones">
                                            <button class="btn-icono" @click="consultarPorWhatsApp">
                                                <i class="fab fa-whatsapp"></i>
                                            </button>
                                            <button class="btn-icono" @click="agregarAlCarrito">
                                                <i class="fas fa-cart-plus"></i>
                                            </button>

                                        </div>
                                    </div>

                                </div>

                                <div class="columna descripcion-detalle">
                                    <div class="descripcion-producto" :class="{ expandida: descripcionExpandida }">
                                        <p class="descripcion-texto" ref="descripcionTexto">{{ producto.descripcion }}
                                        </p>
                                        <div class="fade-descripcion" v-if="!descripcionExpandida && mostrarFade"></div>


                                    </div>

                                    <!-- Botón fuera del contenedor que tiene overflow -->
                                    <button v-if="mostrarFade" class="boton-ver-mas"
                                        @click="descripcionExpandida = !descripcionExpandida">
                                        {{ descripcionExpandida ? 'Ver menos' : 'Ver más' }}
                                        <i
                                            :class="[descripcionExpandida ? 'fa-chevron-up' : 'fa-chevron-down', 'fa-solid']"></i>
                                    </button>

                                    <div v-for="(item, index) in producto.detallesTecnicos" :key="index"
                                        class="acordeon">
                                        <div class="acordeon-header" @click="toggle(index)">
                                            <h4 class="titulo-acordeon">{{ item.titulo }}</h4>
                                            <i :class="['fa-solid', acordeonesAbiertos[index] ? 'fa-chevron-up' : 'fa-chevron-down']"
                                                class="icono-flecha"></i>
                                        </div>
                                        <transition name="fade-acordeon">
                                            <div v-if="acordeonesAbiertos[index]" class="acordeon-cuerpo">
                                                <ul>
                                                    <li v-for="(detalle, i) in item.detalles" :key="i"
                                                        class="item-detalle">
                                                        <span class="detalle-clave">{{ detalle.clave }}:</span> {{
                                                            detalle.valor }}
                                                    </li>
                                                </ul>
                                            </div>
                                        </transition>
                                    </div>


                                </div>
                            </div>


                            <div v-else class="cargando">
                                <p>Cargando producto...</p>
                            </div>
                        </div>
                        <!-- <DetalleProducto :producto="producto" modoPreview /> -->
                    </div>
                </div>
            </div>
        </div>
        <div v-if="producto.value">
            <h1 style="color: white">Producto recibido: {{ producto.value.nombre }}</h1>
        </div>

    </teleport>
    <div v-if="producto.value">
        <h1 style="color: white">Producto recibido: {{ producto.value.nombre }}</h1>
    </div>

</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue';

const props = defineProps({
    producto: Object,
    modeloEnVistaPrevia: Object,
    modelosUnificados: Array,
    modeloSeleccionado: Number,
    modoPreview: Boolean
});

// 🔧 Fix para acceder a `producto` sin errores en el template
const producto = computed(() => props.producto);

const cantidadSeleccionada = ref(1);
const cantidadCustom = ref(null);
const mostrarInputCustom = ref(false);
const descripcionExpandida = ref(false);
const mostrarFade = ref(true);
const modeloActual = computed(() => modeloSeleccionado.value);


const descripcionTexto = ref(null);

const emit = defineEmits(['cerrar'])

onMounted(() => {
    const modal = document.getElementById('modalVistaPrevia')
    if (modal) {
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modal)
        modalInstance.show()

        modal.addEventListener('hidden.bs.modal', () => {
            emit('cerrar') // ahora sí va a andar
        })
    }
})



const modeloSeleccionado = ref();

const modeloBase = computed(() => ({
    id: 'base',
    nombre: producto.value.nombre,
    color: producto.value.colorPrincipal,
    imagenMiniatura: producto.value.imagenCarrusel?.[0],
    imagenCarrusel: producto.value.imagenCarrusel,
    precio: producto.value.precio,
    stockDisponible: producto.value.stockDisponible || 0,
    porcentajeDescuento: producto.value.porcentajeDescuento || 0,
    montoDescuento: producto.value.montoDescuento || 0,
    tipoDescuento: producto.value.tipoDescuento || null,
    precioConDescuento: producto.value.precioConDescuento || producto.value.precio,
    fechaVencimientoDescuento: producto.value.fechaVencimientoDescuento || null
}));

const modelosUnificados = computed(() => {
    return [modeloBase.value, ...(producto.value.modelos || [])];
});

watch(modelosUnificados, (nuevos) => {
    if (nuevos.length > 0 && !modeloSeleccionado.value) {
        modeloSeleccionado.value = nuevos[0];
    }
}, { immediate: true });

const imagenesCompletas = computed(() => {
    const modelo = modeloSeleccionado.value;
    if (!modelo) return [];

    if (modelo.id === 'base') {
        const portada = producto.value.imagen;
        const carrusel = producto.value.imagenCarrusel || [];
        const sinRepetidas = carrusel.filter(img => img !== portada);
        return [portada, ...sinRepetidas];
    }

    const portadaModelo = modelo.imagen || modelo.imagenMiniatura || modelo.imagenCarrusel?.[0];
    const carruselModelo = modelo.imagenCarrusel || [];
    const sinRepetidas = carruselModelo.filter(img => img !== portadaModelo);
    return [portadaModelo, ...sinRepetidas];
});

function formatPrice(value) {
    if (!value) return '$0';
    return new Intl.NumberFormat("es-AR", {
        style: "currency",
        currency: "ARS",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

const stockDisponible = computed(() => modeloSeleccionado.value?.stockDisponible || producto.value.stockDisponible);

function seleccionarModelo(modelo) {
    modeloSeleccionado.value = modelo;
    cantidadSeleccionada.value = 1;
    cantidadCustom.value = null;
}

function verificarCantidad() {
    mostrarInputCustom.value = cantidadSeleccionada.value === 'custom';
    if (cantidadSeleccionada.value !== 'custom') {
        cantidadCustom.value = null;
    }
}

const acordeonesAbiertos = ref([]);

function toggle(index) {
    acordeonesAbiertos.value[index] = !acordeonesAbiertos.value[index];
}

const fechaDescuento = computed(() => {
    const fecha = modeloSeleccionado.value?.fechaVencimientoDescuento || producto.value?.fechaVencimientoDescuento;
    if (!fecha) return null;
    const fechaObj = new Date(fecha);
    return fechaObj.toLocaleDateString('es-AR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
});

const descuentoVencido = computed(() => {
    const fecha = modeloSeleccionado.value?.fechaVencimientoDescuento || producto.value?.fechaVencimientoDescuento;
    if (!fecha) return false;
    return new Date(fecha) < new Date();
});

function calcularPrecioConDescuento(modelo) {
    if (!modelo || !modelo.precio || !modelo.tipoDescuento) return modelo?.precio || 0;

    let final = modelo.precio;

    if (modelo.tipoDescuento === 'porcentaje' && modelo.porcentajeDescuento > 0) {
        final -= (modelo.precio * modelo.porcentajeDescuento) / 100;
    }

    if (modelo.tipoDescuento === 'monto' && modelo.montoDescuento > 0) {
        final -= modelo.montoDescuento;
    }

    return final;
}
watch(() => producto.value, (nuevoValor) => {
    console.log('🕵️‍♂️ Watch producto:', nuevoValor)
})

// ✅ Consolitas por si necesitás seguir debuggeando
console.log("🧩 Recibiendo props:", props.producto);
console.log("📦 Modelos unificados:", modelosUnificados.value);
console.log("🎯 Modelo seleccionado:", modeloSeleccionado.value);

</script>


<style scoped>
/* ======================= */
/* 🔷 ESTRUCTURA GENERAL 🔷 */
/* ======================= */

.fondoModalPreview {
    background: #1f1f1f !important;
    /* Fondo admin oscuro */
    border-radius: 1rem;
    color: white;
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
    border: none;
}


.contenedorGeneral {
    background: rgba(30, 30, 30, 0.85);
    backdrop-filter: blur(8px);
    padding: 2rem 1rem;
    border-radius: 1rem;
}



.contenedor-producto {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    max-width: 1200px;
    margin: auto;
    background: var(--colorFondoPrincipal);
    color: var(--colorTextoPrincipal);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    column-gap: 3rem;
}

.columna.derecha {
    border-left: 1px solid #e5e7eb;
    padding-left: 2rem;
}

.columna {
    flex: 1 1 45%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.descripcion-detalle {
    flex: 1 1 100%;
}

.fila-superior {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}


/* ========================= */
/* 🟦 MODELOS DE PRODUCTO 🟦 */
/* ========================= */

.cardsModeloGeneral {
    padding: 12px;
    overflow-x: auto;
    white-space: nowrap;
}

.cardsModelo {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 10px;
}

.cardModelo {
    width: 70px;
    height: 70px;
    border-radius: 16px;
    border: 2px solid transparent;
    overflow: hidden;
    cursor: pointer;
    transition: border 0.2s ease-in-out;
    flex-shrink: 0;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: none;
    transition: box-shadow 0.2s ease;
}

.cardModelo img {
    width: auto;
    height: 100%;
    max-width: 100%;
    object-fit: contain;
    padding: 6px;
    background-color: white;
}


.cardModelo.activo {
    border: 2px solid var(--colorPrincipal);
}

.descripcion-producto {
    position: relative;
    max-height: 7.5em;
    overflow: hidden;
    transition: max-height 0.3s ease;
    padding-bottom: 3.5rem;
    /* más espacio para el botón */
    z-index: 1;
    /* asegura que esté encima */
}


.descripcion-producto.expandida {
    max-height: none;
    padding-bottom: 0;
}


.fade-descripcion {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3em;
    background: linear-gradient(to top, var(--colorFondoPrincipal), transparent);
}

/* ======================== */
/* 🟢 BOTONES DE ACCIÓN 🟢 */
/* ======================== */

.botones-accion-unificados {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}

.boton-comprar-grande {
    flex: 1;
    padding: 1rem;
    background-color: var(--colorPrincipal);
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    border: none;
    border-radius: 1rem;
    cursor: pointer;
    transition: background 0.3s ease;
}

.boton-comprar-grande:hover {
    opacity: 0.85;
}

.acciones-secundarias {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.boton-icono {
    background-color: var(--colorTerciario);
    color: white;
    border: none;
    width: 52px;
    height: 52px;
    border-radius: 12px;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s ease;
}

.boton-icono:hover {
    opacity: 0.85;
}

.boton-icono:first-child {
    background-color: #25D366;
    /* WhatsApp verde */
}

.botones-modernos {
    max-width: 600px;
    /* Más ancho */
    width: 100%;
    margin: auto;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.btn-comprar {
    width: 100%;
    padding: 1.2rem 2rem;
    background: #111827;
    color: #ffffff;
    font-size: 1.25rem;
    font-weight: 600;
    border: none;
    border-radius: 14px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}

.btn-comprar:hover {
    background: #1f2937;
    transform: translateY(-2px);
}

.botones-acciones {
    display: flex;
    justify-content: space-between;
    gap: 1.2rem;
}

.btn-icono {
    flex: 1;
    padding: 1rem 0;
    font-size: 1.4rem;
    border: none;
    border-radius: 12px;
    background: #f3f4f6;
    color: #111827;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.btn-icono:hover {
    background: #e5e7eb;
    transform: translateY(-1px);
}

.boton-ver-mas {
    background: none;
    border: none;
    color: var(--colorPrincipal);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.25rem 0;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: color 0.2s ease;
}

.boton-ver-mas:hover {
    color: var(--colorPrincipalHover);
}




/* ======================== */
/* 🖼️ CARRUSEL DE IMÁGENES 🖼️ */
/* ======================== */

.contenedor-imagenes {
    display: flex;
    gap: 1rem;
}

.carrusel-principal {
    flex: 1;
}

.contenedor-imagen {
    width: 100%;
    height: 450px;
    background: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 1rem;
    overflow: hidden;
}

.imagen-principal {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.custom-flecha {
    background: none;
    border: none;
    font-size: 2rem;
    color: var(--colorFondoSecundario);
    padding: 0 1rem;
    z-index: 2;
}


/* ============================ */
/* 🔳 MINIATURAS LATERALES 🔳 */
/* ============================ */

.miniaturas-vertical {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.miniatura-vertical {
    width: 60px;
    height: 60px;
    object-fit: contain;
    padding: 4px;
    background-color: white;
    border-radius: 0.5rem;
    border: 2px solid transparent;
    cursor: pointer;
}


.miniatura-vertical:hover {
    border-color: var(--colorPrincipal);
}


/* ============================ */
/* 🏷️ INFORMACIÓN DEL PRODUCTO */
/* ============================ */

.marca-categoria {
    font-size: 0.9rem;
    color: var(--colorSecundario);
    margin: 0;
}

.nombre-producto {
    font-size: 1.8rem;
    font-weight: 500;
    font-family: var(--fuenteTerciario);
    color: var(--colorTextoPrincipal);
    margin-bottom: 0.5rem;
    padding-bottom: 0.4rem;
}


/* 💰 PRECIO */
.precio-producto {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin: 0.5rem 0 1rem;
}

.precio-original {
    font-size: 1rem;
    color: #888;
    text-decoration: line-through;
}

.precio-final-con-descuento {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.precio-final {
    font-size: 2.2rem;
    font-weight: 600;
    color: var(--colorFondoSecundario);
}

.etiqueta-descuento {
    font-size: 1rem;
    font-weight: 600;
    color: #00a650;
    background-color: #e6f6ec;
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    text-transform: uppercase;
}


/* ========================= */
/* 🟣 ETIQUETAS DEL PRODUCTO */
/* ========================= */

.contenedor-etiquetas {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.etiqueta-producto {
    background-color: var(--colorTerciario);
    color: #fff;
    padding: 0.25rem 0.75rem;
    font-size: 0.7rem;
    font-weight: 700;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}


/* 🎨 COLOR DEL PRODUCTO */

.color-circulo {
    width: 25px;
    height: 25px;
    background: var(--colorPrincipal);
    border-radius: 50%;
}


/* ======================== */
/* ➕ CANTIDAD Y BOTONES 🛒 */
/* ======================== */

.control-cantidad {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
}

.boton-cantidad {
    width: 30px;
    height: 30px;
    background: var(--colorSecundario);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    cursor: pointer;
}

.boton-agregar {
    background: var(--colorTerciario);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 9999px;
    font-weight: bold;
    margin-top: 1.5rem;
    transition: background 0.3s ease;
    cursor: pointer;
}

.boton-agregar:hover {
    background: var(--colorTerciarioHover);
}



.stock-info {
    background: #f7f7f7;
    padding: 1rem;
    border-radius: 1rem;
    margin: 1rem 0;
    color: #333;
    border: 1px solid #ddd;
}



.stock-cabecera {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.icono-stock {
    font-size: 1.4rem;
    color: var(--colorPrincipal);
}

.titulo-stock {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
}

.selector-cantidad {
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
}

.select-cantidad,
.input-custom {
    width: 30%;
}

.label-cantidad {
    font-weight: 600;
}

.select-cantidad {
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: none;
    background: white;
    color: #333;
    font-weight: bold;
}

.input-custom {
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: 2px solid var(--colorPrincipal);
    background: #fff;
    color: #333;
    font-weight: 500;
}



/* =================== */
/* 📋 ACORDEÓN TÉCNICO */
/* =================== */

.acordeon {
    border-top: 1px solid #e5e7eb;
    margin-top: 1rem;
    padding-top: 1rem;
}

.acordeon-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    padding: 0.8rem 0;
    transition: color 0.3s ease;
}

.acordeon-header:hover {
    color: var(--colorPrincipal);
}

.titulo-acordeon {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
    color: var(--colorPrincipal);
}

.icono-flecha {
    font-size: 1.2rem;
    color: var(--colorPrincipal);
    transition: transform 0.3s ease;
}

.acordeon-cuerpo {
    margin-top: 0.5rem;
    padding-left: 1rem;
}

.acordeon-cuerpo ul {
    columns: 2;
    column-gap: 2rem;
}


.item-detalle {
    margin-bottom: 0.4rem;
}

.detalle-clave {
    font-weight: 600;
    margin-right: 0.5rem;
    color: #111827;
}

/* Animación */
.fade-acordeon-enter-active,
.fade-acordeon-leave-active {
    transition: all 0.3s ease;
}

.fade-acordeon-enter-from,
.fade-acordeon-leave-to {
    opacity: 0;
    max-height: 0;
}

.fade-acordeon-enter-to,
.fade-acordeon-leave-from {
    opacity: 1;
    max-height: 300px;
}

/* Notificación toast */
.noti-container {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    z-index: 999999;
}

.noti-toast {
    background-color: #212529;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: flex-start;
    min-width: 280px;
    max-width: 350px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    gap: 12px;
    animation: slideIn 0.3s ease-out;
}

.noti-toast.success {
    border-left: 5px solid #28a745;
}

.noti-toast.error {
    border-left: 5px solid #dc3545;
}

.noti-toast.info {
    border-left: 5px solid #17a2b8;
}

.icono {
    margin-top: 2px;
    font-size: 1.2rem;
    color: white;
}

.contenido {
    flex: 1;
    color: white;
}

.titulo {
    display: block;
    font-weight: 600;
    margin-bottom: 4px;
}

.tiempo {
    font-size: 0.75rem;
    color: #ccc;
    margin-top: 4px;
    display: block;
}


.mensaje {
    margin: 0;
    font-size: 0.9rem;
    color: #f1f1f1;
}

.btn-cerrar {
    background: transparent;
    border: none;
    color: white;
    font-size: 1rem;
    cursor: pointer;
}

@keyframes slideIn {
    from {
        transform: translateY(20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.boton-cerrar-modal {
    position: absolute;
    top: 1rem;
    right: 2rem;
    z-index: 9999;
    background: transparent;
    border: none;
}

.boton-cerrar-modal .btn-close {
    filter: invert(1);
    /* hace que se vea blanca */
    opacity: 0.8;
    transition: transform 0.2s ease, opacity 0.2s ease;
}

.boton-cerrar-modal .btn-close:hover {
    transform: scale(1.2);
    opacity: 1;
}


.fecha-vencimiento {
    font-size: 0.9rem;
    color: var(--colorExito);
    font-weight: 500;
    margin-top: 0.3rem;
    display: flex;
    align-items: center;
    gap: 6px;
}



/* ============= */
/* ⏳ CARGANDO... */
/* ============= */

.cargando {
    text-align: center;
    padding: 2rem;
    color: var(--colorSecundario);
}


/* ======================= */
/* 📱 MEDIA QUERIES 📱 */
/* ======================= */


@media (max-width: 991px) {

    html,
    body {
        width: 100%;
        overflow-x: hidden;
    }

    .contenedorGeneral,
    .contenedor-producto,
    .columna {
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }

    .contenedor-producto {
        flex-direction: column;
        align-items: center;
        padding: 1.5rem 1rem;
        gap: 2rem;
    }

    .contenedor-imagenes {
        display: flex;
        flex-direction: row;
        /* Mantenemos miniaturas a la izquierda SIEMPRE */
        align-items: flex-start;
        gap: 1rem;
        width: 100%;
    }

    .miniaturas-vertical {
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        max-height: 350px;
        overflow-y: auto;
        /* Si hay muchas miniaturas */
    }

    .miniatura-vertical {
        width: 55px;
        height: 55px;
        object-fit: contain;
        border-radius: 0.5rem;
        cursor: pointer;
    }

    .carrusel-principal {
        flex: 1;
    }

    .contenedor-imagen {
        width: 100%;
        height: 300px;
        border-radius: 0.75rem;
    }

    /* 🎯 Texto centrado */
    .nombre-producto,
    .precio-producto {
        text-align: center;
    }

    .nombre-producto {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .precio-producto {
        margin-bottom: 1.5rem;
    }

    /* 🛒 Botones cómodos */
    .btn-comprar,
    .btn-icono {
        padding: 1.2rem 2rem;
        font-size: 1.2rem;
    }

    .btn-comprar:hover,
    .btn-icono:hover {
        transform: translateY(-2px);
        opacity: 0.9;
    }

    .botones-modernos {
        width: 100%;
        max-width: 500px;
        margin: 1rem auto;
    }

    .cardsModelo {
        justify-content: center;
        gap: 1rem;
        padding: 0.5rem 0;
    }

    .selector-cantidad {
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
    }

    .select-cantidad,
    .input-custom {
        width: 100%;
    }

    .descripcion-producto {
        max-height: none;
        padding-bottom: 2rem;
    }

    .stock-info {
        padding: 1rem;
        margin-top: 1rem;
        width: 100%;
    }

    .acordeon-cuerpo ul {
        columns: 1;
    }
}

/* 📱 Ajustes extras para celulares muy chicos */
@media (max-width: 575px) {
    .miniatura-vertical {
        width: 45px;
        height: 45px;
    }

    .contenedor-imagen {
        height: 250px;
    }

    .nombre-producto {
        font-size: 1.3rem;
    }

    .precio-final {
        font-size: 1.6rem;
    }

    .cardModelo {
        width: 50px;
        height: 50px;
    }
}



@media (max-width: 439px) {
    .contenedor-producto {
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }

    .columna {
        flex: 1 1 100%;
        padding: 0;
    }

    .contenedor-imagen {
        height: 250px;
        width: 100%;
        border-radius: 0.75rem;
    }

    .miniaturas-vertical {
        flex-direction: row;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .carrusel-principal {
        width: 100%;
    }

    .descripcion-producto {
        max-height: none;
        padding-bottom: 2rem;
    }

    .botones-modernos {
        width: 100%;
        margin-top: 1rem;
    }

    .acordeon-cuerpo ul {
        columns: 1;
    }

}
</style>
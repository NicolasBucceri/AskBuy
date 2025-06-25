<template>
  <div class="contenedorSeccionDetalles">
    <div class="contenedorTituloSeccion">
      <h2 class="tituloFormulario">Detalles del Producto</h2>
    </div>

    <!-- Descripción General -->
    <div class="formularioCampo">
      <label>Descripción General:</label>
      <textarea v-model="product.descripcion" placeholder="Ejemplo: Este teclado mecánico RGB cuenta con switches..."
        class="campoDescripcion"></textarea>
    </div>

    <!-- Botón Agregar Ítem -->
    <div class="contenedorAcordeon" v-if="!mostrarFormDetalles">
      <button class="btnAcordeonPrincipal" @click="iniciarAgregarItem">
        + Agregar Detalle Tecnicos
      </button>
    </div>

    <!-- Formulario para Agregar o Editar Ítem -->
    <div v-else class="seccionAgregarItem">
      <div class="formularioCampo encabezadoAcordeon">
        <button class="btnVolverSeccion" @click="cancelarEdicion">
          <i class="fa-solid fa-arrow-left"></i> Volver
        </button>
        <label>Título del Acordeon:</label>
        <input v-model="nuevoItem.titulo" type="text" class="inputCampo" placeholder="Ej: Sensor Óptico" />
      </div>

      <div v-if="nuevoItem.titulo">
        <h5 class="subtituloSeccion">Agregar Detalles</h5>

        <div class="grupoInputs">
          <div class="formularioCampo">
            <label>Clave:</label>
            <input v-model="nuevoDetalle.clave" type="text" class="inputCampo" placeholder="Ej: DPI Máximo" />
          </div>

          <div class="formularioCampo">
            <label>Valor:</label>
            <input v-model="nuevoDetalle.valor" type="text" class="inputCampo" placeholder="Ej: 14000" />
          </div>
        </div>

        <button class="btnAgregarDetalle" @click="agregarDetalle">
          Agregar Detalle
        </button>

        <ul class="listaDetalles">
          <li v-for="(detalle, i) in nuevoItem.detalles" :key="i" class="detalleTexto">
            <span><strong>{{ detalle.clave }}</strong> : {{ detalle.valor }}</span>
            <div class="detalleAcciones">
              <button class="btnEditarIcono" @click="editarDetalleTemp(i)"><i
                  class="fa-solid fa-pen-to-square"></i></button>
              <button class="btnEliminar" @click="eliminarDetalleTemp(i)"><i class="fa-solid fa-trash"></i></button>
            </div>
          </li>
        </ul>

        <div class="accionesItem">
          <button class="btnAgregarItem" @click="agregarItem">Guardar Acordeon</button>
          <button class="btnCancelarItem" @click="cancelarEdicion">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Acordeón -->
    <div class="listaItemsAcordeon">
      <div v-for="(item, index) in product.detallesTecnicos" :key="index" class="itemAcordeon">
        <div class="itemAcordeonHeader" @click="toggle(index)">
          <h5>{{ item.titulo }}</h5>
          <div class="accionesAcordeon">
            <button @click.stop="editarItem(index)" class="btnAccion btnEditarIcono">
              <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <button @click.stop="eliminarItem(index)" class="btnAccion btnEliminar">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>

        <transition name="fade-slide">
          <div v-if="item.abierto" class="itemAcordeonBody">
            <ul>
              <li v-for="(detalle, i) in item.detalles" :key="i" class="detalleItem">
                <div class="detalleItemContent" :class="{ detalleItemEdicion: detalle.editando }">
                  <template v-if="!detalle.editando">
                    <div class="detalleTexto" :class="{ expandidoHorizontal: detalleExpandido === i }"
                      @click="toggleDetalleExpandido(i)">
                      <div class="detalleContenido">
                        <strong>{{ detalle.clave }}</strong>:
                        <span class="detalleValor">
                          {{ detalle.valor }}
                        </span>
                      </div>
                      <div class="detalleAcciones">
                        <button class="btnAccion btnEditarIcono" @click.stop="editarDetalle(detalle)">
                          <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button class="btnAccion btnEliminar" @click.stop="eliminarDetalle(item, i)">
                          <i class="fa-solid fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </template>


                  <template v-else>
                    <div class="grupoInputsEdicion">
                      <div class="inputGroup">
                        <label>Clave</label>
                        <input v-model="detalle.clave" class="inputCampo" placeholder="Ej: DPI Máximo" />
                      </div>
                      <div class="inputGroup">
                        <label>Valor</label>
                        <input v-model="detalle.valor" class="inputCampo" placeholder="Ej: 14000" />
                      </div>
                    </div>
                    <div class="accionesEdicion">
                      <button class="btnGuardar" @click="guardarEdicionDetalle(detalle)">
                        <i class="fa-solid fa-floppy-disk"></i> Guardar
                      </button>
                      <button class="btnCancelar" @click="cancelarEdicionDetalle(detalle)">
                        <i class="fa-solid fa-xmark"></i> Cancelar
                      </button>
                    </div>
                  </template>
                </div>
              </li>
            </ul>
          </div>
        </transition>
      </div>
    </div>
  </div>
  <!-- Botones de navegación -->
  <div class="contenedorBoton" v-if="!mostrarFormDetalles">
    <button class="btnFormulario btnAtras" @click="$emit('volver')">Atrás</button>
    <button class="btnFormulario" @click="$emit('siguiente')">Siguiente</button>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
const props = defineProps({
  product: Object,
})

const emit = defineEmits(['volver', 'siguiente'])

const mostrarFormDetalles = ref(false)
const nuevoItem = reactive({ titulo: '', detalles: [] })
const nuevoDetalle = reactive({ clave: '', valor: '' })

const iniciarAgregarItem = () => {
  mostrarFormDetalles.value = true
  Object.assign(nuevoItem, { titulo: '', detalles: [] })
}

const cancelarEdicion = () => {
  mostrarFormDetalles.value = false
}

const agregarDetalle = () => {
  if (nuevoDetalle.clave && nuevoDetalle.valor) {
    nuevoItem.detalles.push({ ...nuevoDetalle })
    Object.assign(nuevoDetalle, { clave: '', valor: '' })
  }
}

const editarDetalleTemp = (i) => {
  Object.assign(nuevoDetalle, nuevoItem.detalles[i])
  nuevoItem.detalles.splice(i, 1)
}

const eliminarDetalleTemp = (i) => {
  nuevoItem.detalles.splice(i, 1)
}

const agregarItem = () => {
  props.product.detallesTecnicos.push({ ...nuevoItem, abierto: false })
  cancelarEdicion()
}

const toggle = (i) => {
  props.product.detallesTecnicos[i].abierto = !props.product.detallesTecnicos[i].abierto
}

const editarItem = (i) => {
  Object.assign(nuevoItem, props.product.detallesTecnicos[i])
  props.product.detallesTecnicos.splice(i, 1)
  mostrarFormDetalles.value = true
}

const eliminarItem = (i) => {
  props.product.detallesTecnicos.splice(i, 1)
}

const editarDetalle = (detalle) => {
  detalle.editando = true
}

const cancelarEdicionDetalle = (detalle) => {
  detalle.editando = false
}

const guardarEdicionDetalle = (detalle) => {
  detalle.editando = false
}

const detalleExpandido = ref(null)
const toggleDetalleExpandido = (index) => {
  detalleExpandido.value = detalleExpandido.value === index ? null : index
}


</script>

<style scoped>
.contenedorSeccionDetalles {
  padding: 1rem;
}

.contenedorTituloSeccion {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -40px;
  margin-bottom: 20px;
}

.tituloFormulario {
  font-size: 1.25rem;
  text-align: center;
  margin-bottom: 1rem;
  color: var(--colorTextoSecundario);
}

.subtituloSeccion {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--colorSecundario);
}

.formularioCampo label {
  font-weight: bold;
  font-size: 1rem;
  color: var(--colorTextoSecundario);
}

.campoDescripcion {
  width: 100%;
  height: 150px;
  padding: 1rem;
  padding-right: 1.5rem;
  /* ⬅️ espacio para el scrollbar */
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  resize: vertical;
  font-size: 1rem;
  font-family: inherit;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  overflow-y: auto;
  scrollbar-gutter: stable;
  /* 👌 Evita que se mueva el contenido al aparecer el scroll */
}


.campoDescripcion:focus {
  border-color: var(--colorTerciario);
  box-shadow: 0 0 5px rgba(226, 211, 74, 0.3);
  outline: none;
}

.campoDescripcion::-webkit-scrollbar {
  width: 10px;
}

.campoDescripcion::-webkit-scrollbar-track {
  background: #2c2c2c;
  border-radius: 8px;
}

.campoDescripcion::-webkit-scrollbar-thumb {
  background-color: var(--colorTerciario);
  border-radius: 8px;
  border: 2px solid #2c2c2c;
}

.campoDescripcion::-webkit-scrollbar-thumb:hover {
  background-color: var(--colorTerciarioHover);
}


.grupoInputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.inputGroup {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.inputGroup label {
  margin-bottom: 0.25rem;
  color: #666;
  font-size: 0.85rem;
}

.inputCampo {
  padding: 0.5rem;
  font-size: 0.9rem;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 6px;
  transition: border-color 0.3s;
}

.subtituloSeccion {
  font-size: 1rem;
  color: var(--colorTextoSecundario);
}

.inputCampo:focus {
  border-color: #00bfa6;
}


.btnAcordeonPrincipal {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--colorTerciario);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 12px;
  margin-top: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btnAgregarDetalle {
  display: block;
  margin: 1.5rem auto;
  padding: 0.75rem 1.5rem;
  background-color: var(--colorTerciario);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btnAgregarDetalle:hover {
  background-color: var(--colorTerciarioHover);
  transform: translateY(-2px);
}

.btnAgregarItem {
  background: linear-gradient(90deg, #4caf50, #45a049);
  color: #fff;
  border: none;
  border-radius: 0.75rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(76, 175, 80, 0.4);
}

.btnAgregarItem:hover {
  background: linear-gradient(90deg, #45a049, #4caf50);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.6);
}

.btnCancelarItem {
  background-color: #e0e0e0;
  color: #333;
  border: none;
  border-radius: 0.75rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.btnCancelarItem:hover {
  background-color: #d5d5d5;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.btnGuardar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background-color: #4caf50;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.btnGuardar:hover {
  background-color: #43a047;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btnCancelar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background-color: #e0e0e0;
  color: #333;
  font-size: 0.95rem;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.btnCancelar:hover {
  background-color: #d5d5d5;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btnAccion {
  background-color: transparent;
  border: none;
  color: #cfcfcf;
  font-size: 1.1rem;
  padding: 6px;
  border-radius: 8px;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btnAccion:hover {
  background-color: rgba(255, 193, 7, 0.15);
  /* dorado transparente */
  color: var(--colorTerciario);
  transform: scale(1.1);
  cursor: pointer;
}


.contenedorAcordeon {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
}

.encabezadoAcordeon {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 20px;
}

.listaItemsAcordeon {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.itemAcordeon {
  background: #1e1e1e;
  border: 1px solid #2a2a2a;
  border-left: 6px solid var(--colorTerciario);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transition: transform 0.2s ease;
  cursor: pointer;
}

.itemAcordeon:hover {
  transform: scale(1.01);
}

.itemAcordeonHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background-color: #2a2a2a;
  color: var(--colorTextoSecundario);
  font-size: 1rem;
  font-weight: 600;

}

.itemAcordeonHeader:hover {
  background-color: #333;
}


.itemAcordeonBody {
  padding: 1.5rem;
  background-color: #2a2a2a;
  border-radius: 0 0 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}


.listaDetalles {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detalleTexto {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 400;
  color: #fff;
  white-space: nowrap;
  flex-shrink: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}


.detalleAcciones {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: flex-end;
  margin-left: auto;
}

.detalleItem {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(4px);
  padding: 0.9rem 1rem;
  border-radius: 16px;
  margin-bottom: 0.5rem;
  border-left: 5px solid var(--colorTerciario);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.detalleItem:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}


.detalleTexto {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 1rem;
  font-weight: 400;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.detalleValor {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 100px;
  transition: all 0.3s ease;
}

.detalleValor.expandido {
  max-width: 1000px;
  /* forzamos expansión */
  white-space: normal;
  text-overflow: unset;
  overflow: visible;
}



.detalleValor::after {
  content: attr(title);
  display: none;
}

.detalleValor:hover::after {
  display: block;
}


.detalleTexto strong {
  color: var(--colorTerciario);
}


.detalleAcciones {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detalleItemContent {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: nowrap;
  width: 100%;
}

.detalleItemEdicion {
  flex-direction: column;
  align-items: stretch;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: #f9fafb;
}

.grupoInputsEdicion {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
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

.btnEliminar i {
  color: var(--colorError);
  /* o directamente #dc3545 */
  transition: color 0.2s ease;
}

.btnEliminar:hover i {
  color: var(--colorErrorHover);
  /* o un rojo más oscuro tipo #b02a37 */
}

.accionesItem {
  display: flex;
  justify-content: center;
  /* centra los botones */
  align-items: center;
  gap: 1rem;
  /* espacio entre botones */
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.detalleTexto {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: nowrap;
  gap: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.detalleContenido {
  display: flex;
  gap: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
}

.detalleTexto.expandidoHorizontal .detalleContenido {
  white-space: normal;
  overflow: visible;
  flex-wrap: wrap;
}

.detalleTexto.expandidoHorizontal .detalleValor {
  white-space: normal;
  text-overflow: unset;
  overflow: visible;
}

.detalleValor {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100px;
  display: inline-block;
  transition: all 0.3s ease;
}
</style>

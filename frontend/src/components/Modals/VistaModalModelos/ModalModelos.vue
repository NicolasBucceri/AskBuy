<template>
  <div class="modal fade" id="modalModelos" tabindex="-1" aria-labelledby="modalModelosLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">

        <!-- Header -->
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-puzzle-piece"></i> Modelos Agregados
          </h5>


          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>

        <!-- Body -->
        <div class="modal-body">
          <div v-if="product.modelos.length > 0" class="contenedor-modelos">
            <CardModelo v-for="(modelo, index) in product.modelos" :key="modelo.id" :modelo="modelo" :index="index"
              @eliminar-modelo="prepararEliminacion"
              @seleccionar-imagen-principal="seleccionarImagenModeloPrincipalEditar"
              @borrar-imagen="borrarImagenModeloEditar" @subir-imagen="subirImagenModeloEditar"
              @abrir-explorador="abrirExplorador" @cargar-imagen="cargarImagen" @toggle-ocultar="toggleOcultarModelo"
              @validar-stock="validarStockModelo" />
          </div>
          <p v-else>No hay modelos agregados.</p>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="btn-cerrar" data-bs-dismiss="modal">Cerrar</button>
        </div>

      </div>
    </div>
  </div>

  <Notificacion ref="notiRef" />
  <ModalConfirmacion ref="modalConfirmacionRef" :mensaje="mensajeConfirmacion" :colorBoton="'btn-danger'"
    @confirmar="confirmarEliminacionModelo" />


</template>

<script setup>
import { getCurrentInstance, ref } from 'vue'
import CardModelo from './CardModelo.vue'
import Notificacion from '../../ToastNotificacion.vue'
import ModalConfirmacion from '../ModalConfirmacion.vue'
import axios from 'axios'

const { proxy } = getCurrentInstance()
const notiRef = ref(null)
const modalConfirmacionRef = ref(null)
const mensajeConfirmacion = ref('')
let idModeloAEliminar = null

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'actualizar-modelos',
  'seleccionar-imagen-principal',
  'borrar-imagen',
  'subir-imagen',
  'abrir-explorador',
  'cargar-imagen',
  'toggle-ocultar',
  'validar-stock'
])

function eliminarModelo(idModelo) {
  console.log("🧨 Eliminar modelo con ID:", idModelo);
  const idProducto = props.product.id;

  // Si NO existe en Firestore aún, solo lo borrás local
  if (!idProducto) {
    const modelosActualizados = props.product.modelos.filter((m) => m.id !== idModelo);
    emit("actualizar-modelos", modelosActualizados);
    notiRef.value?.mostrar("🗑️ Borrado local", "Modelo eliminado del borrador.", "info");
    return;
  }

  // Si existe en Firestore, lo borrás del backend también
  axios
    .delete(`http://localhost:5000/api/product/${idProducto}/modelo-id/${idModelo}`)
    .then(() => {
      const modelosActualizados = props.product.modelos.filter((m) => m.id !== idModelo);
      emit("actualizar-modelos", modelosActualizados);
      notiRef.value?.mostrar("✅ Éxito", "Modelo eliminado correctamente.", "success");
    })
    .catch((err) => {
      console.error("❌ Error al eliminar:", err);
      notiRef.value?.mostrar("❌ Error", "No se pudo eliminar el modelo.", "error");
    });
}

function prepararEliminacion({ id, nombre }) {
  idModeloAEliminar = id
  mensajeConfirmacion.value = `¿Estás seguro que querés eliminar el modelo "${nombre}"? Esta acción no se puede deshacer.`
  modalConfirmacionRef.value?.abrir()
}
function confirmarEliminacionModelo() {
  eliminarModelo(idModeloAEliminar)
}



function seleccionarImagenModeloPrincipalEditar(index) {
  emit('seleccionar-imagen-principal', index)
}

function borrarImagenModeloEditar(index) {
  props.product.modelos[index].imagen = ''

  const refKey = `fileInputEditar${index}`
  const input = proxy?.$refs?.[refKey]
  if (input) input.value = ''
}

function subirImagenModeloEditar(event, index) {
  emit('subir-imagen', event, index)
}

function abrirExplorador(i) {
  emit('abrir-explorador', i)
}

function cargarImagen(modelo, i, e) {
  emit('cargar-imagen', modelo, i, e)
}

function toggleOcultarModelo(index, oculto) {
  const mensaje = oculto
    ? '👻 Modelo ocultado correctamente.'
    : '👁️ Modelo ahora es visible en la tienda.'

  notiRef.value?.mostrar('Estado del modelo', mensaje, oculto ? 'success' : 'info')
}

function validarStockModelo(modelo) {
  emit('validar-stock', modelo)
}

function precioConDescuentoModelo(modelo) {
  if (!modelo.precio) return '$0'
  let final = modelo.precio
  if (modelo.aplicaDescuento) {
    if (modelo.tipoDescuento === 'porcentaje') {
      final -= (final * modelo.porcentajeDescuento) / 100
    } else if (modelo.tipoDescuento === 'monto') {
      final -= modelo.montoDescuento
    }
  }
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0
  }).format(final)
}
</script>



<style scoped>
.modal-content {
  background-color: #1f1f1f;
  color: var(--colorTextoSecundario);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.modal-header,
.modal-footer {
  background-color: #2c2c2c;
  border-color: #444;
}

.modal-title {
  color: var(--colorTerciario);
  /* o directamente #ffc107 */
  font-size: 1.6rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-title i {
  color: var(--colorTextoSecundario); /* Si ya definiste un blanco suave */
}



.contenedor-modelos {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.btn-close {
  filter: invert(1) brightness(1.8);
  opacity: 1;
  width: 1rem;
  height: 1rem;
  background-size: 1rem;
  transition: transform 0.2s ease-in-out;
}

.btn-close:hover {
  transform: scale(1.15);
  filter: invert(1) brightness(2.2);
}
.btn-cerrar {
  background-color: var(--colorTerciario); /* amarillo dorado */
  color: #000;
  font-weight: 600;
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  transition: all 0.3s ease;
}

.btn-cerrar:hover {
  background-color: var(--colorTerciarioHover);
  transform: scale(1.05);
}

</style>

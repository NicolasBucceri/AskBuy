<template>
  <div class="card-modelo-admin">
    <!-- Imagen o Carrusel -->
    <div class="modelo-imagen-edit">
      <!-- Modo colapsado: imagen portada -->
      <img v-if="!modelo.showEdit && modelo.imagen" :src="modelo.imagen" alt="Imagen modelo" class="imagen-portada" />

      <!-- Modo edición: carrusel -->
      <swiper v-else :modules="[Navigation, Pagination]" :slides-per-view="1" :space-between="16" :navigation="true"
        :pagination="{ clickable: true }" class="swiper-container">
        <swiper-slide v-if="modelo.imagen">
          <div class="slide-content">
            <img :src="modelo.imagen" alt="Imagen principal" class="carruselImagen" />
          </div>
        </swiper-slide>

        <swiper-slide v-for="(img, i) in modelo.imagenCarrusel.filter(src => src && src.length > 5)" :key="i">
          <div class="slide-content">
            <img :src="img" alt="Imagen carrusel" class="carruselImagen" />
          </div>
        </swiper-slide>
      </swiper>
    </div>

    <!-- Info y acciones -->
    <div class="modelo-info">
      <h3 class="modelo-titulo">{{ modelo.nombre || 'Sin Nombre' }}</h3>

      <div class="modelo-acciones">
        <button class="btn-editar" @click="modelo.showEdit = !modelo.showEdit">
          <i class="fas fa-pen"></i> {{ modelo.showEdit ? 'Ocultar' : 'Editar' }}
        </button>
<button class="btn-eliminar" @click="$emit('eliminar-modelo', { id: modelo.id, nombre: modelo.nombre })">
  <i class="fas fa-trash"></i> Eliminar
</button>



      </div>

      <!-- Formulario -->
      <FormularioModelo v-if="modelo.showEdit" :modelo="modelo" :index="index"
        @seleccionar-imagen-principal="(idx) => $emit('seleccionar-imagen-principal', idx)"
        @borrar-imagen="(idx) => $emit('borrar-imagen', idx)" @subir-imagen="(e, idx) => $emit('subir-imagen', e, idx)"
        @abrir-explorador="(i) => $emit('abrir-explorador', i)"
        @cargar-imagen="(modelo, i, e) => $emit('cargar-imagen', modelo, i, e)"
        @toggle-ocultar="(index, val) => $emit('toggle-ocultar', index, val)"
        @validar-stock="(modelo) => $emit('validar-stock', modelo)" :precio-con-descuento="precioConDescuento" />


    </div>
  </div>
</template>


<script setup>
import FormularioModelo from './FormularioModelo.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'


components: {
  Swiper,
    SwiperSlide,
    FormularioModelo
}


const props = defineProps({
  modelo: Object,
  index: Number
})



const emit = defineEmits([
  'eliminar-modelo',
  'seleccionar-imagen-principal',
  'borrar-imagen',
  'subir-imagen',
  'abrir-explorador',
  'cargar-imagen',
  'toggle-ocultar',
  'validar-stock'
])

function precioConDescuento(modelo) {
  if (!modelo.precio) return '$0'
  let final = modelo.precio
  if (modelo.descuento) {
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

function prepararEliminacion({ id, nombre }) {
  idModeloAEliminar = id
  mensajeConfirmacion.value = `¿Estás seguro que querés eliminar el modelo "${nombre}"? Esta acción no se puede deshacer.`
  modalConfirmacionRef.value?.abrir()
}






</script>

<style scoped>
.card-modelo-admin {
  display: flex;
  background-color: #2b2b2b;
  border-radius: 16px;
  padding: 24px;
  gap: 32px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  color: var(--colorTextoSecundario);
  align-items: flex-start;
  flex-wrap: wrap;
}

.modelo-imagen img {
  max-width: 200px;
  border-radius: 12px;
  background-color: #fff;
  padding: 8px;
}

.modelo-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.modelo-titulo {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--colorTerciario);
  /* Cambiamos a amarillo */
}

.modelo-acciones {
  display: flex;
  gap: 12px;
  margin-top: auto;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn-editar,
.btn-eliminar {
  padding: 10px 18px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

/* 🟡 Edición: amarillo */
.btn-editar {
  background-color: var(--colorTerciario);
  color: var(--colorTextoPrincipal);
}

.btn-editar:hover {
  background-color: var(--colorTerciarioHover);
}

/* 🔴 Eliminar */
.btn-eliminar {
  background-color: var(--colorError);
  color: white;
}

.btn-eliminar:hover {
  background-color: var(--colorErrorHover);
}

.swiper-container {
  width: 100%;
  max-width: 280px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}

.carruselImagen {
  max-width: 100%;
  max-height: 280px;
  object-fit: contain;
  border-radius: 8px;
  padding: 10px;
}

.imagen-portada {
  max-width: 200px;
  border-radius: 12px;
  background-color: #fff;
  padding: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
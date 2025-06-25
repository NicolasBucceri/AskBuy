<template>
  <div class="main-container">

    <SidebarProducto :activeSection="activeSection" :product="product" @update:activeSection="activeSection = $event"
      @abrirModalCategoriasEtiquetas="abrirModalCategoriasEtiquetas" @abrirModalVistaPrevia="abrirModalVistaPrevia"
      @abrirModalLimpieza="abrirModalLimpieza" @toggleOcultar="toggleOcultar" />


    <VistaPreviaProducto v-if="mostrarVistaPrevia" :producto="product" :modelo-en-vista-previa="modeloEnVistaPrevia"
      :modelos-unificados="modelosUnificados" :modelo-seleccionado="modeloSeleccionado" :modo-preview="true"
      @cerrar="mostrarVistaPrevia = false" />

    <div class="contenedorForm">
      <!-- Formulario -->
      <div class="seccionForm">
        <div class="contenedorTitulo">
          <h1 class="tituloGeneral">Agregar Producto</h1>
        </div>

        <!-- Sección 1: Información -->
        <FormularioInformacion v-if="activeSection === 1" :product="product" @ir-siguiente="activeSection = 2" />


        <!-- Sección 2: Imágenes y Categorías -->
        <FormularioImagenesCategorias v-if="activeSection === 2" :product="product" :categorias="categorias"
          :etiquetasDisponibles="etiquetasDisponibles" :nueva-etiqueta-seleccionada="nuevaEtiquetaSeleccionada"
          :select-key="selectKey" @volver="activeSection--" @siguiente="activeSection++" />


        <!-- Sección 3: Detalles del Producto -->
        <FormularioDetallesTecnicos v-if="activeSection === 3" :product="product" @volver="activeSection--"
          @siguiente="activeSection++" />


        <!-- Sección 4: Modelos -->
        <FormularioModelos v-if="activeSection === 4" :activeSection="activeSection" :product="product"
          :modeloTemporal="modeloTemporal" :modeloSeleccionado="modeloSeleccionado" @volver="activeSection--"
          @siguiente="activeSection++" @toast="mostrarToast" />



        <!-- Sección 5: Logística -->
        <FormularioLogistica v-if="activeSection === 5" :product="product" :active-section="activeSection"
          @volver="activeSection--" @toast="mostrarToast"  @submit="agregarProducto" />

      </div>

      <!-- Vista previa -->
      <FormularioVistaPrevia :product="product" />


    </div>
  </div>

  <!-- Modal para agregar etiquetas -->
  <ModalAgregarEtiqueta @agregar-etiqueta="manejarEtiquetaDesdeModal" @toast="mostrarToast" />

  <!-- Modal para agregar categorias -->
  <ModalAgregarCategoria @agregar-categoria="manejarCategoriaDesdeModal" @toast="mostrarToast" />

  <!-- Modal de Categorías y Etiquetas con Tabs -->
  <ModalCategoriasEtiquetas v-if="mostrarModalCategorias" :visible="mostrarModalCategorias"
    @cerrar="mostrarModalCategorias = false" @toast="mostrarToast" />



  <!-- Modal Modelos -->
  <ModalModelos :product="product" :precio-con-descuento-modelo="precioConDescuentoModelo"
    @actualizar-modelos="actualizarModelos" />


  <!-- Modal Confirmar Agregar Producto -->
  <ModalProductoAgregado ref="modalProductoAgregado" />

  <!-- Notificacion -->
  <ToastNotificacion ref="toastRef" />


  <ModalConfirmacion ref="modalConfirmarLimpieza"
    mensaje="¿Estás seguro que querés borrar toda la información cargada? Esta acción no se puede deshacer."
    colorBoton="btn-danger" @confirmar="limpiarLocalStorage" />
</template>

<script>
import axios from "axios";
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { Navigation, Pagination } from "swiper/modules";
import cloneDeep from "lodash/cloneDeep";
import { nextTick } from "vue";

import VistaPreviaProducto from "../components/VistaPreviaProducto.vue";
import ModalAgregarEtiqueta from "../components/Modals/ModalAgregarEtiqueta.vue";
import ModalCategoriasEtiquetas from "../components/Modals/ModalCategoriasEtiquetas.vue";
import ModalAgregarCategoria from "../components/Modals/ModalAgregarCategoria.vue";
import ModalModelos from "../components/Modals/VistaModalModelos/ModalModelos.vue";
import ModalConfirmacion from "../components/Modals/ModalConfirmacion.vue";
import ModalProductoAgregado from "../components/Modals/ModalProductoAgregado.vue";
import FormularioInformacion from "../components/AddProductSections/FormularioInformacion.vue";
import FormularioImagenesCategorias from "../components/AddProductSections/FormularioImagenesCategorias.vue";
import FormularioDetallesTecnicos from "../components/AddProductSections/FormularioDetallesTecnicos.vue";
import FormularioModelos from "../components/AddProductSections/FormularioModelos.vue";
import FormularioLogistica from "../components/AddProductSections/FormularioLogistica.vue";
import FormularioVistaPrevia from "../components/AddProductSections/FormularioVistaPrevia.vue";
import SidebarProducto from '../components/AddProductSections/SidebarProducto.vue';
import ToastNotificacion from '../components/ToastNotificacion.vue'


export default {
  components: {
    Swiper,
    SwiperSlide,
    VistaPreviaProducto,
    ModalCategoriasEtiquetas,
    ModalAgregarEtiqueta,
    ModalAgregarCategoria,
    ModalModelos,
    ModalConfirmacion,
    ModalProductoAgregado,
    FormularioInformacion,
    FormularioImagenesCategorias,
    FormularioDetallesTecnicos,
    FormularioModelos,
    FormularioLogistica,
    FormularioVistaPrevia,
    SidebarProducto,
    ToastNotificacion
  },
  data() {
    return {
      // Datos del producto
      product: {
        marca: "",
        nombre: "",
        colorPrincipal: "",
        precio: null,
        descuento: false,
        tipoDescuento: "porcentaje",
        porcentajeDescuento: null,
        montoDescuento: null,
        fechaVencimientoDescuento: "",
        imagen: "",
        imagenCarrusel: [],
        categoria: "",
        etiquetas: [],
        descripcion: "",
        detallesTecnicos: [],
        stockFisico: 0,
        stockDisponible: 0,
        modelos: [],
        ocultar: false,
        nuevo: false,
      },
      modeloTemporal: {
        nombre: "",
        color: "",
        imagen: "",
        precio: 0,
        descuento: false,
        porcentajeDescuento: 0,
        montoDescuento: 0,
        imagenCarrusel: [],
      },


      // Categorías y etiquetas
      categorias: [],
      categoriaSeleccionada: null,
      nuevaCategoria: "",
      categoriaEditada: {
        id: null,
        nombre: "",
      },
      etiquetasDisponibles: [],
      nuevaEtiqueta: "",
      nuevaEtiquetaSeleccionada: "",

      // Estado de la UI
      activeSection: 1,
      mostrarModal: false,
      statusMessage: "",
      editando: false,

      // Control de navegación y carrousel
      currentIndex: 0,
      currentSlideIndex: 1,

      // Tablas dinámicas
      tablaOriginal: [],
      tablaVistaPrevia: null,
      tablasDinamicas: {},
      tablaSeleccionada: null,
      tablaEnEdicion: null,
      tablas: [],
      nuevaTabla: {
        categorias: [],
        titulo: "",
        subtablas: [],
      },
      tablaSeleccionada: {
        titulo: "",
        subtablas: [],
      },

      plantillas: [],
      tablaVistaPrevia: null,
      productoActual: {
        nombre: "",
        tablaDetallesTecnicos: null,
      },

      descripcionTabla: "",
      descripciones: [],
      item: {},

      acordeonItems: [],
      mostrarFormDetalles: false,
      editandoItem: false,
      nuevoItem: { titulo: "", detalles: [] },
      nuevoDetalle: { clave: "", valor: "" },
      editandoAcordeon: false,
      indexEnEdicion: null,
      imagenCarrusel: [],

      modelo: {
        imagenCarrusel: [], // Asegúrate de que esta propiedad siempre esté inicializada
      },

      categoriaAEliminar: null,
      etiquetaAEliminar: null,
      mensajeConfirmacion: "",
      mostrarVistaPrevia: false,
      mostrarModalCategorias: false,
      selectKey: 0,

      // Propiedades de Swiper
      Navigation,
      Pagination,
    };
  },

  computed: {
    totalImages() {
      return 1 + (this.product.imagenCarrusel?.length || 0);
    },
    imagenesCarruselModelo() {
      if (this.modeloEnVistaPrevia && this.modeloEnVistaPrevia.imagenCarrusel) {
        return this.modeloEnVistaPrevia.imagenCarrusel;
      }
      return [];
    },
    modelosUnificados() {
      const modeloPrincipal = {
        nombre: this.product.nombre,
        color: this.product.colorPrincipal,
        imagen: this.product.imagen,
        precio: this.product.precio,
        imagenCarrusel: this.product.imagenCarrusel,
        descuento: this.product.descuento,
        tipoDescuento: this.product.tipoDescuento,
        porcentajeDescuento: this.product.porcentajeDescuento,
        montoDescuento: this.product.montoDescuento,
      };

      return [modeloPrincipal, ...this.product.modelos];
    },
    detallesAgrupados() {
      return this.product.detallesTecnicos.reduce((acc, detalle) => {
        const grupo = detalle.grupo || "Otros";
        if (!acc[grupo]) acc[grupo] = [];
        acc[grupo].push(detalle);
        return acc;
      }, {});
    },
    modelosEnVistaPrevia() {
      return [
        {
          nombre: this.product.nombre,
          color: this.product.colorPrincipal,
          imagen: this.product.imagen,
          precio: this.product.precio,
          descuento: this.product.descuento,
          tipoDescuento: this.product.tipoDescuento,
          porcentajeDescuento: this.product.porcentajeDescuento,
          montoDescuento: this.product.montoDescuento,
          stockDisponible: this.product.stockDisponible,
        },
        ...(this.product.modelos || []).filter((modelo) => modelo && modelo.nombre),
      ];
    },
    coloresUnicos() {
      const colores = this.modelosEnVistaPrevia.map((modelo) => modelo.color);
      return [...new Set(colores)];
    },
    formattedMontoDescuentoModelo() {
      if (!this.modeloTemporal || typeof this.modeloTemporal.montoDescuento === 'undefined') return '';
      return this.formatNumber(this.modeloTemporal.montoDescuento);
    }
  },

  mounted() {
    this.cargarDescripciones();
    this.cargarProductoDesdeLocalStorage();

    this.tablaDetallesTecnicos = cloneDeep(this.tablaVistaPrevia);

    const seccionGuardada = localStorage.getItem("draft.activeSection");
    if (seccionGuardada) {
      this.activeSection = parseInt(seccionGuardada, 10);
    }

    const categoriaGuardada = localStorage.getItem("categoriaSeleccionada");
    if (categoriaGuardada) {
      this.product.categoria = categoriaGuardada;
    }

    const detallesGuardados = localStorage.getItem("detallesTecnicos");
    if (detallesGuardados) {
      this.tablaSeleccionada = JSON.parse(detallesGuardados);
    }

    const guardado = localStorage.getItem("descripcionTabla");
    if (guardado) {
      this.descripcionTabla = guardado;
    }

    const data = localStorage.getItem("acordeonItems");
    if (data) {
      this.acordeonItems = JSON.parse(data);
    }

    this.$nextTick(() => {
      const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
      );
      tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));
    });
  },

  watch: {
    product: {
      deep: true,
      handler(val) {
        localStorage.setItem("productoDraft", JSON.stringify(val));
      },
    },

    activeSection(newValue) {
      localStorage.setItem("draft.activeSection", newValue);
    },

    "product.categoria"(nuevaCategoria) {
      if (!nuevaCategoria) return;

      localStorage.setItem("draft.categoriaSeleccionada", nuevaCategoria);

      const categoriaKey = `Plantilla ${nuevaCategoria}`;

      if (this.tablasDinamicas[categoriaKey]) {
        this.tablaSeleccionada = cloneDeep(this.tablasDinamicas[categoriaKey]);
        this.product.tablaDetallesTecnicos = cloneDeep(this.tablaSeleccionada);
      } else {
        this.tablaSeleccionada = null;
      }
    },

    "product.stockDisponible"(newValue) {
      this.product.stockDisponible = Math.min(
        newValue,
        this.product.stockFisico
      );
    },

    tablaSeleccionada: {
      deep: true,
      handler() {
        // Intencionalmente vacío
      },
    },
      'product.modelos': {
    handler(val) {
      console.log("👀 Modelos actualizados:", val)
    },
    deep: true
  }
  },

  methods: {
    formatNumber(value) {
      if (value === null || value === undefined || isNaN(value)) return '';
      return Number(value).toLocaleString("es-AR", {
        style: "currency",
        currency: "ARS",
        minimumFractionDigits: 0,
      });
    },

    async agregarProducto() {
      if (!this.product.nombre || !this.product.precio || !this.product.categoria) {
        this.mostrarToast("❌ Completá los campos obligatorios.");
        return;
      }

      try {
        const response = await axios.post("http://localhost:5000/api/products", this.product);
        this.product.id = response.data.id;
        this.mostrarToast("✅ Producto agregado con éxito");

        this.limpiarFormulario();
        this.activeSection = 1; // ⬅️ Volver a la sección 1

        const modalSuccess = new bootstrap.Modal(document.getElementById("modalProductoAgregado"));
        modalSuccess.show();
      } catch {
        this.mostrarToast("❌ Error al agregar el producto");
      }
    },

    limpiarFormulario() {
      this.product = {
        marca: "", nombre: "", colorPrincipal: "", precio: null,
        descuento: false, tipoDescuento: "porcentaje", porcentajeDescuento: null,
        montoDescuento: null, imagen: "", imagenCarrusel: [],
        categoria: "", etiquetas: [], descripcion: "", detallesTecnicos: [],
        stockFisico: 0, stockDisponible: 0, modelos: [], ocultar: false, nuevo: false,
      };
      this.tablaSeleccionada = null;
      localStorage.removeItem("categoriaSeleccionada");
      localStorage.removeItem("productoDraft");
      this.mostrarToast("🗑 Formulario limpiado correctamente");
    },

    guardarProductoEnLocalStorage() {
      localStorage.setItem("productoDraft", JSON.stringify(this.product));
    },

    cargarProductoDesdeLocalStorage() {
      const draft = localStorage.getItem("productoDraft");
      if (draft) {
        this.product = JSON.parse(draft);
        this.filtrarModeloBase();

        // ⬇️ Agregás esto
        this.product.modelos = (this.product.modelos || []).map((modelo) => {
          if (!modelo.id) {
            return { ...modelo, id: crypto.randomUUID() }
          }
          return modelo
        })
      }
    }
    ,

    limpiarLocalStorage() {
      localStorage.removeItem("productoDraft");
      localStorage.removeItem("categoriaSeleccionada");
      localStorage.removeItem("tablaSeleccionada");
      localStorage.removeItem("modeloTemporalDraft");

      this.product = {
        marca: "", nombre: "", colorPrincipal: "", precio: null,
        descuento: false, tipoDescuento: "porcentaje", porcentajeDescuento: null,
        montoDescuento: null, imagen: "", imagenCarrusel: [],
        categoria: "", etiquetas: [], descripcion: "", detallesTecnicos: [],
        stockFisico: 0, stockDisponible: 0, modelos: [], ocultar: false, nuevo: false,
      };

      this.modeloTemporal = {
        nombre: "", color: "", imagen: "", precio: 0,
        descuento: false, porcentajeDescuento: 0, imagenCarrusel: [],
      };

      this.modeloSeleccionado = 0;
      this.tablaSeleccionada = null;
      this.$refs.modalConfirmarLimpieza?.cerrar();
      this.mostrarToast("🗑 Formulario reseteado correctamente.");
    },

    inicializarModeloPredeterminado() {
      if (!this.product.modelos.length && this.product.nombre && this.product.precio) {
        this.product.modelos.unshift({
          nombre: this.product.nombre,
          color: this.product.colorPrincipal || "Predeterminado",
          imagen: this.product.imagen,
          precio: this.product.precio,
          descuento: this.product.descuento,
          porcentajeDescuento: this.product.porcentajeDescuento,
          imagenCarrusel: [...this.product.imagenCarrusel],
        });
      }
    },

    eliminarModelo(index) {
      this.product.modelos.splice(index + 1, 1);
      localStorage.setItem("productoDraft", JSON.stringify(this.product));
    },

    updateCurrentIndex(index) {
      this.currentIndex = Math.max(0, index);
    },

    updateSlideIndex(swiper) {
      this.currentSlideIndex = swiper.activeIndex + 1;
    },

    cargarLocalStorage() {
      const draft = localStorage.getItem("productoDraft");
      if (!draft) return;
      this.product = JSON.parse(draft);
      this.filtrarModeloBase();
      this.modeloSeleccionado = this.product.modelos.length ? 0 : null;
    },

    filtrarModeloBase() {
      const base = {
        nombre: this.product.nombre,
        color: this.product.colorPrincipal,
        imagen: this.product.imagen,
        precio: this.product.precio,
        imagenCarrusel: JSON.stringify(this.product.imagenCarrusel || []),
      };

      this.product.modelos = this.product.modelos.filter((modelo) => {
        return (
          modelo.nombre !== base.nombre ||
          modelo.color !== base.color ||
          modelo.imagen !== base.imagen ||
          modelo.precio !== base.precio ||
          JSON.stringify(modelo.imagenCarrusel || []) !== base.imagenCarrusel
        );
      });
    },

    cargarDescripciones() {
      const data = localStorage.getItem("descripciones");
      if (data) {
        this.descripciones = JSON.parse(data);
      }
    },

    abrirModalSecundario() {
      const modal = new bootstrap.Modal(document.getElementById("modalCrearTabla"));
      modal.show();
    },

    mostrarToast(mensaje, tipo = 'info', titulo = 'Notificación') {
      this.$refs.toastRef?.mostrar(titulo, mensaje, tipo);
    },

    toggleOcultar() {
      this.mostrarToast(
        this.product.ocultar
          ? "🔒 Producto oculto. No será visible en la página."
          : "✅ Producto visible para los usuarios."
      );

      this.$nextTick(() => {
        const tooltipTriggerList = [].slice.call(
          document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));
      });
    },

    manejarEtiquetaDesdeModal(etiquetaObj) {
      const nombre = etiquetaObj.nombre;

      if (!this.etiquetasDisponibles.find((e) => e.nombre === nombre)) {
        this.etiquetasDisponibles.push(etiquetaObj);
      }

      this.nuevaEtiquetaSeleccionada = etiquetaObj;

      if (!this.product.etiquetas.includes(nombre)) {
        this.product.etiquetas.push(nombre);
        this.mostrarToast(`✅ Etiqueta "${nombre}" agregada al producto`);
      } else {
        this.mostrarToast(`⚠️ La etiqueta "${nombre}" ya estaba agregada`);
      }
    },

    manejarCategoriaDesdeModal(categoriaObj) {
      if (!categoriaObj || !categoriaObj.nombre) return;
      const nombre = categoriaObj.nombre;

      if (!this.categorias.find(cat => cat.nombre === nombre)) {
        this.categorias.push(categoriaObj);
      }

      this.product.categoria = nombre;
      this.selectKey++;
      this.mostrarToast(`✅ Categoría "${nombre}" agregada y seleccionada`);
    },

    abrirModalVistaPrevia() {
      this.mostrarVistaPrevia = true;
      nextTick(() => {
        setTimeout(() => {
          const modalElement = document.getElementById("modalVistaPrevia");
          if (modalElement && window.bootstrap?.Modal) {
            const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
            modal.show();
          }
        }, 100);
      });
    },

    agregarEtiquetaDesdeModal(etiqueta) {
      if (!this.product.etiquetas.includes(etiqueta)) {
        this.product.etiquetas.push(etiqueta);
        this.mostrarToast(`✅ Etiqueta "${etiqueta}" agregada`);
      } else {
        this.mostrarToast(`⚠️ La etiqueta "${etiqueta}" ya existe`);
      }
    },

    abrirModalLimpieza() {
      this.$refs.modalConfirmarLimpieza?.abrir();
    },

    abrirModalCategoriasEtiquetas() {
      this.mostrarModalCategorias = true;
    },
    actualizarModelos(modelosActualizados) {
      console.log("🧹 Nuevos modelos después de eliminar:", modelosActualizados);
      this.product.modelos = modelosActualizados;
    }





  }

};
</script>

<style scoped>
.main-container {
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  display: flex;
  align-items: stretch;
  height: 100vh;
}

/* Inputs */
.contenedorForm {
  display: flex;
  flex: 1;
  gap: 20px;
  padding: 20px;
  justify-content: center;
  height: 100vh;
}

.seccionForm {
  flex: 0.5;
  max-width: 500px;
  max-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  padding-right: 15px;
  /* ⬅️ acá está la magia */
  scrollbar-gutter: stable both-edges;
  /* ⛑ si el navegador lo soporta */
}

/* Scroll personalizado */
.seccionForm::-webkit-scrollbar {
  width: 10px;
}

.seccionForm::-webkit-scrollbar-track {
  background: #1a1a1a;
  /* Fondo canal oscuro */
  border-radius: 8px;
}

.seccionForm::-webkit-scrollbar-thumb {
  background-color: var(--colorTerciario);
  /* Dorado */
  border-radius: 8px;
  border: 2px solid #1a1a1a;
}

.seccionForm::-webkit-scrollbar-thumb:hover {
  background-color: var(--colorTerciarioHover);
}

/* ❌ Eliminamos flechitas feas */
.seccionForm::-webkit-scrollbar-button {
  display: none;
}

.seccionForm::-webkit-scrollbar-button:vertical:decrement {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23fff' d='M0,6 L5,1 L10,6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}

.seccionForm::-webkit-scrollbar-button:vertical:increment {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23fff' d='M0,4 L5,9 L10,4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}

.contenedorTitulo {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: var(--fuentePrincipal);
}

.tituloGeneral {
  color: var(--colorTerciario);
  padding: 10px;
  border-radius: 10px;
  font-size: 2rem;
}


.contenedorTituloSeccion {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -30px;
  margin-bottom: 20px;
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
  color: #3a3a3a;
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
  border-color: #4a90e2;
  box-shadow: 0 0 8px rgba(74, 144, 226, 0.3);
  outline: none;
}

.formularioCampo input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #4a90e2;
  cursor: pointer;
}

/* Precios -- Seccion 1  */
.contenedorDescuento {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-direction: row;
}

.checkboxDescuento {
  margin-top: 4px;
  width: 18px;
  height: 18px;
  accent-color: #4a90e2;
  cursor: pointer;
}

.campoDescuento {
  display: flex;
  justify-content: start;
  gap: 15px;
}
</style>

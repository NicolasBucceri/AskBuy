<template>
  <div class="modal fade show d-block" id="modalCategoriasEtiquetas" tabindex="-1"
    aria-labelledby="modalCategoriasEtiquetasLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalCategoriasEtiquetasLabel">Administrar Categorías y Etiquetas</h5>
          <button type="button" class="btn-close" @click="$emit('cerrar')" aria-label="Cerrar"></button>
        </div>

        <div class="modal-body">
          <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
              <button class="nav-link active" id="categorias-tab" data-bs-toggle="tab" data-bs-target="#categorias-pane"
                type="button" role="tab" aria-controls="categorias-pane" aria-selected="true">Categorías</button>
            </li>
            <li class="nav-item" role="presentation">
              <button class="nav-link" id="etiquetas-tab" data-bs-toggle="tab" data-bs-target="#etiquetas-pane"
                type="button" role="tab" aria-controls="etiquetas-pane" aria-selected="false">Etiquetas</button>
            </li>
          </ul>

          <div class="tab-content mt-3" id="myTabContent">
            <!-- CATEGORÍAS -->
            <div class="tab-pane fade show active" id="categorias-pane" role="tabpanel"
              aria-labelledby="categorias-tab">
              <h5>Lista de Categorías</h5>
              <p v-if="categorias.length === 0" class="text-muted">No hay categorías registradas.</p>

              <table v-if="categorias.length > 0" class="table table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>#</th>
                    <th>Nombre de la Categoría</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(categoria, index) in categorias" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>
                      <input v-if="categoria.editando" type="text" v-model="categoria.nombre" class="form-control">
                      <span v-else>{{ categoria.nombre }}</span>
                    </td>
                    <td>
                      <button v-if="!categoria.editando" class="btn btn-warning btn-sm me-2"
                        @click="habilitarEdicion(categoria)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button v-if="categoria.editando" class="btn btn-success btn-sm me-2"
                        @click="guardarEdicion(categoria)">
                        <i class="fas fa-check"></i>
                      </button>
                      <button class="btn btn-danger btn-sm" @click="eliminarCategoria(categoria)">
                        <i class="fas fa-trash-alt"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div class="mt-3">
                <label for="nuevaCategoria">Nueva Categoría:</label>
                <input type="text" v-model="nuevaCategoria" id="nuevaCategoria" class="form-control"
                  placeholder="Ejemplo: Monitores" />
                <button class="btn btn-primary mt-2" @click="guardarCategoria">Agregar Categoría</button>
              </div>
            </div>

            <!-- ETIQUETAS -->
            <div class="tab-pane fade" id="etiquetas-pane" role="tabpanel" aria-labelledby="etiquetas-tab">
              <h5>Lista de Etiquetas</h5>
              <p v-if="etiquetasDisponibles.length === 0" class="text-muted">No hay etiquetas registradas.</p>

              <table v-if="etiquetasDisponibles.length > 0" class="table table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>#</th>
                    <th>Nombre de la Etiqueta</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(etiqueta, index) in etiquetasDisponibles" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>
                      <input v-if="etiqueta.editando" type="text" v-model="etiqueta.nombre" class="form-control">
                      <span v-else>{{ etiqueta.nombre || 'Sin nombre' }}</span>
                    </td>
                    <td>
                      <button v-if="!etiqueta.editando" class="btn btn-warning btn-sm me-2"
                        @click="habilitarEdicionEtiqueta(etiqueta)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button v-if="etiqueta.editando" class="btn btn-success btn-sm me-2"
                        @click="guardarEdicionEtiqueta(etiqueta)">
                        <i class="fas fa-check"></i>
                      </button>
                      <button class="btn btn-danger btn-sm" @click="eliminarEtiqueta(etiqueta)">
                        <i class="fas fa-trash-alt"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div class="mt-3">
                <label for="nuevaEtiqueta">Nueva Etiqueta:</label>
                <input type="text" v-model="nuevaEtiqueta" id="nuevaEtiqueta" class="form-control"
                  placeholder="Ejemplo: Destacado" />
                <button class="btn btn-primary mt-2" @click="guardarEtiqueta">Agregar Etiqueta</button>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('cerrar')">Cerrar</button>
        </div>
      </div>
    </div>
  </div>

  <ModalConfirmacion ref="modalConfirmacion" :mensaje="mensajeConfirmacion" @confirmar="ejecutarEliminacion" />

</template>


<script>
import axios from 'axios';
import ModalConfirmacion from '../Modals/ModalConfirmacion.vue';

export default {
  components: {
    ModalConfirmacion
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      categorias: [],
      nuevaCategoria: '',
      categoriaAEliminar: null,

      etiquetasDisponibles: [],
      nuevaEtiqueta: '',
      etiquetaAEliminar: null,

      mensajeConfirmacion: '',
      accionConfirmacion: null,
    };
  },

  // Si el modal se vuelve visible, recargá data
  watch: {
    visible(val) {
      if (val) {
        this.fetchCategorias();
        this.fetchEtiquetas();
      }
    }
  },

  // También si ya estaba visible desde el principio
  mounted() {
    if (this.visible) {
      this.fetchCategorias();
      this.fetchEtiquetas();
    }
  },

  methods: {
    // =======================
    // 🔄 Cargar desde backend
    // =======================
    async fetchCategorias() {
      try {
        const res = await axios.get("http://localhost:5000/api/categorias");
        this.categorias = res.data.map(cat =>
          typeof cat === 'string' ? { nombre: cat } : cat
        );
      } catch (err) {
        this.$emit("toast", "❌ Error al cargar categorías");
      }
    },

    async fetchEtiquetas() {
      try {
        const res = await axios.get("http://localhost:5000/api/etiquetas");
        this.etiquetasDisponibles = res.data;
      } catch (err) {
        this.$emit("toast", "❌ Error al cargar etiquetas");
      }
    },

    // =======================
    // ➕ Guardar
    // =======================
    async guardarCategoria() {
      const nombre = this.nuevaCategoria.trim();
      if (!nombre) return;
      try {
        await axios.post("http://localhost:5000/api/categorias", { nombre });
        this.categorias.push({ nombre });
        this.nuevaCategoria = '';
        this.$emit("toast", "✅ Categoría agregada");
      } catch (err) {
        this.$emit("toast", "❌ Error al guardar categoría");
      }
    },

    async guardarEtiqueta() {
      const nombre = this.nuevaEtiqueta.trim();
      if (!nombre) return;
      try {
        const res = await axios.post("http://localhost:5000/api/etiquetas", { nombre });
        this.etiquetasDisponibles.push(res.data);
        this.nuevaEtiqueta = '';
        this.$emit("toast", "✅ Etiqueta agregada");
      } catch (err) {
        this.$emit("toast", "❌ Error al guardar etiqueta");
      }
    },

    // =======================
    // ✏️ Editar
    // =======================
    habilitarEdicion(categoria) {
      this.categorias.forEach(cat => cat.editando = false);
      categoria.oldNombre = categoria.nombre;
      categoria.editando = true;
    },

    async guardarEdicion(categoria) {
      const nuevoNombre = categoria.nombre.trim();
      if (!nuevoNombre) {
        this.$emit("toast", "⚠️ El nombre no puede estar vacío");
        return;
      }
      try {
        await axios.put(`http://localhost:5000/api/categorias/${encodeURIComponent(categoria.oldNombre)}`, {
          nombre: nuevoNombre
        });
        categoria.editando = false;
        this.$emit("toast", "✅ Categoría actualizada");
      } catch {
        this.$emit("toast", "❌ Error al actualizar categoría");
      }
    },

    habilitarEdicionEtiqueta(etiqueta) {
      this.etiquetasDisponibles.forEach(e => e.editando = false);
      etiqueta.oldNombre = etiqueta.nombre;
      etiqueta.editando = true;
    },

    async guardarEdicionEtiqueta(etiqueta) {
      const nuevoNombre = etiqueta.nombre.trim();
      if (!nuevoNombre) {
        this.$emit("toast", "⚠️ El nombre no puede estar vacío");
        return;
      }
      try {
        await axios.put(`http://localhost:5000/api/etiquetas/${etiqueta.id}`, {
          nombre: nuevoNombre
        });
        etiqueta.editando = false;
        this.$emit("toast", "✅ Etiqueta actualizada");
      } catch {
        this.$emit("toast", "❌ Error al actualizar etiqueta");
      }
    },

    // =======================
    // 🗑️ Eliminar
    // =======================
    async eliminarCategoria(categoria) {
      this.abrirModalConfirmacion(
        `¿Eliminar la categoría "${categoria.nombre}"?`,
        async () => {
          try {
            await axios.delete(`http://localhost:5000/api/categorias/${encodeURIComponent(categoria.nombre)}`);
            this.categorias = this.categorias.filter(cat => cat.nombre !== categoria.nombre);
            this.$emit("toast", "✅ Categoría eliminada");
          } catch {
            this.$emit("toast", "❌ Error al eliminar categoría");
          }
        }
      );
    },

    async eliminarEtiqueta(etq) {
      this.abrirModalConfirmacion(
        `¿Eliminar la etiqueta "${etq.nombre}"?`,
        async () => {
          try {
            await axios.delete(`http://localhost:5000/api/etiquetas/${etq.id}`);
            this.etiquetasDisponibles = this.etiquetasDisponibles.filter(e => e.id !== etq.id);
            this.$emit("toast", "✅ Etiqueta eliminada");
          } catch {
            this.$emit("toast", "❌ Error al eliminar etiqueta");
          }
        }
      );
    },

    // =======================
    // ⚠️ Confirmaciones
    // =======================
    ejecutarEliminacion() {
      if (typeof this.accionConfirmacion === 'function') {
        this.accionConfirmacion();
      }
    },

    abrirModalConfirmacion(mensaje, accion) {
      this.mensajeConfirmacion = mensaje;
      this.accionConfirmacion = accion;
      this.$refs.modalConfirmacion.abrir();
    }
  }
};
</script>



<style scoped>
/* Fondo del modal */
.modal-content {
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  color: #f1f1f1;
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
}

/* Encabezado del modal */
.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #ffc107;
}

/* Botón cerrar */
.btn-close {
  filter: invert(1);
}

/* Tabs */
.nav-tabs .nav-link {
  background-color: transparent;
  border: none;
  color: #ccc;
  transition: all 0.3s ease;
}

.nav-tabs .nav-link.active {
  color: #ffc107;
  font-weight: bold;
  border-bottom: 2px solid #ffc107;
}

/* Tab panels */
.tab-pane {
  padding: 10px;
}

/* Tablas */
.table {
  background-color: transparent;
  color: #fff;
}

.table thead {
  background-color: #333;
  color: #ffc107;
}

.table-striped > tbody > tr:nth-of-type(odd) {
  background-color: rgba(255, 255, 255, 0.05);
}
/* Forzamos visibilidad en filas con estilos oscuros o inactivos */
.table tbody tr {
  color: #f1f1f1 !important;
  opacity: 1 !important;
}

/* También los <td> y <th> individualmente */
.table td, .table th {
  color: #ffffff !important;
  opacity: 1 !important;
}

/* Para casos que vienen con muted o estilos automáticos */
.table .text-muted {
  color: #bbbbbb !important;
  opacity: 0.85 !important;
}

/* Inputs */
input.form-control {
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: #fff;
}

input.form-control:focus {
  border-color: #ffc107;
  box-shadow: 0 0 8px rgba(255, 193, 7, 0.4);
}

/* Botones */
.btn {
  transition: all 0.2s ease-in-out;
  font-weight: 500;
}

.btn-primary {
  background-color: #ffc107;
  border: none;
  color: #000;
}

.btn-primary:hover {
  background-color: #e6b800;
}

.btn-warning {
  background-color: #ff9800;
  border: none;
  color: #000;
}

.btn-warning:hover {
  background-color: #e67e00;
}

.btn-success {
  background-color: #28a745;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  border: none;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* Footer */
.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>


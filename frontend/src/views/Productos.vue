<template>
  <div class="productosVista">
    <h1 class="titulo">Todos los productos</h1>

    <div class="layoutPrincipal">
      <!-- FILTROS -->
      <aside class="sidebarFiltros">
        <h3>Filtros</h3>
        <div class="filtroCampo">
          <label>Categoría</label>
          <select v-model="filtroCategoria">
            <option value="">Todas</option>
            <option v-for="cat in categoriasUnicas" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <div class="filtroCampo">
          <label>Marca</label>
          <select v-model="filtroMarca">
            <option value="">Todas</option>
            <option v-for="marca in marcasUnicas" :key="marca" :value="marca">{{ marca }}</option>
          </select>
        </div>

        <div class="filtroCampo">
          <label>Color</label>
          <select v-model="filtroColor">
            <option value="">Todos</option>
            <option v-for="color in coloresUnicos" :key="color" :value="color">{{ color }}</option>
          </select>
        </div>

        <div class="filtroCampo">
          <label>Con descuento</label>
          <select v-model="filtroDescuento">
            <option value="">Todos</option>
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
        </div>

        <div class="filtroCampo">
          <label>Etiqueta</label>
          <select v-model="filtroEtiqueta">
            <option value="">Todas</option>
            <option v-for="et in etiquetasUnicas" :key="et" :value="et">{{ et }}</option>
          </select>
        </div>

      </aside>

      <!-- PRODUCTOS -->
      <section class="contenidoProductos">
        <div v-if="productos.length === 0" class="mensajeCargando">
          Cargando productos...
        </div>

        <div class="gridProductos">
          <div v-for="prod in productosFiltrados" :key="prod.id" class="cardProducto">
            <!-- BOTÓN FAVORITO -->
            <button class="btn-fav" @click.stop="toggleFavorito(prod.id)"
              :aria-label="esFavorito(prod.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
              <i :class="esFavorito(prod.id) ? 'fas fa-heart' : 'far fa-heart'"></i>
            </button>

            <!-- LINK A DETALLE -->
            <router-link :to="`/producto/${prod.id}`" class="contenidoCard">
              <img :src="prod.imagen" alt="Imagen" class="imagen" />
              <h3>{{ prod.nombre }}</h3>

              <!-- Precio original tachado -->
              <p class="precio-original" v-if="prod.descuento && prod.porcentajeDescuento">
                {{ formatPrice(calcularPrecioOriginal(prod)) }}
              </p>

              <!-- Precio con descuento o precio normal -->
              <p :class="prod.descuento ? 'precio-descuento' : 'precio'">
                {{ formatPrice(prod.precio) }}
              </p>

              <!-- Badge de descuento -->
              <span v-if="prod.descuento && prod.porcentajeDescuento" class="badge-descuento">
                -{{ prod.porcentajeDescuento }}% OFF
              </span>

              <p class="categoria">{{ prod.categoria }}</p>
            </router-link>
          </div>
        </div>

      </section>
    </div>
  </div>

  <Notificacion ref="notiRef" />


</template>

<script>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { auth, db } from '../firebase'
import { doc, getDoc, setDoc } from 'firebase/firestore'
import Notificacion from '../components/ToastNotificacion.vue'

export default {
  components: { Notificacion },

  data() {
    return {
      productos: [],
      favoritosIds: [],
      favoritos: [],
      filtroCategoria: '',
      filtroMarca: '',
      filtroColor: '',
      filtroDescuento: '',
      filtroEtiqueta: '',
      terminoBusqueda: '',
      router: null,
    }
  },

  mounted() {
    const route = useRoute()
    this.router = useRouter()

    const query = route.query
    this.filtroCategoria = query.categoria || ''
    this.filtroMarca = query.marca || ''
    this.filtroColor = query.color || ''
    this.filtroDescuento = query.descuento || ''
    this.filtroEtiqueta = query.etiqueta || ''
    this.terminoBusqueda = (query.buscar || '').toLowerCase()

    this.cargarProductos()
    this.cargarFavoritos()
  },

  watch: {
    filtroCategoria: 'actualizarQuery',
    filtroMarca: 'actualizarQuery',
    filtroColor: 'actualizarQuery',
    filtroDescuento: 'actualizarQuery',
    filtroEtiqueta: 'actualizarQuery',
    terminoBusqueda: 'actualizarQuery',
  },

  methods: {
    actualizarQuery() {
      this.router.replace({
        query: {
          categoria: this.filtroCategoria || undefined,
          marca: this.filtroMarca || undefined,
          color: this.filtroColor || undefined,
          descuento: this.filtroDescuento || undefined,
          etiqueta: this.filtroEtiqueta || undefined,
          buscar: this.terminoBusqueda || undefined,
        }
      })
    },

    async cargarProductos() {
      try {
        const res = await axios.get("http://localhost:5000/api/products")
        this.productos = res.data
      } catch (err) {
        console.error("Error al cargar productos:", err)
      }
    },

    async cargarFavoritos() {
      const user = auth.currentUser
      if (user) {
        const userRef = doc(db, "usuarios", user.uid)
        const docSnap = await getDoc(userRef)
        const idsFavoritos = docSnap.exists() ? (docSnap.data().favoritos || []) : []

        this.favoritosIds = idsFavoritos
        this.favoritos = this.productos.filter(p => idsFavoritos.includes(p.id))
      }
    },

    formatPrice(value) {
      return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0
      }).format(value || 0)
    },

    mostrarNotificacion(tipo, titulo, mensaje) {
      this.$refs.notiRef?.mostrar(titulo, mensaje, tipo)
    },

    async toggleFavorito(idProducto) {
      const user = auth.currentUser
      if (!user) {
        this.mostrarNotificacion('error', 'Iniciá sesión', 'Tenés que iniciar sesión para usar favoritos')

        setTimeout(() => {
          this.router.push('/login')
        }, 2000)

        return
      }

      const userRef = doc(db, "usuarios", user.uid)

      if (this.favoritosIds.includes(idProducto)) {
        this.favoritosIds = this.favoritosIds.filter(id => id !== idProducto)
        this.favoritos = this.favoritos.filter(p => p.id !== idProducto)
        this.mostrarNotificacion('info', 'Eliminado de favoritos', 'Ya no está en tu lista')
      } else {
        const producto = this.productos.find(p => p.id === idProducto)
        if (producto) {
          this.favoritos.push(producto)
          this.favoritosIds.push(idProducto)
          this.mostrarNotificacion('success', 'Agregado a favoritos', 'Lo encontrarás en tu lista')
        }
      }

      await setDoc(userRef, { favoritos: this.favoritosIds }, { merge: true })

      if (window?.cargarProductosFavoritos) {
        window.cargarProductosFavoritos()
      }
    },

    esFavorito(idProducto) {
      return this.favoritosIds.includes(idProducto)
    },

    calcularPrecioOriginal(producto) {
      if (producto.tipoDescuento === 'porcentaje' && producto.porcentajeDescuento) {
        const descuento = Number(producto.porcentajeDescuento)
        const precioConDescuento = Number(producto.precio)
        return Math.round((precioConDescuento * 100) / (100 - descuento))
      }
      return producto.precio
    }
  },

  computed: {
    productosFiltrados() {
      return this.productos.filter(prod => {
        const coincideCategoria = this.filtroCategoria ? prod.categoria === this.filtroCategoria : true
        const coincideMarca = this.filtroMarca ? prod.marca?.trim() === this.filtroMarca : true
        const coincideColor = this.filtroColor ? prod.colorPrincipal?.trim() === this.filtroColor : true
        const coincideDescuento = this.filtroDescuento !== '' ? prod.descuento === (this.filtroDescuento === 'true') : true
        const coincideEtiqueta = this.filtroEtiqueta
          ? prod.etiquetas && prod.etiquetas.includes(this.filtroEtiqueta)
          : true
        const coincideBusqueda = this.terminoBusqueda
          ? prod.nombre.toLowerCase().includes(this.terminoBusqueda)
          : true

        return coincideCategoria && coincideMarca && coincideColor && coincideDescuento && coincideEtiqueta && coincideBusqueda
      })
    },
    categoriasUnicas() {
      return [...new Set(this.productos.map(p => p.categoria).filter(Boolean))]
    },
    marcasUnicas() {
      return [...new Set(
        this.productos
          .filter(p => !this.filtroCategoria || p.categoria === this.filtroCategoria)
          .map(p => p.marca?.trim())
          .filter(Boolean)
      )]
    },
    coloresUnicos() {
      return [...new Set(
        this.productos
          .filter(p => !this.filtroCategoria || p.categoria === this.filtroCategoria)
          .map(p => p.colorPrincipal?.trim())
          .filter(Boolean)
      )]
    },
    etiquetasUnicas() {
      return [...new Set(this.productos.flatMap(p => p.etiquetas || []))]
    }
  }
}
</script>


<style scoped>
.productosVista {
  padding: 2rem;
}

.titulo {
  text-align: center;
  font-family: var(--fuentePrincipal);
  margin-bottom: 2rem;
}

.gridProductos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 2rem;
}

.cardProducto {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 1.5rem;
  background: #fff;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 100%;
  border: 1px solid transparent;
}

.cardProducto:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  border-color: var(--main-color);
}

.cardProducto .imagen {
  height: 160px;
  object-fit: contain;
  margin-bottom: 1rem;
}

.cardProducto h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  line-height: 1.4;
  color: #1f2937;
  /* gris oscuro elegante */
}

.cardProducto .precio {
  font-size: 1rem;
  font-weight: bold;
  color: #1d4ed8;
  /* azul intenso */
  margin-bottom: 0.2rem;
}

.precio-original {
  font-size: 0.9rem;
  color: #9ca3af;
  text-decoration: line-through;
  margin-bottom: 0.2rem;
}

.imagen {
  width: 100%;
  height: 180px;
  object-fit: contain;
  margin-bottom: 0.5rem;
}

.precio {
  font-weight: bold;
  color: var(--colorTextoPrincipal);
}

.precio-original {
  font-size: 0.9rem;
  color: #9ca3af;
  text-decoration: line-through;
  margin-bottom: 0.2rem;
}

.precio-descuento {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1d4ed8;
  margin-bottom: 0.3rem;
}

.badge-descuento {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background-color: #16a34a;
  color: #fff;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 2;
}


.categoria {
  font-size: 0.9rem;
  color: #777;
}

.layoutPrincipal {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.sidebarFiltros {
  position: sticky;
  top: 2rem;
  /* distancia desde el top al hacer scroll */
  height: fit-content;
  /* se ajusta a su contenido */
  /* ya tenés lo siguiente, lo dejamos */
  flex: 0 0 220px;
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid #ddd;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: var(--fuentePrincipal);
}


.contenidoProductos {
  flex: 1;
}

.gridProductos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 2rem;
}

.sidebarFiltros {
  flex: 0 0 220px;
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid #ddd;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: var(--fuentePrincipal);
}

.sidebarFiltros h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--black900);
}

.filtroCampo {
  margin-bottom: 1.2rem;
}

.filtroCampo label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: var(--black900);
}

.filtroCampo select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #fafafa;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.filtroCampo select:focus {
  border-color: var(--main-color);
  outline: none;
}

.cardProducto {
  position: relative;
}

.btn-fav {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.3rem;
  z-index: 10;
  color: #bbb;
  transition: transform 0.2s ease, color 0.2s ease;
}

.btn-fav:hover {
  transform: scale(1.1);
  color: var(--main-color);
}

.fas.fa-heart {
  color: red;
  animation: latido 0.3s ease;
}

@keyframes latido {
  0% {
    transform: scale(1);
  }

  30% {
    transform: scale(1.4);
  }

  60% {
    transform: scale(1);
  }
}


@media (max-width: 1024px) {
  .layoutPrincipal {
    flex-direction: column;
  }

  .sidebarFiltros {
    position: relative;
    top: 0;
    width: 100%;
    flex: 1;
    margin-bottom: 2rem;
  }

  .gridProductos {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .cardProducto .imagen {
    height: 140px;
  }

  .cardProducto h3 {
    font-size: 1rem;
  }

  .cardProducto .precio {
    font-size: 0.95rem;
  }

  .cardProducto .categoria {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .gridProductos {
    grid-template-columns: 1fr;
  }

  .cardProducto {
    padding: 1rem;
  }

  .cardProducto .imagen {
    height: 120px;
  }

  .cardProducto h3 {
    font-size: 0.95rem;
  }
}
</style>

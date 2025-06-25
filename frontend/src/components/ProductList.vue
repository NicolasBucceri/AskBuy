<template>
  <div class="listaProductos">

    <div v-for="carrusel in carruselesHome" :key="carrusel.id" class="carrusel-dinamico">
      <div class="seccionTitulo">
        <h2 class="category-title">{{ carrusel.nombre }}</h2>
        <div class="lineaDecorativa"></div>
      </div>

      <swiper :slides-per-view="3" space-between="20" navigation pagination loop>
        <swiper-slide v-for="product in obtenerProductosOrdenados(carrusel.productos).slice(0, 6)" :key="product.id">
          <div class="productoCard">
            <span v-if="product.descuento && product.porcentajeDescuento" class="etiquetaDescuento">
              -{{ product.porcentajeDescuento }}%
            </span>

            <span class="iconoFavorito" @click.stop="toggleFavorito(product.id)">
              <i :class="esFavorito(product.id) ? 'fas fa-heart corazonLleno' : 'far fa-heart corazonVacio'"></i>
            </span>

            <router-link :to="`/producto/${product.id}`" class="cardLink">
              <img :src="product.imagen" alt="Imagen del producto" class="imagenProducto" />
              <h3 class="nombreProducto">{{ product.nombre }}</h3>

              <div class="precioContainer">
                <p v-if="product.descuento && product.porcentajeDescuento" class="precioOriginal">
                  {{ formatPrice(calcularPrecioOriginal(product)) }}
                </p>

                <div class="precioYAccion">
                  <p class="precioProducto">
                    <span class="precioTexto">{{ formatPrice(product.precio) }}</span>
                    <span class="precioOjo"><i class="fas fa-eye"></i></span>
                  </p>
                </div>

                <p class="infoExtra">¡Envío gratis a todo el país!</p>
              </div>
            </router-link>
          </div>
        </swiper-slide>
      </swiper>

      <p v-if="filtrarProductosPorID(carrusel.productos).length === 0" class="text-muted">
        No hay productos cargados aún.
      </p>

    </div>
  </div>

  <Notificacion ref="notiRef" />

</template>

<script>
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/swiper-bundle.css';
import { auth, db } from '../firebase';
import { ref } from 'vue'
import { doc, getDoc, setDoc } from 'firebase/firestore';
import Notificacion from '../components/ToastNotificacion.vue'

export default {
  components: {
    Swiper,
    SwiperSlide,
    Notificacion
  },
  data() {
    return {
      products: [],
      monitorProducts: [],
      headphoneProducts: [],
      masVendidos: [],
      ofertas: [],
      nuevos: [],
      favoritos: [],
      favoritosIds: [],
      carruselesHome: [],
      statusMessage: ''
    };
  },
  async mounted() {
    await this.fetchProducts();
    await this.cargarFavoritos();
    await this.cargarCarruseles();
  },
  methods: {
    async cargarCarruseles() {
      try {
        const response = await fetch('http://localhost:5000/api/carruseles');
        const data = await response.json();
        this.carruselesHome = data.sort((a, b) => (a.orden ?? 0) - (b.orden ?? 0)); // 🔥 ORDEN VISUAL
      } catch (error) {
        console.error('Error al obtener carruseles:', error);
        this.statusMessage = 'Error al cargar los carruseles.';
      }
    },
    filtrarProductosPorID(ids) {
      if (!Array.isArray(ids)) return []
      const mapa = new Map(this.products.map(p => [String(p.id), p]));
      return ids.map(id => mapa.get(String(id))).filter(Boolean);
    },

    async fetchProducts() {
      try {
        const response = await fetch('http://localhost:5000/api/products');
        const data = await response.json();
        this.products = data;
        this.filterCategories();
      } catch (error) {
        console.error('Error al obtener productos:', error);
        this.statusMessage = 'Error al cargar los productos.';
      }
    },

    async cargarFavoritos() {
      const user = auth.currentUser;
      if (!user) return;
      try {
        const userRef = doc(db, "usuarios", user.uid);
        const docSnap = await getDoc(userRef);
        const idsFavoritos = docSnap.exists() ? (docSnap.data().favoritos || []) : [];
        this.favoritosIds = idsFavoritos;
      } catch (error) {
        console.error('Error al cargar favoritos:', error);
      }
    },

    filterCategories() {
      this.monitorProducts = this.products.filter(product =>
        !product.oculto && product.categoria.toLowerCase() === 'monitor'
      );

      this.headphoneProducts = this.products.filter(product =>
        !product.oculto && product.categoria.toLowerCase() === 'auriculares'
      );

      this.masVendidos = this.products.filter(product =>
        !product.oculto && product.etiquetas?.some(etiqueta =>
          etiqueta.toLowerCase().trim() === 'mas vendido'
        )
      );

      this.ofertas = this.products.filter(product =>
        !product.oculto && product.etiquetas?.some(etiqueta =>
          etiqueta.toLowerCase().trim() === 'oferta'
        )
      );

      this.nuevos = this.products.filter(product =>
        !product.oculto && product.etiquetas?.some(etiqueta =>
          etiqueta.toLowerCase().trim() === 'nuevo ingreso'
        )
      );
    },

    formatPrice(value) {
      if (!value || isNaN(value)) return '$0';
      return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    },

    calcularPrecioOriginal(product) {
      if (product.tipoDescuento === 'porcentaje' && product.porcentajeDescuento) {
        const descuento = Number(product.porcentajeDescuento);
        const precio = Number(product.precio);
        return Math.round((precio * 100) / (100 - descuento));
      }
      return null;
    },

    async toggleFavorito(idProducto) {
      const user = auth.currentUser

      if (!user) {
        // 🔔 Mostrar noti y redirigir
        this.$refs.notiRef?.mostrar('Favoritos', 'Tenés que iniciar sesión para guardar favoritos', 'error')
        setTimeout(() => {
          this.$router.push('/login') // o la ruta que tengas
        }, 2000)
        return
      }

      const userRef = doc(db, "usuarios", user.uid)

      if (this.favoritosIds.includes(idProducto)) {
        this.favoritosIds = this.favoritosIds.filter(id => id !== idProducto)
        this.$refs.notiRef?.mostrar('Favoritos', 'Eliminado de favoritos', 'info')
      } else {
        this.favoritosIds.push(idProducto)
        this.$refs.notiRef?.mostrar('Favoritos', 'Agregado a favoritos', 'success')
      }

      await setDoc(userRef, { favoritos: this.favoritosIds }, { merge: true })

      if (window?.cargarProductosFavoritos) {
        window.cargarProductosFavoritos()
      }
    },

    esFavorito(idProducto) {
      return this.favoritosIds.includes(idProducto);
    },

    verProducto(id) {
      this.$router.push(`/producto/${id}`);
    },
    obtenerProductosOrdenados(ids) {
      const mapa = new Map(this.products.map(p => [String(p.id), p]));
      return ids.map(id => mapa.get(String(id))).filter(Boolean);
    }

  }
};
</script>


<style scoped>
/* Estilos generales */
.listaProductos {
  padding: 20px;
  background-color: #f7fafc;
  min-height: 100vh;
}

.destacados h2,
.masVendidos h2,
.ofertas h2,
.nuevos h2 {
  font-family: var(--fuentePrincipal);
  font-size: 1.5rem;
  font-weight: 400;
}

/* Estilos del carrusel */
.monitor-carousel,
.headphone-carousel {
  margin-bottom: 40px;
}

.category-title {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

/* Swiper */
.swiper-container {
  width: 100%;
  height: 100%;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: stretch;
  /* 🔥 Clave para que las cards tengan misma altura */
}

.swiper-button-next,
.swiper-button-prev {
  color: #4a90e2;
}

.swiper-pagination-bullet {
  background-color: #4a90e2;
}

.swiper-pagination-bullet-active {
  background-color: #1d72b8;
}

/* CARD */
.productoCard {
  width: 100%;
  max-width: 280px;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  padding: 16px;
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.productoCard:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
}

/* Icono favorito */
.iconoFavorito {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 1.4rem;
  color: #d1d5db;
  cursor: pointer;
  z-index: 1;
  transition: color 0.3s;
}

.corazonLleno {
  color: #ef4444;
}

.corazonVacio:hover {
  color: #f87171;
}

.precioProducto {
  background-color: #1d4ed8;
  color: white;
  padding: 8px 0;
  text-align: center;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 12px;
  margin-bottom: 8px;
  width: 100%;
  transition: background 0.3s ease;
  position: relative;
  overflow: hidden;
}

.precioTexto {
  display: inline-block;
  transition: opacity 0.3s ease;
}

.precioOjo {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 1.1rem;
}

.precioProducto:hover .precioTexto {
  opacity: 0;
}

.precioProducto:hover .precioOjo {
  opacity: 1;
}

.cardLink {
  text-decoration: none;
  color: inherit;
}

.seccionTitulo {
  display: flex;
  align-items: center;
  gap: 16px;
  /* Espacio entre el texto y la línea */
  margin-bottom: 20px;
}

.category-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
}

.lineaDecorativa {
  max-width: 150px;
  margin-bottom: 10px;
  width: 100%;
  height: 3px;
  background: var(--colorSecundario);
  border-radius: 4px;
}






/* Imagen */
.imagenProducto {
  width: 100%;
  height: 180px;
  object-fit: contain;
  margin-bottom: 12px;
}

/* Info producto */
.nombreProducto {
  font-weight: 600;
  font-size: 1rem;
  color: #111827;
  text-align: center;
  margin-bottom: 10px;
}

.precioProducto {
  background-color: #1d4ed8;
  color: white;
  padding: 8px 0;
  text-align: center;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 12px;
  margin-bottom: 8px;
}

.infoExtra {
  font-size: 0.9rem;
  color: #6b7280;
  text-align: center;
}

.precioContainer {
  text-align: center;
  margin-bottom: 8px;
}

.precioOriginal {
  color: #9ca3af;
  text-decoration: line-through;
  font-size: 0.9rem;
  margin: 0;
}

.precioProducto {
  background-color: #1d4ed8;
  color: white;
  padding: 8px 0;
  text-align: center;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 12px;
  margin-top: 4px;
}

.etiquetaDescuento {
  position: absolute;
  top: 12px;
  left: 14px;
  background-color: #dcfce7;
  color: #16a34a;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 8px;
  z-index: 2;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}



/* Responsive Grid si usás fuera del carrusel */
.product-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

@media (min-width: 640px) {
  .product-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (min-width: 768px) {
  .product-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

/* Mensaje de error */
.error-message {
  text-align: center;
  color: #ef4444;
  margin-top: 20px;
}
</style>

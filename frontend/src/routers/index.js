import { createRouter, createWebHistory } from "vue-router";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../firebase"; // tu config Firebase

// Vistas
import HomeView from "../views/HomeView.vue";
import AdminView from "../views/AdminView.vue";
import AddProduct from "../views/AddProduct.vue";
import Contacto from "../views/Contacto.vue";
import QuienesSomos from "../views/QuienesSomos.vue";
import ServiciosUsuario from "../views/ServiciosUsuario.vue";
import Productos from "../views/Productos.vue";
import LoginRegistro from "../views/LoginRegistro.vue";
import Panel from "../views/Panel.vue";
import DetalleProducto from "../views/DetalleProducto.vue";
import Perfil from "../views/Perfil.vue";
import AdminProductos from "../views/AdminProductos.vue";
import ListaUsuarios from "../views/ListaUsuarios.vue";
import AdminDescuentos from "../views/AdminDescuentos.vue";
import VistaFavoritos from "../components/SeccionesDePerfil/VistaFavoritos.vue";
import NotFound from "../views/NotFound.vue";
import AdminAnaliticas from "../views/AdminAnaliticas.vue";
import AdminCarruseles from "../views/AdminCarruseles.vue";
import AdminCargaMasiva from "../views/AdminCargaMasiva.vue";
import AdminServicios from "../views/AdminServicios.vue";
import AdminPedidos from "../views/AdminPedidos.vue";
import Checkout from "../views/Checkout.vue";
import Success from "../views/Success.vue";



const routes = [
  { path: "/", component: HomeView },

  { path: "/admin", component: AdminView },

  { path: "/add-product", name: "AddProduct", component: AddProduct, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/contacto", name: "Contacto", component: Contacto },

  { path: "/quienes-somos", name: "QuienesSomos", component: QuienesSomos },

  { path: "/servicios-usuario", name: "ServiciosUsuario", component: ServiciosUsuario },

  { path: "/productos", name: "Productos", component: Productos },

  { path: "/login-registro", name: "LoginRegistro", component: LoginRegistro },

  { path: "/panel", name: "Panel", component: Panel, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/producto/:id", name: "DetalleProducto", component: DetalleProducto },

  { path: "/perfil", name: "Perfil", component: Perfil },

  { path: "/success", name: "Success", component: Success },

  { path: "/checkout", name: "Checkout", component: Checkout },

  { path: "/adminproductos", name: "AdminProductos", component: AdminProductos, meta: { requiereRol: ["admin"] } },

  { path: "/listausuarios", name: "ListaUsuarios", component: ListaUsuarios, meta: { requiereRol: ["admin"] } },

  { path: "/admindescuentos", name: "AdminDescuentos", component: AdminDescuentos, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/adminanaliticas", name: "AdminAnaliticas", component: AdminAnaliticas, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/admincarruseles", name: "AdminCarruseles", component: AdminCarruseles, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/admincargamasiva", name: "AdminCargaMasiva", component: AdminCargaMasiva, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/adminservicios", name: "AdminServicios", component: AdminServicios, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/adminpedidos", name: "AdminPedidos", component: AdminPedidos, meta: { requiereRol: ["admin", "moderador"] } },

  { path: "/favoritos", name: "VistaFavoritos", component: VistaFavoritos },

  { path: "/404", name: "NotFound", component: NotFound },

  { path: "/:pathMatch(.*)*", redirect: "/404" }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// 🛡 Control de acceso con espera a Firebase
let authReady = false;

router.beforeEach(async (to, from, next) => {
  const requiereRol = to.meta.requiereRol;

  // Ruta pública
  if (!requiereRol) return next();

  const auth = getAuth();

  // 🔒 Esperar que Firebase confirme estado de sesión
  if (!authReady) {
    await new Promise((resolve) => {
      const unsuscribe = onAuthStateChanged(auth, () => {
        authReady = true;
        unsuscribe();
        resolve();
      });
    });
  }

  const user = auth.currentUser;

  if (!user) return next("/login-registro");

  try {
    const docRef = doc(db, "usuarios", user.uid);
    const docSnap = await getDoc(docRef);

    if (!docSnap.exists()) return next("/404");

    const rol = docSnap.data().rol?.toLowerCase() || "usuario";

    if (requiereRol.includes(rol)) {
      return next(); // ✅ Tiene permiso
    } else {
      return next("/404"); // ❌ Acceso denegado
    }
  } catch (error) {
    console.error("Error al verificar rol:", error);
    return next("/404");
  }
});

export default router;

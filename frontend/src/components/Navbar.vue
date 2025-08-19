<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark barraNavegacion">
        <div class="container">
            <a class="navbar-brand" href="/">
                <img src="../assets/Logos/LogoAskBuy.png" alt="AskBuy Logo" class="logo-navbar" />
            </a>


            <button class="navbar-toggler shadow-none border-0" type="button" data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="sidebar offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavbar"
                aria-labelledby="offcanvasNavbarLabel">
                <div class="offcanvas-header text-white border-bottom">
                    <h5 class="offcanvas-title" id="offcanvasNavbarLabel">AskBuy</h5>
                    <button type="button" class="btn-close btn-close-white shadow-none" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>

                <div
                    class="offcanvas-body d-flex flex-column flex-lg-row justify-content-between align-items-center p-4 p-lg-0 gap-4 gap-lg-0">

                    <!-- Links -->
                    <ul class="navbar-nav justify-content-center align-items-center fs-5 flex-grow-1 pe-3">
                        <!-- ADMIN -->
                        <template v-if="userRol === 'admin' || userRol === 'moderador'">

                            <li class="nav-item mx-2">
                                <router-link to="/" class="nav-link">Home</router-link>
                            </li>
                            <li class="nav-item mx-2">
                                <router-link to="/productos" class="nav-link">Tienda</router-link>
                            </li>
                            <li class="nav-item dropdown mx-2">
                                <a class="nav-link dropdown-toggle" href="#" id="nosotrosDropdown" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">
                                    Nosotros
                                </a>
                                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="nosotrosDropdown">
                                    <li><router-link to="/contacto" class="dropdown-item">Contacto</router-link></li>
                                    <li><router-link to="/quienes-somos" class="dropdown-item">Quiénes
                                            Somos</router-link></li>
                                </ul>
                            </li>
                            <li class="nav-item mx-2">
                                <router-link to="/servicios-usuario" class="nav-link">Servicios</router-link>
                            </li>
                            <li class="nav-item mx-2">
                                <router-link to="/panel" class="nav-link">Panel</router-link>
                            </li>
                        </template>

                        <!-- USUARIO COMÚN -->
                        <template v-else>
                            <li class="nav-item mx-2">
                                <router-link to="/" class="nav-link">Home</router-link>
                            </li>
                            <li class="nav-item mx-2">
                                <router-link to="/productos" class="nav-link">Tienda</router-link>
                            </li>
                            <li class="nav-item dropdown mx-2">
                                <a class="nav-link dropdown-toggle" href="#" id="nosotrosDropdown" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">
                                    Nosotros
                                </a>
                                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="nosotrosDropdown">
                                    <li><router-link to="/contacto" class="dropdown-item">Contacto</router-link></li>
                                    <li><router-link to="/quienes-somos" class="dropdown-item">Quiénes
                                            Somos</router-link></li>
                                </ul>
                            </li>
                            <li class="nav-item mx-2">
                                <router-link to="/servicios-usuario" class="nav-link">Servicios</router-link>
                            </li>
                        </template>
                    </ul>


                    <!-- Buscador y carrito -->
                    <div class="d-flex flex-column flex-lg-row justify-content-center align-items-center gap-3">
                        <div class="search-box" ref="searchBox" :class="{ 'open': isOpen }" @click.stop>


                            <button type="button" @click="abrirBuscador">
                                <i class="fas fa-search"></i>
                            </button>


                            <input ref="searchInput" type="text" class="form-control mx-1" placeholder="Buscar..."
                                v-model="searchText" @focus="isOpen = true" @blur="handleBlur"
                                @keyup.enter="buscarProductos" />
                        </div>

                        <!-- Carrito -->
                        <button class="cart-btn position-relative" type="button" data-bs-toggle="offcanvas"
                            data-bs-target="#offcanvasCarrito" aria-controls="offcanvasCarrito">
                            <i class="fa-solid fa-cart-shopping"></i>
                            <span class="cart-badge badge rounded-pill bg-danger">{{ cantidadCarrito }}</span>
                        </button>

                    </div>

                    <!-- Autenticación -->
                    <div
                        class="d-flex justify-content-center align-items-center gap-3 auth-buttons flex-column flex-lg-row ms-lg-4">
                        <template v-if="user">
                            <router-link to="/perfil" custom v-slot="{ navigate }">
                                <span @click="navigate" class="text-white fw-bold text-decoration-none cursor-pointer">
                                    Hola, {{ user.displayName || user.email }}
                                </span>
                            </router-link>

                            <button @click="abrirModalLogout" class="logout-btn">
                                <i class="fa-solid fa-arrow-right-from-bracket me-2"></i> Cerrar sesión
                            </button>


                        </template>
                        <template v-else>
                            <a href="/login-registro" class="login-btn text-decoration-none">
                                <i class="fa-solid fa-right-to-bracket me-2"></i> Iniciar Sesión
                            </a>
                            <a href="/login-registro" class="register-btn text-decoration-none">
                                <i class="fa-solid fa-user-plus me-2"></i> Registrate
                            </a>
                        </template>
                    </div>

                </div>
            </div>
        </div>
    </nav>

    <!-- Offcanvas Carrito -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasCarrito" aria-labelledby="offcanvasCarritoLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasCarritoLabel">Tu carrito</h5>
            <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>

        <div class="offcanvas-body d-flex flex-column gap-3">
            <ul v-if="productosCarrito.length" class="list-group mb-3">
                <li v-for="(producto, index) in productosCarrito" :key="index"
                    class="list-group-item d-flex align-items-center gap-2">
                    <img :src="producto.imagen" alt="imagen" style="width: 50px; height: 50px; object-fit: contain;" />
                    <div class="d-flex justify-content-between w-100 align-items-center">
                        <div>
                            <p class="mb-1">{{ producto.nombre }}</p>
                            <small class="text-muted">Color: {{ producto.color }}</small>
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            <span class="badge bg-primary rounded-pill">{{ producto.cantidad }}</span>
                            <button class="btn btn-sm btn-outline-danger" @click="eliminarProducto(index)">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </li>
            </ul>

            <div v-else class="text-center text-muted">Tu carrito está vacío.</div>

            <!-- Botones de acción -->
            <div v-if="productosCarrito.length" class="d-flex justify-content-between gap-2 mt-auto">
                <button class="btn btn-danger w-50" @click="vaciarCarrito">
                    <i class="fas fa-trash-alt me-1"></i> Vaciar carrito
                </button>
                <button class="btn btn-success w-50" @click="comprarAhora">
                    <i class="fas fa-shopping-cart me-1"></i> Comprar
                </button>
            </div>
        </div>
    </div>

    <ModalConfirmacion ref="modalConfirmacionLogout"
        :mensaje="'¿Estás seguro que querés cerrar sesión? Podés seguir navegando 😉'" colorBoton="btn-danger"
        @confirmar="cerrarSesion" />



    <!-- Modal para eliminar cantidad -->
    <div class="modal fade" id="modalEliminarCantidad" tabindex="-1" aria-labelledby="modalEliminarCantidadLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content rounded-4 shadow-sm border-0">
                <div class="modal-header bg-light border-bottom-0 rounded-top-4">
                    <h5 class="modal-title fw-semibold" id="modalEliminarCantidadLabel">¿Cuántas unidades querés
                        eliminar?
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body">
                    <p class="mb-3">Tenés <strong>{{ productoSeleccionado?.cantidad }}</strong> unidades en el carrito.
                    </p>
                    <input type="number" class="form-control" v-model.number="cantidadAEliminar"
                        :max="productoSeleccionado?.cantidad" min="1" />
                </div>
                <div class="modal-footer border-top-0 bg-light rounded-bottom-4">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-danger" @click="confirmarEliminarCantidad">Eliminar</button>
                </div>
            </div>
        </div>
    </div>



</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from "vue";
import { onAuthStateChanged, signOut } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";
import { auth, db } from "../firebase";
import { useRouter } from "vue-router";
import ModalConfirmacion from '../components/Modals/ModalConfirmacion.vue'

const user = ref(null);
const router = useRouter();
const isOpen = ref(false);
const searchText = ref("");
const isAdmin = ref(false);
const searchInput = ref(null);

const productoSeleccionado = ref(null);
const productoSeleccionadoIndex = ref(null);
const cantidadAEliminar = ref(1);
const modalConfirmacionLogout = ref(null)
const userRol = ref(null)


const toggleSearch = () => {
    isOpen.value = true;
};

const handleBlur = () => {

    setTimeout(() => {
        if (!searchText.value.trim()) {
            isOpen.value = false;
        }
    }, 150);
};


const handleClickOutside = (event) => {
    if (!searchText.value.trim() && !event.target.closest(".search-box")) {
        isOpen.value = false;
    }
};

const logout = async () => {
    await signOut(auth);
    user.value = null;
    router.push("/login-registro");
};

onMounted(() => {
    onAuthStateChanged(auth, async (u) => {
        if (u) {
            await u.reload();
            user.value = auth.currentUser;

            // 🔥 Traer rol desde Firestore
            const docRef = doc(db, "usuarios", user.value.uid);
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                userRol.value = docSnap.data().rol?.toLowerCase() || 'usuario';
            } else {
                userRol.value = 'usuario';
            }
        } else {
            user.value = null;
            userRol.value = null;
        }
    });


    document.addEventListener("click", handleClickOutside);

    // ✅ Esto arregla el problema del input oculto
    nextTick(() => {
        searchText.value = '';
    });
});


onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside);
});

const confirmLogout = async () => {
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmLogoutModal'));
    modal.hide(); // 👈 Esto lo cierra

    await signOut(auth);
    user.value = null;
    router.push("/login-registro");
};

const cantidadCarrito = ref(0);
const productosCarrito = ref([]);

function actualizarCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    productosCarrito.value = carrito;
    cantidadCarrito.value = carrito.reduce((total, producto) => total + producto.cantidad, 0);
}

onMounted(() => {
    actualizarCarrito();
    window.addEventListener('storage', actualizarCarrito); // Escucha cambios si en otra pestaña cambia
});

onUnmounted(() => {
    window.removeEventListener('storage', actualizarCarrito);
});

function eliminarProducto(index) {
    const producto = productosCarrito.value[index];

    if (producto.cantidad <= 2) {
        // Restar de a 1 si tiene 2 o menos
        producto.cantidad--;

        if (producto.cantidad <= 0) {
            productosCarrito.value.splice(index, 1);
        }

        localStorage.setItem('carrito', JSON.stringify(productosCarrito.value));
        actualizarCarrito();
    } else {
        // Más de 2: mostrar modal
        productoSeleccionado.value = producto;
        productoSeleccionadoIndex.value = index;
        cantidadAEliminar.value = 1;

        const modal = new bootstrap.Modal(document.getElementById('modalEliminarCantidad'));
        modal.show();
    }
}

const abrirBuscador = () => {
    isOpen.value = true;

    // Esperá un tick para que el input esté visible, luego enfocalo
    nextTick(() => {
        searchInput.value?.focus();
    });
};

const buscarProductos = () => {
    if (searchText.value.trim()) {
        console.log("🕵️ Buscando producto:", searchText.value);
        router.push({ path: '/productos', query: { buscar: searchText.value.trim() } });
        isOpen.value = false;
    } else {
        console.log("⚠️ Nada para buscar");
    }
};

function abrirModalLogout() {
    modalConfirmacionLogout.value?.abrir()
}

async function cerrarSesion() {
    try {
        await signOut(auth)
        user.value = null
        router.push("/login-registro")
    } catch (error) {
        console.error("❌ Error al cerrar sesión:", error)
    }
}







function confirmarEliminarCantidad() {
    const producto = productoSeleccionado.value;
    const index = productoSeleccionadoIndex.value;

    producto.cantidad -= cantidadAEliminar.value;

    if (producto.cantidad <= 0) {
        productosCarrito.value.splice(index, 1);
    }

    localStorage.setItem('carrito', JSON.stringify(productosCarrito.value));
    actualizarCarrito();

    const modal = bootstrap.Modal.getInstance(document.getElementById('modalEliminarCantidad'));
    modal.hide();
}





function vaciarCarrito() {
    productosCarrito.value = []
    localStorage.removeItem('carrito')
    actualizarCarrito()
}

function comprarAhora() {
    alert("¡Funcionalidad de compra en camino! 🚀"); // Acá podés redirigir a /checkout si querés
}




</script>

<style scoped>
/* Navbar */
.search-box {
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
    width: 40px;
    transition: width 0.5s ease;
    overflow: hidden;
}

.logo-navbar {
    height: 120px;
    width: auto;
    object-fit: contain;
    filter: brightness(0) invert(1);
    display: block;
    margin-top: -25px;
    margin-bottom: -25px;
}

.search-box input {
    border-radius: 20px;
    border: 1px solid transparent;
    padding: 5px 10px;
    width: 0;
    opacity: 0;
    transition: width 0.5s ease, opacity 0.5s ease, border-color 0.5s ease, background-color 0.5s ease;
}

.search-box.open {
    width: 250px;
}

.search-box.open input {
    width: 200px;
    opacity: 1;
    border-color: #ccc;
    background-color: white !important;
    color: black !important;
}

.search-box button i {
    font-size: 1.2rem;
    color: white;
    transition: color 0.3s;
}

.search-box.open button i {
    color: var(--colorTerciario);
}

.navbar-nav .nav-link {
    color: white !important;
    position: relative;
    transition: color 0.3s ease;
}

.navbar-nav .nav-link:hover,
.navbar-nav .nav-link.active {
    color: var(--colorTerciario) !important;
}

.navbar-nav .nav-link.active::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--colorTerciario);
}

.navbar-brand {
    padding-top: 0;
    padding-bottom: 0;
    display: flex;
    align-items: center;
}


/* Login y registro */
.auth-buttons a {
    padding: 10px 20px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    border: 2px solid var(--colorTerciario);
}

/* Botón login */
.login-btn {
    background-color: transparent;
    color: white;
    border-color: white;
}


.login-btn:hover {
    background-color: transparent;
    color: white;
    border-color: white;
}

/* Botón registro */
.register-btn {
    background-color: var(--colorTerciario);
    color: white;
}

.register-btn:hover {
    background-color: transparent;
    color: white;
    border-color: white;
}

.logout-btn {
    background-color: var(--colorTerciario);
    color: var(--colorFondoSecundario);
    padding: 10px 20px;
    border-radius: 30px;
    font-weight: 600;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    white-space: nowrap;
    /* 🔒 Evita que se corte */
    min-width: 180px;
    /* 🧱 Asegura el ancho mínimo */
}

.logout-btn i {
    font-size: 1rem;
    margin-right: 6px;
}

.logout-btn:hover {
    background-color: transparent;
    color: white;
    border-color: white;
}


/* Carrito */
.cart-badge {
    position: absolute;
    top: -6px;
    right: 5px;
    font-size: 0.7rem;
    padding: 2px 6px;
}

.cart-btn {
    width: 40px;
    height: 33px;
    background-color: transparent;
    color: white;
    border-radius: 50%;
    font-size: 1.2rem;
    transition: color 0.3s ease;
}

.cart-btn:hover {
    color: var(--colorTerciario);
}

.badge {
    font-size: 0.7rem;
}

.router-link-active {
    color: var(--colorTerciario) !important;
}

.router-link-active::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--colorTerciario);
}

.btn-outline-danger i,
.btn-success i {
    font-size: 0.9rem;
}

.logout-btn {
    background-color: var(--colorTerciario);
    border: none;
    color: #000;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-weight: bold;
    font-size: 0.95rem;
    transition: all 0.2s ease-in-out;
}

.logout-btn:hover {
    background-color: var(--colorTerciarioHover);
    color: white;
}




@media (max-width: 1199px) {
    .logo-navbar {
        transform: scale(1);
        transform-origin: left center;
        margin-right: 160px;
        /* 🪄 Empuja el texto a la derecha */
    }

    .offcanvas-body {
        flex-wrap: nowrap !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 0 !important;
    }

    .auth-buttons {
        flex-direction: row !important;
        flex-wrap: nowrap;
        gap: 0.5rem;
    }

    .search-box input {
        width: 120px !important;
    }

    .search-box.open {
        width: 160px;
    }

    .logo-navbar {
        max-height: 80px;
        margin-right: 80px;
        margin-top: -10px;
        margin-bottom: -10px;
    }

    .logout-btn {
        font-size: 0.8rem;
        padding: 6px 10px;
        min-width: auto;
    }

    .cart-btn {
        width: 30px;
        height: 30px;
        font-size: 1rem;
    }
}


/* Responsive */
@media (max-width: 991px) {
    .offcanvas-header {
        background-color: #212529;
    }

    .offcanvas-body {
        background-color: #343a40;
        color: white;
    }

    .navbar-toggler-icon {
        color: white;
    }

    .auth-buttons {
        flex-direction: column !important;
        gap: 1rem;
    }
}
</style>

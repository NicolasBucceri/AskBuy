<template>
    <div class="contenedorGeneral">
        <div class="contenedor" ref="contenedor">
            <div class="contenedorIniciarSeccionRegistro">
                <LoginForm />
                <RegisterForm />
            </div>

            <div class="contenedorPaneles">
                <div class="panel panelIzquierdo">
                    <div class="contenido">
                        <h3>¿Ya sos parte de nuestra comunidad?</h3>
                        <p>Iniciá sesión para seguir disfrutando de nuestros servicios y novedades exclusivas.</p>
                        <button class="btnEnviar btnPanel" id="btnIniciarSeccion">Iniciar sesión</button>
                    </div>
                    <img src="../../../public/Img/registro.svg" alt="" class="imagen" />
                </div>

                <div class="panel panelDerecho">
                    <div class="contenido">
                        <h3>¿Sos nuevo por acá?</h3>
                        <p>Registrate gratis y comenzá a disfrutar de todos nuestros beneficios como usuario.</p>
                        <button class="btnEnviar btnPanel" id="btnRegistrarse">Registrarse</button>
                    </div>
                    <img src="../../../public/Img/login.svg" alt="" class="imagen" />
                </div>
            </div>
        </div>

    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'

const contenedor = ref(null)

onMounted(() => {
  const btnIniciarSeccion = document.querySelector('#btnIniciarSeccion')
  const btnRegistrarse = document.querySelector('#btnRegistrarse')
  const btnIniciarSeccion2 = document.querySelector('#btnIniciarSeccion2')
  const btnRegistrarse2 = document.querySelector('#btnRegistrarse2')

  btnIniciarSeccion?.addEventListener('click', () => {
    contenedor.value.classList.remove('modoRegistro')
  })

  btnRegistrarse?.addEventListener('click', () => {
    contenedor.value.classList.add('modoRegistro')
  })

  btnIniciarSeccion2?.addEventListener('click', (e) => {
    e.preventDefault()
    contenedor.value.classList.remove('modoRegistro')
  })

  btnRegistrarse2?.addEventListener('click', (e) => {
    e.preventDefault()
    contenedor.value.classList.add('modoRegistro')
  })
})
</script>




<style >
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

.contenedorGeneral {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: var(--colorFondoSecundario);
}

.contenedor {
    position: relative;
    width: 100vw;
    height: 100vh;
    background: var(--colorFondoPrincipal);
    border-radius: 15px;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3), 0 6px 20px 0 rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.contenedor::before {
    content: "";
    position: absolute;
    top: 0;
    left: -50%;
    width: 100%;
    height: 100%;
    background: linear-gradient(220.55deg, #3793FF 0%, #0017E4 100%);
    z-index: 6;
    transform: translateX(100%);
    transition: 1s ease-in-out;
}

.contenedorIniciarSeccionRegistro {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
    z-index: 5;
}

form {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    width: 40%;
    min-width: 238px;
    padding: 0 10px;
}

form.formularioIniciarSeccion {
    opacity: 1;
    transition: 0.5s ease-in-out;
    transition-delay: 1s;
}

form.formularioRegistro {
    opacity: 0;
    transition: 0.5s ease-in-out;
    transition-delay: 1s;
}

.tituloPrincipal {
    font-size: 35px;
    color: var(--colorPrincipal);
    margin-bottom: 10px;
}

.campoEntrada {
    width: 100%;
    height: 50px;
    background: #f0f0f0;
    margin: 10px 0;
    border: 2px solid var(--colorPrincipal);
    border-radius: 50px;
    display: flex;
    align-items: center;
}

.campoEntrada i {
    flex: 1;
    text-align: center;
    color: #666;
    font-size: 18px;
}

.campoEntrada input {
    flex: 5;
    background: none;
    border: none;
    outline: none;
    width: 100%;
    font-size: 18px;
    font-weight: 600;
    color: var(--colorTextoPrincipal);
}

.btnEnviar {
    width: 150px;
    height: 50px;
    border: 2px solid var(--colorTextoSecundario);
    background: var(--colorTextoSecundario); 
    color: var(--colorPrincipal);
    border-radius: 50px;
    font-weight: 600;
    margin: 10px 0;
    text-transform: uppercase;
    cursor: pointer;
    transition: 0.3s;
}

.btnEnviar:hover {
  background: var(--colorTextoSecundario);
  color: var(--colorPrincipal);
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}



.btnPanel:hover {
  background: white;
  color: var(--colorPrincipal);
  border-color: white;
}

.btnForm {
  width: 100%;
  max-width: 180px;
  height: 50px;
  background: transparent;
  color: var(--colorFondoSecundario);
  font-weight: 600;
  font-size: 1rem;
  border: 2px solid var(--colorFondoSecundario);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  margin-top: 10px;
}

.btnForm:hover {
  border-color: var(--colorPrincipal);
  color: var(--colorPrincipal);
  transform: translateY(-2px);
}


.socialTexto {
    margin: 10px 0;
    font-size: 16px;
}

.socialMedia {
    display: flex;
    justify-content: center;
}

.socialIcon {
    height: 45px;
    width: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--colorTextoPrincipal);
    border-color: var(--colorTextoPrincipal);
    border-radius: 50px;
    margin: 0 5px;
    font-size: 20px;
}

a {
    text-decoration: none;
}

.socialIcon:hover {
    color: var(--colorPrincipal);
    border-color: var(--colorPrincipal);
}

.contenedorPaneles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    width: 35%;
    min-width: 238px;
    padding: 0 10px;
    text-align: center;
    z-index: 6;
}

.panelIzquierdo {
    pointer-events: none;
}

.contenido {
    color: var(--colorTextoSecundario);
    transition: 1.1s ease-in-out;
    transition-delay: 0.5s;
}

.panel h3 {
    font-size: 24px;
    font-weight: 600;
}

.panel p {
    font-size: 15px;
    padding: 10px 0;
}

.imagen {
    width: 100%;
    transition: 1.1s ease-in-out;
    transition-delay: 0.4s;
}

.panelIzquierdo .imagen,
.panelIzquierdo .contenido {
    transform: translateX(-200%);
}

.panelDerecho .imagen,
.panelDerecho .contenido {
    transform: translateX(0);
}

.textoCuenta {
    display: none;
}

/*Animaciones*/
.contenedor.modoRegistro::before {
    transform: translateX(0);
}

.contenedor.modoRegistro .panelDerecho .imagen,
.contenedor.modoRegistro .panelDerecho .contenido {
    transform: translateX(200%);
}

.contenedor.modoRegistro .panelIzquierdo .imagen,
.contenedor.modoRegistro .panelIzquierdo .contenido {
    transform: translateX(0);
}

.contenedor.modoRegistro form.formularioIniciarSeccion {
    opacity: 0;
}

.contenedor.modoRegistro form.formularioRegistro {
    opacity: 1;
}

.contenedor.modoRegistro .panelDerecho {
    pointer-events: none;
}

.contenedor.modoRegistro .panelIzquierdo {
    pointer-events: all;
}

/*Responsive*/
@media (max-width:779px) {
    .contenedor {
        width: 100vw;
        height: 100vh;
    }
}

@media (max-width:635px) {
    .contenedor::before {
        display: none;
    }

    form {
        width: 80%;
    }

    form.formularioRegistro {
        display: none;
    }

    .contenedor.sign-up-mode2 form.formularioRegistro {
        display: flex;
        opacity: 1;
    }

    .contenedor.sign-up-mode2 form.formularioIniciarSeccion {
        display: none;
    }

    .contenedorPaneles {
        display: none;
    }

    .textoCuenta {
        display: initial;
        margin-top: 30px;
    }
}

@media (max-width:320px) {
    form {
        width: 90%;
    }
}
</style>
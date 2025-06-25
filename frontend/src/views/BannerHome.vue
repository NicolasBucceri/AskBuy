<template>
<div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-inner">
    <!-- Primer slide - Auriculares -->
    <div class="carousel-item active">
      <section class="fondoAuriculares">
        <main class="mainContainer">
            <section class="containerAuriculares">
                <div class="logoBackground3"></div>
                <div class="leftSideAuriculares">
                    <h1>Logitech</h1> 
                    <span class="boldFontAuriculares">Auriculares Gaming</span>
                    <p>Auriculares inalámbricos con tecnología de sonido envolvente y ultra ligeros.</p>
                    <div class="buttonContainerAuriculares">
                        <div id="verauriculares" class="btnAuriculares">Ver auriculares</div>
                        <div id="todosProductos" class="btnAuriculares btnSecondaryAuriculares">Todos los productos</div>
                    </div>
                </div>
                <div class="rightSideAuriculares">
                    <img src="../../../public/Img/imgBanner.png" alt="Auriculares Logitech" loading="eager">
                </div>
            </section>
        </main>
      </section>
    </div>

    <!-- Segundo slide - Mouse -->
    <div class="carousel-item">
      <section class="fondoMouse">
        <main class="mainContainer">
            <section class="containerMouse">
                <div class="logoBackground2"></div>
                <div class="leftSideMouse">
                    <h1>Razer</h1> 
                    <span class="boldFontMouse">Mouse Gaming</span>
                    <p>Mouse ergonómico con sensor óptico de alta precisión.</p>
                    <div class="buttonContainerMouse">
                        <div id="vermouse" class="btnMouse">Ver mouse</div>
                        <div id="todosProductos" class="btnMouse btnSecondaryMouse">Todos los productos</div>
                    </div>
                </div>
                <div class="rightSideMouse">
                    <img src="../../../public/Img/imgBanner2.png" alt="Mouse Razer" loading="eager">
                </div>
            </section>
        </main>
      </section>
    </div>

    <!-- Tercer slide - Monitor -->
    <div class="carousel-item">
      <section class="fondoMonitor">
        <main class="mainContainer">
            <section class="containerMonitor">
                <div class="logoBackground"></div>
                <div class="leftSideMonitor">
                    <h1>Alienware</h1>
                    <span class="boldFontMonitor">Monitor Curved Gaming</span>
                    <p>Pantalla curva de 34'' con tecnología G-Sync para una experiencia inmersiva.</p>
                    <div class="buttonContainerMonitor">
                        <div id="verMonitores" class="btnMonitor">Ver monitores</div>
                        <div id="todosProductos" class="btnMonitor btnSecondaryMonitor">Todos los productos</div>
                    </div>
                </div>
                <div class="rightSideMonitor">
                    <img src="../../../public/Img/imgBanner3.png" alt="Monitor Alienware" loading="eager">
                </div>
            </section>
        </main>
      </section>
    </div>
  </div>

  <!-- Controles del carrusel -->
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

</template>





<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&display=swap');

/* Estilos Generales */
* {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
/* Carrusel */
.carousel-inner {
    display: flex;
    align-items: center;
}
.carousel-item {
    position: absolute;
    transform: translateY(0) !important;
    width: 100%;
    top: 0;
    left: 0;
    opacity: 0;
    transition: opacity 0.6s ease-in-out;
}
.carousel-item.active {
    position: relative;
    opacity: 1;
}
.carousel-control-next-icon{
    margin-left: 80px;
}
.carousel-control-prev-icon {
    margin-right: 80px;
}
/* Animacion */
@keyframes floatAnimation {
    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
}

/* --------------------- Seccion Auriculares --------------------------*/
.fondoAuriculares {
    background: linear-gradient(135deg, #1D1D1D, #009CDE);
}
.containerAuriculares {
    width: 85%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100vh;
}
.logoBackground3 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 400px;
    background: url('../../../public/Img/logoLogitech.png') no-repeat center;
    background-size: contain;
    opacity: 0.2;
}
.leftSideAuriculares {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.leftSideAuriculares h1 {
    font-size: 5.2rem;
    margin-top: 2rem;
    color: #00a7e0;
    font-family: 'Roboto', sans-serif;
    font-weight: 700;

}
.boldFontAuriculares {
    font-weight: bold;
    color: #FFFFFF;
}
.leftSideAuriculares p {
    margin-top: 10px;
    line-height: 1.5;
    color: #FFFFFF;
}
.buttonContainerAuriculares {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-top: 25px;
}
.btnAuriculares {
    padding: 14px 35px;
    background-color: #009CDE;
    border-radius: 50px;
    color: #ffffff;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: 0.3s ease-out;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}
.btnAuriculares:hover {
    background-color: transparent;
    color: #FFFFFF;
    border: 1px solid #009CDE;
}
.btnSecondaryAuriculares {
    background-color: transparent;
    color: #FFFFFF;
    border: 2px solid #009CDE;
}
.rightSideAuriculares {
    width: 50%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}
.rightSideAuriculares img {
    width: 100%;
    max-width: 745px;
    animation: floatAnimation 3s ease-in-out infinite;
    filter: drop-shadow(0px 10px 30px rgba(0, 0, 0, 0.2));
    transition: transform 0.3s ease-out;
}
/* ------------------------ Seccion Mouse -----------------------------*/
.fondoMouse {
    background: linear-gradient(135deg, #0a0a0a, #1a1a1a, #00FF00);
}

.containerMouse {
    width: 85%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100vh;
}

.logoBackground2 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 400px;
    background: url('../../../public/Img/logoRazer.png') no-repeat center;
    background-size: contain;
    opacity: 0.2;
}

.leftSideMouse {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.leftSideMouse h1 {
    font-size: 5.2rem;
    margin-top: 2rem;
    color: #00FF00;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;

}

.boldFontMouse {
    font-weight: bold;
    color: #FFFFFF;
}

.leftSideMouse p {
    margin-top: 10px;
    line-height: 1.5;
    color: #FFFFFF;
}

.buttonContainerMouse {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-top: 25px;
}

.btnMouse {
    padding: 14px 35px;
    background-color: #00FF00;
    border-radius: 50px;
    color: #000000;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: 0.3s ease-out;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.btnMouse:hover {
    background-color: transparent;
    color: #FFFFFF;
    border: 1px solid #00FF00;
}

.btnSecondaryMouse {
    background-color: transparent;
    color: #FFFFFF;
    border: 2px solid #00FF00;
}

.rightSideMouse {
    width: 50%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.rightSideMouse img {
    width: 100%;
    max-width: 745px;
    animation: floatAnimation 3s ease-in-out infinite;
    filter: drop-shadow(0px 10px 30px rgba(0, 0, 0, 0.2));
    transition: transform 0.3s ease-out;
}

/* ----------------------- Seccion Monitor ----------------------------*/
.fondoMonitor {
    background: linear-gradient(135deg, #0a0a0a, #1a1a1a, #00FF00);
}

.containerMonitor {
    width: 85%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100vh;
}

.logoBackground {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 400px;
    background: url('../../../public/Img/logoAlienware.png') no-repeat center;
    background-size: contain;
    opacity: 0.2;
}

.leftSideMonitor {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.leftSideMonitor h1 {
    font-size: 5.2rem;
    margin-top: 2rem;
    color: #00FF00;
    font-family: 'Orbitron', sans-serif;
    font-weight: 500;
}

.boldFontMonitor {
    font-weight: bold;
    color: #FFFFFF;
}

.leftSideMonitor p {
    margin-top: 10px;
    line-height: 1.5;
    color: #FFFFFF;
}

.buttonContainerMonitor {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-top: 25px;
}

.btnMonitor {
    padding: 14px 35px;
    background-color: #00FF00;
    border-radius: 50px;
    color: #000000;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: 0.3s ease-out;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.btnMonitor:hover {
    background-color: transparent;
    color: #FFFFFF;
    border: 1px solid #00FF00;
}

.btnSecondaryMonitor {
    background-color: transparent;
    color: #FFFFFF;
    border: 2px solid #00FF00;
}

.rightSideMonitor {
    width: 50%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.rightSideMonitor img {
    width: 100%;
    max-width: 745px;
    animation: floatAnimation 3s ease-in-out infinite;
    filter: drop-shadow(0px 10px 30px rgba(0, 0, 0, 0.2));
    transition: transform 0.3s ease-out;
}

/* Media Queries */
@media (max-width: 880px) {
    .leftSide {
        width: 90%;
    }

    .rightSide {
        width: 10%;
    }

    .rightSide img {
        width: 745px;
        position: relative;
        left: -20rem;
        z-index: -1;
    }
}

@media (max-width: 700px) {
    .leftSide h1 {
        font-size: 4.2rem;
    }
}

@media (max-width: 500px) {
    .leftSide h1 {
        font-size: 2.2rem;
    }

    .leftSide p {
        font-size: 12px;
    }

    #auriculares,
    #productos {
        padding: 8px 20px;
    }
}
</style>

<template>
    <section>
        <div class="contenedorSuperior">

            <div class="contenedorAuriculares">
                <div class="img-contenedor">
                    <img src="../../../public/Img/contenedorAuriculares.png" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorAuriculares">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Auriculares</h4>
                    <button class="btnAuriculares">Ver mas</button>
                </div>
            </div>

            <div class="contenedorRelojes">
                <div class="imgContenedorRelojes">
                    <img src="../../../public/Img/contenedorRelojes.png" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorRelojes">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Relojes</h4>
                    <button class="btnRelojes">Ver Más</button>
                </div>
            </div>

            <div class="contenedorLaptop">
                <div class="imgContenedorLaptop">
                    <img src="../../../public/Img/contenedorLaptops.png" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorLaptop">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Laptops</h4>
                    <button class="btnLaptop">Ver Más</button>
                </div>
            </div>
        </div>

        <div class="contenedorInferior">

            <div class="contenedorMonitor">
                <div class="imgContenedorMonitor">
                    <img src="../../../public/Img/contenedorMonitor.webp" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorMonitor">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Monitores</h4>
                    <button class="btnMonitor">Ver mas</button>
                </div>
            </div>

            <div class="contenedorMouse">
                <div class="imgContenedorMouse">
                    <img src="../../../public/Img/contenedorMouse.png" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorMouse">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Mouse</h4>
                    <button class="btnMouse">Ver Más</button>
                </div>
            </div>

            <div class="contenedorTeclados">
                <div class="imgContenedorTeclados">
                    <img src="../../../public/Img/contenedorTeclado.png" alt="Imagen de auricular">
                </div>
                <div class="textoContenedorTeclados">
                    <h2>Disfruta </h2>
                    <h3>Con</h3>
                    <h4>Teclados</h4>
                    <button class="btnTeclados">Ver Más</button>
                </div>
            </div>
        </div>
    </section>

</template>

<script>

</script>

<style scoped>
/*Etiquetas generales*/
section {
    margin: 5%;
}

img {
    width: 100%;
    max-width: 150px;
    height: auto;
    margin-top: 20px;
}

/* Clases */
.contenedorSuperior {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    gap: 20px;
}

.contenedorInferior {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    gap: 20px;
}

.contenedorAuriculares,
.contenedorRelojes {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.contenedorMouse,
.contenedorTeclados {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}
.contenedorAuriculares,
.contenedorRelojes,
.contenedorLaptop,
.contenedorMonitor,
.contenedorMouse,
.contenedorTeclados {
    transition: transform 0.5s ease-in-out;
}

.contenedorAuriculares:hover,
.contenedorRelojes:hover,
.contenedorLaptop:hover,
.contenedorMonitor:hover,
.contenedorMouse:hover,
.contenedorTeclados:hover {
    transform: scale(1.02);
}

/*----Contenedor Auliculares-----*/
.contenedorAuriculares {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: linear-gradient(220.55deg, #565656 0%, #181818 100%);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.textoContenedorAuriculares {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}

.textoContenedorAuriculares h2,
.textoContenedorAuriculares h3,
.textoContenedorAuriculares h4 {
    margin: 10px 0;
}

.textoContenedorAuriculares h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: var(--colorSecundario);
    letter-spacing: 1px;
}

.textoContenedorAuriculares h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
}

.textoContenedorAuriculares h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: var(--colorSecundario);
    margin: 0;
}

.textoContenedorAuriculares .btnAuriculares {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: #f42c38;
    color: white;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.textoContenedorAuriculares .btnAuriculares:hover {
    background-color: #e65c00;
    transform: scale(1.05);
}

.img-contenedor {
    position: absolute;
    top: 20%;
    left: 30%;
    /* Ajusté un poco más a la derecha */
    right: 0;
    bottom: 0;
    z-index: 1;
    opacity: 0.3;
}

.img-contenedor img {
    width: 120%;
    max-width: 300%;
    /* Lo hice un poco más grande */
    height: 100%;
    object-fit: cover;
}

/*----Contenedor Relojes-----*/
.contenedorRelojes {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background:  linear-gradient(220.55deg, #FF896D 0%, #D02020 100%);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.textoContenedorRelojes {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}

.textoContenedorRelojes h2,
.textoContenedorRelojes h3,
.textoContenedorRelojes h4 {
    margin: 10px 0;
}

.textoContenedorRelojes h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
}

.textoContenedorRelojes h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #8d8d8d;
}

.textoContenedorRelojes h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: #ffffff;
    margin: 0;
}

.textoContenedorRelojes .btnRelojes {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: white;
    color: #D02020;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.textoContenedorRelojes .btnRelojes:hover {
    background-color: white;
    transform: scale(1.05);
}

.imgContenedorRelojes {
    position: absolute;
    display: flex;
    justify-content: center;
    text-align: center;
    top: -5%;
    left: 0%;
    right: 0;
    bottom: 0;
    z-index: 1;
}

.imgContenedorRelojes img {
    width: 70%;
    max-width: 150%;
    height: auto;
    object-fit: contain;
}

/*----Contenedor Laptop-----*/
.contenedorLaptop {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: linear-gradient(220.55deg, #FFF500 0%, #FFB800 100%);
    flex: 2;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.textoContenedorLaptop {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}

.textoContenedorLaptop h2,
.textoContenedorLaptop h3,
.textoContenedorLaptop h4 {
    margin: 10px 0;
}

.textoContenedorLaptop h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
}

.textoContenedorLaptop h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #8d8d8d;
}

.textoContenedorLaptop h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: #ffffff;
}

.textoContenedorLaptop .btnLaptop {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: white;
    color: #FFB800;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.textoContenedorLaptop .btnLaptop:hover {
    background-color: white;
    transform: scale(1.05);
}

.imgContenedorLaptop {
    position: absolute;
    display: flex;
    justify-content: center;
    text-align: center;
    top: 0%;
    left: 40%;
    right: 0;
    bottom: 0;
    z-index: 1;
}

.imgContenedorLaptop img {
    width: 100%;
    max-width: 100%;
    height: auto;
    object-fit: contain;
}


/*----Contenedor Monitor-----*/
.contenedorMonitor {
    display: flex;
    flex: 2;
    justify-content: center;
    align-items: center;
    position: relative;
    background: linear-gradient(220.55deg, #EAEAEA 0%, #8B8B8B 100%);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}
.textoContenedorMonitor {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}
.textoContenedorMonitor h2,
.textoContenedorMonitor h3,
.textoContenedorMonitor h4 {
    margin: 10px 0;
}
.textoContenedorMonitor h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: var(--colorSecundario);
    letter-spacing: 1px;
}
.textoContenedorMonitor h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
}
.textoContenedorMonitor h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: var(--colorSecundario);
    margin: 0;
}
.textoContenedorMonitor .btnMonitor {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: #f42c38;
    color: white;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.textoContenedorMonitor .btnMonitor:hover {
    background-color: #f42c38;
    transform: scale(1.05);
}
.imgContenedorMonitor {
    position: absolute;
    top: 0;
    left: 40%;
    right: 0;
    bottom: 0;
    z-index: 1;
}
.imgContenedorMonitor img {
    width: 120%;
    max-width: 400%;
    height: 100%;
    object-fit: cover;
}

/*----Contenedor Mouse-----*/
.contenedorMouse {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: linear-gradient(220.55deg, #4643DF 0%, #0B0A47 100%);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}
.textoContenedorMouse {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}
.textoContenedorMouse h2,
.textoContenedorMouse h3,
.textoContenedorMouse h4 {
    margin: 10px 0;
}
.textoContenedorMouse h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 1px;
}
.textoContenedorMouse h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #8d8d8d;
}
.textoContenedorMouse h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: #FFFFFF;
    margin: 0;
}
.textoContenedorMouse .btnMouse {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: white;
    color: #4643DF;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.textoContenedorMouse .btnMouse:hover {
    background-color: white;
    transform: scale(1.05);
}
.imgContenedorMouse {
    position: absolute;
    display: flex;
    justify-content: center;
    text-align: center;
    top: 25%;
    left: 60%;
    right: 0;
    bottom: 0;
    z-index: 1;
}
.imgContenedorMouse img {
    width: 280%;
    max-width: 400%;
    height: 100%;
    object-fit: contain;
}

/*----Contenedor Teclados-----*/
.contenedorTeclados {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: linear-gradient(220.55deg, #61C695 0%, #133114 100%);
    flex: 2;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}
.textoContenedorTeclados {
    color: white;
    text-align: left;
    flex: 1;
    padding-right: 20px;
    position: relative;
    z-index: 2;
}
.textoContenedorTeclados h2,
.textoContenedorTeclados h3,
.textoContenedorTeclados h4 {
    margin: 10px 0;
}
.textoContenedorTeclados h2 {
    font-family: var(--fuentePrincipal);
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
}
.textoContenedorTeclados h3 {
    font-family: var(--fuentePrincipal);
    font-size: 22px;
    font-weight: 700;
    color: #8d8d8d;
}
.textoContenedorTeclados h4 {
    font-family: var(--fuentePrincipal);
    font-size: 48px;
    font-weight: 900;
    color: #ffffff;
}
.textoContenedorTeclados .btnTeclados {
    margin-top: 20px;
    padding: 12px 24px;
    background-color: white;
    color: #133114;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.textoContenedorTeclados .btnTeclados:hover {
    background-color: white;
    transform: scale(1.05);
}
.imgContenedorTeclados {
    position: absolute;
    display: flex;
    justify-content: center;
    text-align: center;
    top: 0%;
    left: 40%;
    right: 0;
    bottom: 0;
    z-index: 1;
}
.imgContenedorTeclados img {
    width: 100%;
    max-width: 100%;
    height: auto;
    object-fit: contain;
}
</style>
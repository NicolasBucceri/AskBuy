<template>
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="footerColumna">
                    <h4>Compañía</h4>
                    <ul>
                        <li><a href="#">Quienes somos</a></li>
                        <li><a href="#">Servicios</a></li>
                        <li><a href="#">Políticas y privacidad</a></li>
                    </ul>
                </div>
                <div class="footerColumna">
                    <h4>Ayuda</h4>
                    <ul>
                        <li><a href="#">Contáctanos</a></li>
                        <li><a href="#">Métodos de pago</a></li>
                        <li><a href="#">Mantenimiento 24hs</a></li>
                    </ul>
                </div>
                <div class="footerColumna">
                    <h4>Tienda</h4>
                    <ul>
                        <li><a href="#">Auriculares</a></li>
                        <li><a href="#">Laptops</a></li>
                        <li><a href="#">Monitores</a></li>
                        <li><a href="#">Mouses</a></li>
                        <li><a href="#">Teclados</a></li>
                        <li><a href="#">Relojes</a></li>
                    </ul>
                </div>
                <div class="footerColumna">
                    <h4>Seguinos</h4>
                    <div class="socialLinks">
                        <a href="https://www.instagram.com/nicolas_bucceri/?hl=es-la" aria-label="Instagram">
                            <i class="fa-brands fa-instagram"></i>
                        </a>
                        <a href="https://github.com/NicolasBucceri" aria-label="GitHub">
                            <i class="fa-brands fa-github"></i>
                        </a>
                        <a href="https://www.linkedin.com/in/nicolas-bucceri-715972244/" aria-label="LinkedIn">
                            <i class="fa-brands fa-linkedin"></i>
                        </a>
                        <a href="https://nicolasbucceri.netlify.app/" aria-label="Portafolio">
                            <i class="fa-solid fa-globe"></i>
                        </a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                © 2025 Nicolas Bucceri. Todos los derechos reservados.
            </div>
        </div>
    </footer>
</template>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    line-height: 1.5;
}

a {
    cursor: pointer;
}

ul {
    list-style: none;
}

.container {
    max-width: 1170px;
    margin: auto;
}

.row {
    display: flex;
    flex-wrap: wrap;
}

.footer {
    background-color: var(--colorFondoSecundario);
    padding: 70px 0;
}

.footerColumna {
    width: 25%;
    padding: 0 15px;
}

.footerColumna h4 {
    font-size: 18px;
    color: var(--colorTerciario);
    text-transform: capitalize;
    margin-bottom: 30px;
    font-weight: 500;
    position: relative;
}

.footerColumna h4::before {
    content: '';
    position: absolute;
    left: 0;
    bottom: -10px;
    background-color: var(--colorError);
    height: 2px;
    width: 50px;
}

.footerColumna ul li:not(:last-child) {
    margin-bottom: 10px;
}

.footerColumna ul li a {
    font-size: 16px;
    text-transform: capitalize;
    color: #ddd;
    text-decoration: none;
    font-weight: 300;
    display: block;
    transition: all 0.3s ease;
}

.footerColumna ul li a:hover {
    color: var(--colorTextoSecundario);
    padding-left: 8px;
}

.footerColumna .socialLinks {
    display: flex;
    flex-wrap: wrap;
}

.footerColumna .socialLinks a {
    display: inline-block;
    height: 40px;
    width: 40px;
    background-color: rgba(255, 255, 255, 0.2);
    margin: 0 10px 10px 0;
    text-align: center;
    line-height: 40px;
    border-radius: 50%;
    color: var(--colorTextoSecundario);
    transition: all 0.3s ease;
}

.footerColumna .socialLinks a:hover {
    color: var(--colorFondoSecundario);
    background-color: var(--colorTextoSecundario);
    transform: scale(1.1);
}

.footer-bottom {
    text-align: center;
    color: #888;
    padding-top: 30px;
    font-size: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 40px;
}

@media(max-width: 767px) {
    .footerColumna {
        width: 50%;
        margin-bottom: 30px;
    }
}

@media(max-width: 574px) {
  .footerColumna {
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
  }

  .footerColumna .socialLinks {
    justify-content: center;
  }

  .footerColumna h4::before {
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
  }
}

</style>
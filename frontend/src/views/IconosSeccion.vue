<template>
    <section class="quality-sections p-6">
      <div class="grillaContenedorIconos">
        <!-- Sección 1 -->
        <div class="iconoItem">
          <div class="icono iconoVerde">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="iconoContenedor">
            <h3 class="iconoTitulo">Calidad Asegurada</h3>
            <p class="iconoDescripcion">Productos certificados con garantía del fabricante.</p>
          </div>
        </div>
  
        <!-- Sección 2 -->
        <div class="iconoItem">
          <div class="icono iconoAzul">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="iconoContenedor">
            <h3 class="iconoTitulo">Protección Garantizada</h3>
            <p class="iconoDescripcion">Compra segura con políticas de devolución y soporte confiable.</p>
          </div>
        </div>
  
        <!-- Sección 3 -->
        <div class="iconoItem">
          <div class="icono iconoAmarillo">
            <i class="fas fa-star"></i>
          </div>
          <div class="iconoContenedor">
            <h3 class="iconoTitulo">Compra en Tienda</h3>
            <p class="iconoDescripcion">Visítanos y disfruta de una experiencia de compra personalizada y directa.</p>
          </div>
        </div>
  
        <!-- Sección 4 -->
        <div class="iconoItem">
          <div class="icono iconoRojo">
            <i class="fas fa-clipboard-check"></i>
          </div>
          <div class="iconoContenedor">
            <h3 class="iconoTitulo">Soporte Continuo</h3>
            <p class="iconoDescripcion">Recibe asistencia personalizada antes, durante y después de tu compra.</p>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: "QualitySection",
  };
  </script>
  
  <style scoped>
  /* Clases */

  .grillaContenedorIconos {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1.5rem;
  }
  .iconoItem {
    display: flex;
    align-items: center;
    padding: 1.5rem;
    border-radius: 8px;
  }
  .icono {
    font-size: 3rem;
    margin-right: 1rem;
    margin-bottom: 1.5rem;
  }
  .iconoVerde {
    color: #28a745;
  }
  .iconoAzul {
    color: #007bff;
  }
  .iconoAmarillo {
    color: #ffc107;
  }
  .iconoRojo {
    color: #dc3545;
  }
  .iconoContenedor {
    display: flex;
    flex-direction: column;
  }
  .iconoTitulo {
    font-weight: 600;
    font-size: 1.2rem;
    color: #3A3A3A;
  }
  .iconoDescripcion {
    font-size: 0.8rem;
    color: #6c757d;
  }

  /* Medias */
  @media (min-width: 640px) {
    .grillaContenedorIconos {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (min-width: 1024px) {
    .grillaContenedorIconos {
      grid-template-columns: repeat(4, 1fr);
    }
  }
  

  

  

  

  

  

  

  </style>
  
<template>
    <section class="servicioExpress">
      <div class="contenedorServicio">
        <i class="fas fa-tools iconoServicio"></i>
        <div>
          <h3>Servicio técnico express</h3>
          <p>Reparamos o reemplazamos tu producto en menos de 24 horas. Garantía directa y sin vueltas.</p>
          <a href="#servicio" class="botonServicio">Ver Servicio Técnico</a>
        </div>
      </div>
    </section>
  </template>
  
  <style scoped>
  .servicioExpress {
    background-color: #f9fafb;
    padding: 40px 20px;
    text-align: center;
    border-top: 1px solid #e5e7eb;
  }
  
  .contenedorServicio {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .iconoServicio {
    font-size: 3rem;
    color: var(--main-color, #2563eb);
  }
  
  .servicioExpress h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
  }
  
  .servicioExpress p {
    font-size: 1rem;
    color: #4b5563;
  }
  .botonServicio {
  display: inline-block;
  background-color: #2563eb;
  color: white;
  padding: 12px 24px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.botonServicio:hover {
  background-color: #1e3a8a;
}

  </style>
  
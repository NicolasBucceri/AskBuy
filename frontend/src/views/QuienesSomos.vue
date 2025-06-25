<template>
    <section class="quienes-somos py-16 px-6 md:px-20">
      <!-- Sección principal -->
      <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-10 items-center">
        <img
          src="../../../public/Img/equipoAskBuy.jpg"
          alt="Equipo AskBuy"
          class="imagen rounded-2xl shadow-lg"
        />
  
        <div class="texto space-y-6">
          <h2 class="titulo text-4xl font-bold">¿Quiénes somos?</h2>
          <p class="descripcion text-lg leading-relaxed">
            En <strong>AskBuy</strong> nos apasiona la tecnología. Somos un equipo joven que busca ofrecerte lo mejor en accesorios y periféricos gaming. 
            Combinamos diseño, rendimiento y atención personalizada para que tu experiencia de compra sea rápida, confiable y clara.
          </p>
          <p class="text-md text-[var(--colorSecundario)] italic">
            Tu mundo gamer, más cerca.
          </p>
        </div>
      </div>
  
      <!-- Separador visual -->
      <div class="flex items-center justify-center mt-16 mb-10 gap-4 valores">
        <div class="w-20 h-[2px] bg-[var(--colorPrincipal)] animate-pulse"></div>
        <span class="text-[var(--colorPrincipal)] font-semibold tracking-wider uppercase text-sm ">
          Nuestros Valores
        </span>
        <div class="w-20 h-[2px] bg-[var(--colorPrincipal)] animate-pulse"></div>
      </div>
  
      <!-- Sección de visión -->
      <div class="vision grid md:grid-cols-3 gap-8 text-center">
        <div class="card p-6 rounded-2xl shadow-md">
          <div class="icono-wrapper flex justify-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="icono" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5s8.268 2.943 9.542 7c-1.274 4.057-5.065 7-9.542 7s-8.268-2.943-9.542-7z" />
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-[var(--colorPrincipal)] mb-3">Nuestra Visión</h3>
          <p class="textoValores">Queremos que tu compra sea simple, rápida y segura. Confianza en cada paso.</p>
        </div>
  
        <div class="card p-6 rounded-2xl shadow-md">
          <div class="icono-wrapper flex justify-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="icono" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9.75 3v1.5M14.25 3v1.5M3 7.5h18M3.75 7.5v11.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V7.5" />
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-[var(--colorPrincipal)] mb-3">¿Qué nos diferencia?</h3>
          <p class="textoValores">Soporte técnico 24hs y una experiencia diseñada para encontrar todo sin perder tiempo.</p>
        </div>
  
        <div class="card p-6 rounded-2xl shadow-md">
          <div class="icono-wrapper flex justify-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="icono" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 8h10M7 16h10M5 12h14" />
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-[var(--colorPrincipal)] mb-3">Compromiso con vos</h3>
          <p class="textoValores">Somos un equipo real que te escucha y conoce tus necesidades como gamer o techlover.</p>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  // Todo visual 😎
  </script>
  
  <style scoped>
  .quienes-somos {
    background-color: var(--colorFondoPrincipal);
    color: var(--colorTextoPrincipal);
    font-family: var(--fuentePrincipal);
    margin-top: 30px;
  }
  
  .titulo {
    color: var(--colorPrincipal);
    font-family: var(--fuenteTerciario);
    transition: transform 0.3s ease;
  }
  
  .titulo:hover {
    transform: scale(1.05);
    color: var(--colorPrincipalHover);
  }
  
  .imagen {
    animation: fadeIn 1.2s ease forwards;
    opacity: 0;
  }
  
  .texto {
    animation: slideUp 1.2s ease forwards;
    opacity: 0;
  }

  .textoValores {
    margin: 10px;
    padding-bottom: 10px;
  }

  .valores {
    margin-top: 30px;
  }
  
  .vision .card {
    background-color: var(--colorFondoSecundario);
    color: var(--colorTextoSecundario);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: popUp 1s ease forwards;
    opacity: 0;
    margin: 20px;
  }
  
  .vision .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  /* Icono dentro de la card */
  .icono {
    margin-top: 20px;
    height: 2rem;
    width: 2rem;
    stroke: var(--colorTerciario);
    transition: stroke 0.3s ease;
  }
  
  .card:hover .icono {
    stroke: var(--colorTerciarioHover);
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes popUp {
    from {
      transform: scale(0.95);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }
  </style>
  
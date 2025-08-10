<template>
  <div class="about-container">
    
    <!-- Main content -->
    <main class="main-content">
      <div class="hero-section">
        <!-- Contenedor para el texto superpuesto -->
        <div class="hero-content-wrapper">
          <h1 class="hero-title">
            NAVEGA TU<br>
            UNIVERSIDAD EN 360°
          </h1>
          
          <p class="hero-subtitle">
            Encuentra salones, rutas y más con la primera app de<br>
            mapas interactivos de la UNET
          </p>
        </div>
        
        <UButton 
          type="contrast" 
          text="Probar ahora"
          @click="navigateToMap"
          class="hero-button"
        />
      </div>
      
      <!-- Features section -->
      <section class="features-section">
        <p class="features-intro">
          ¿Cansado de perderte en el campus? Los mapas estáticos no ayudan, y preguntar a cada rato tampoco es la solución.
        </p>
        
        <p class="features-title">
          Mapa tradicional vs. UNET360
        </p>
        
        <div class="features-grid">
          <UCard 
            text="Fotos 360°: 'Explora los edificios como si estuvieras ahí'"
            icon="icons/camera"
            class="feature-card"
          />
          <UCard 
            text="Rutas inteligentes: 'De punto A a B con instrucciones visuales'"
            icon="icons/route-arrow"
            class="feature-card"
          />
          <UCard 
            text="Buscador: 'Encuentra cualquier salón en segundos'"
            icon="icons/search"
            class="feature-card"
          />
        </div>
      </section>
      
      <!-- Credits section -->
      <section class="credits-section">
        <p class="credits-text">
          Creado por estudiantes UNETENSES
        </p>
        
        <p class="credits-description">
          Somos estudiantes de Informática. Desarrollamos esta app para hacer la vida universitaria más fácil.
        </p>
      </section>
    </main>
    
    <!-- Sidebar -->
    <USidebar :isOpen="isPanelOpen" @close="closePanel">
      <router-link to="/" class="nav-item">Inicio</router-link>
      <router-link to="/360-map" class="nav-item">Mapa 360°</router-link>
      <router-link to="/about" class="nav-item">Acerca de</router-link>
      <button class="nav-item" @click="handleLogout">Cerrar sesión</button>
    </USidebar>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/service/stores/auth'
import UButton from '@/components/UButton.vue'
import UCard from '@/components/UCard.vue'
import USidebar from '@/components/USidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const isPanelOpen = ref(false)

const togglePanel = () => {
  isPanelOpen.value = !isPanelOpen.value
}

const closePanel = () => {
  isPanelOpen.value = false
}

const navigateToMap = () => {
  router.push({ name: 'Map' })
}

const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'Login' })
  closePanel()
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

.about-container {
  min-height: 100vh;
  background: var(--strong-gray);
  position: relative;
  padding-top: 1rem;
}

.main-content {
  padding: 0 1.125rem;
}

.hero-section {
  position: relative; /* Necesario para posicionar el contenido superpuesto */
  text-align: center;
  padding: 4rem 1rem; /* Aumentamos el padding para dar espacio a la imagen de fondo */
  border-radius: 12px;
  overflow: hidden; /* Asegura que la superposición no se salga del contenedor */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/images/about-image.png');
    background-size: cover;
    background-position: center;
    filter: blur(2px) brightness(0.6); /* Desenfoque y oscurecimiento para legibilidad */
    z-index: 1;
  }

  .hero-content-wrapper {
    position: relative;
    z-index: 2; /* Asegura que el texto esté sobre la imagen y la superposición */
    margin-bottom: 2rem;
  }
  
  .hero-title {
    @include paragraph-h1;
    color: var(--main-yellow);
    margin: 0 0 1.5rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }
  
  .hero-subtitle {
    @include paragraph-small;
    color: var(--fill-white);
    margin: 0 0 2rem 0;
    opacity: 0.95;
    font-weight: 400; /* Un poco más legible que 300 sobre una imagen */
    font-size: 1rem;
  }

  .hero-button {
    position: relative;
    z-index: 2;
    background-color: var(--main-blue);
    color: var(--fill-white);
    border: none;
    display: inline-block;
  }
}

.features-section {
  margin: 1.5rem 0;

  .features-intro {
    @include paragraph-medium-light;
    color: var(--fill-white);
    text-align: center;
    margin-bottom: 2rem;
    opacity: 0.9;
    line-height: 1.5;
  }
  
  .features-title {
    @include paragraph-medium;
    color: var(--fill-white);
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 600;
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem; 
    margin-top: 2rem;
  }
}

:deep(.feature-card) {
    background-color: var(--main-blue);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin: 0.5rem 0;
    padding: 1rem 0.75rem !important;
    font-size: 0.95rem !important;
    max-width: 260px;
    min-width: 0;
    min-height: 90px;
    width: 100%;
    box-sizing: border-box;

    &:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
}

.features-grid {
    justify-items: center;
}


.credits-section {
  text-align: center;
  margin-top: 2rem;
  border-top: 1px solid rgba(253, 253, 253, 0.2);
  
  .credits-text {
    @include section-title;
    color: var(--main-yellow);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .credits-description {
    @include paragraph-small;
    color: var(--fill-white);
    opacity: 0.8;
    line-height: 1.5;
    max-width: 400px;
    margin: 0;
    font-weight: 300;
    font-size: 0.9rem;
  }
}

:deep(.nav-item) {
  @include section-title;
  color: var(--fill-white);
  text-transform: uppercase;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
  padding: 0;
  display: block;
  
  &:hover {
    opacity: 0.8;
  }
  
  &.router-link-active {
    color: var(--main-yellow);
  }
}
</style>

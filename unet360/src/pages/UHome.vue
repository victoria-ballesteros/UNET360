<template>
  <div class="home-container">

    <!-- HERO -->
    <section class="hero" ref="heroRef">
      <div class="hero-dots"></div>
      <div class="hero-vignette"></div>

      <div class="hero-inner">
        <!-- LEFT: texto -->
        <div class="hero-content">
          <div class="hero-eyebrow">
            <span class="eyebrow-dot"></span>
            Asistente Universitario
          </div>

          <h1 class="hero-title">
            Tu guía inteligente<br />
            para explorar la <br />
            <em>UNET</em>
          </h1>

          <p class="hero-sub">{{ generalInfo }}</p>

          <div class="button-container">
            <RouterLink :to="{ name: button.route }" class="no-underline-link">
              <UButton :text="button.label" type="contrast" size="lg" />
            </RouterLink>
          </div>
        </div>

        <!-- RIGHT: visual con anillos orbitales + logo pin -->
        <div class="hero-visual">
          <div class="orbit orbit-3"></div>
          <div class="orbit orbit-2"></div>
          <div class="orbit orbit-1"></div>

          <div class="orbit-icon oi-1">
            <UIcon name="icons/search" size="16" color="var(--contrast-blue)" />
          </div>

          <div class="orbit-icon oi-3">
            <UIcon name="icons/camera" size="16" color="var(--contrast-blue)" />
          </div>

          <div class="visual-center">
            <UIcon name="images/home-image" :size="isMobile ? 190 : 280" />
          </div>
        </div>
      </div>

      <div class="hero-badge-float">
        <span>360°</span>
      </div>
    </section>

    <!-- Insignia de administrador (solo PC, esquina inferior derecha) -->
    <div v-if="isAdminUser" class="admin-corner-badge">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="var(--main-yellow)" viewBox="0 0 16 16">
        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
      </svg>
      <span>Administrador</span>
    </div>

  </div>
</template>

<script setup>
import UIcon from "@/components/UIcon.vue"
import UButton from "@/components/UButton.vue"
import { ref, onMounted, onBeforeMount, onUnmounted } from "vue"
import { getGeneralInfo, getButtonData } from "@/service/global_dialogs"
import { useAuthStore } from "@/service/stores/auth"

let authStore = null
const generalInfo = getGeneralInfo()
const isAuthenticated = ref(false)
const isAdminUser = ref(false)
const button = ref(null)
const heroRef = ref(null)
const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onBeforeMount(() => {
  checkMobile()
  authStore = useAuthStore()
  isAuthenticated.value = authStore.isAuthenticated
  isAdminUser.value = !!authStore.user && (authStore.user.is_admin || authStore.user.role === 'admin')
  button.value = getButtonData(isAuthenticated.value)
})

onMounted(() => {
  window.addEventListener("resize", checkMobile)
})

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile)
})
</script>

<style scoped lang="scss">
@import "@/assets/styles/_colors.scss";
@import "@/assets/styles/_typography.scss";

/* ─── BASE ─────────────────────────────────────────────── */
.home-container {
  display: flex;
  flex-direction: column;
  flex: 1; /* FIX: reemplaza height:100dvh — crece dentro del wrapper sin forzar altura */
}

.no-underline-link {
  text-decoration: none;
}

/* ─── HERO ──────────────────────────────────────────────── */
.hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 0 2rem;
  flex: 1; /* FIX: llena home-container → el contenido queda centrado naturalmente */

  @media (max-width: 768px) {
    align-items: center;
    padding: 1rem;
  }
}

.hero-inner {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1100px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 3rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    text-align: left;
    gap: 0.5rem;
  }
}

/* ── Texto ── */
.hero-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;

  @media (max-width: 768px) {
    align-items: center;
    text-align: center;
    gap: 0.85rem; // Antes lo daban los margin-bottom de cada elemento
    padding: 0 0.5rem;
    order: 2;
  }
}

.hero-eyebrow {
  @include paragraph-medium;
  color: var(--contrast-blue);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.65rem;
  padding: 0.4rem 1rem; // Diseño de chip: también en desktop
  background: rgba(33, 118, 255, 0.1);
  border: 1px solid rgba(33, 118, 255, 0.25);
  border-radius: 999px;

  .eyebrow-dot {
    width: 4px;
    height: 4px;
    background: var(--contrast-blue);
    border-radius: 50%;
  }

  @media (max-width: 768px) {
    font-size: 1rem;
    margin-bottom: 0;
  }
}

.hero-title {
  @include paragraph-h1;
  font-size: 2.75rem;
  line-height: 1.1;
  color: var(--full-white);
  margin-bottom: 0.75rem;

  em {
    font-style: normal;
    color: var(--contrast-blue);
  }

  @media (max-width: 768px) {
    font-size: 2.2rem;
    line-height: 1.15;
    margin-bottom: 0;
    text-align: center;
    br { display: none; }
  }
}

.hero-sub {
  @include paragraph-medium-light;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.5;
  margin-bottom: 1.5rem;
  max-width: 400px;

  @media (max-width: 768px) {
    font-size: 1.05rem; /* <-- Aumentado para equilibrar el título grande */
    font-weight: 400;
    line-height: 1.4; /* <-- Interlineado ajustado para mejor lectura */
    margin: 0; /* <-- Sin margen: el espacio antes del botón lo da el gap del contenedor */
    max-width: 95%; /* <-- Permite que el texto respire mejor en los bordes */
    text-align: center;
  }
}

.button-container {
  @media (max-width: 768px) {
    display: flex;
    justify-content: center;
  }
}

/* ── Visual ── */
.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 380px;

  @media (max-width: 768px) {
    order: 1;
    height: 260px;
    margin-bottom: 0.5rem;
    justify-content: center;
  }
}

.orbit {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 239, 61, 0.18);
  transform: rotateX(65deg) rotateZ(-15deg);
  transition: opacity 0.3s ease;

  &.orbit-1 { 
    width: 220px; height: 220px; 
    animation: pulseOrbit 3s ease-in-out infinite;
    @media (max-width: 768px) { width: 160px; height: 160px; } 
  }
  &.orbit-2 { 
    width: 290px; height: 290px; 
    border-color: rgba(255, 239, 61, 0.1); 
    animation: pulseOrbit 4.2s ease-in-out infinite 0.4s;
    @media (max-width: 768px) { width: 210px; height: 210px; } 
  }
  &.orbit-3 { 
    width: 360px; height: 360px; 
    border-color: rgba(255, 239, 61, 0.05); 
    animation: pulseOrbit 5.4s ease-in-out infinite 0.8s;
    @media (max-width: 768px) { width: 260px; height: 260px; } 
  }
}

.orbit-icon {
  position: absolute;
  z-index: 3;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 239, 61, 0.1);
  border: 1px solid rgba(255, 239, 61, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
  animation: floatIcon 2.4s ease-in-out infinite;

  &:hover {
    background: rgba(255, 239, 61, 0.25);
    border-color: var(--contrast-blue);
  }

  &.oi-1 { 
    top: 18%; right: 12%; animation-delay: 0s; 
    @media (max-width: 768px) {
      top: 10%;
      right: 15%;
    }
  }
  &.oi-2 { 
    bottom: 22%; right: 8%; animation-delay: 0.6s; 
    @media (max-width: 768px) {
      bottom: 12%;
      right: 12%;
    }
  }
  &.oi-3 { 
    top: 40%; left: 6%; animation-delay: 1.2s; 
    @media (max-width: 768px) {
      top: 36%;
      left: 8%;
    }
  }
}

@keyframes pulseOrbit {
  0%, 100% {
    opacity: 0.6;
    transform: rotateX(65deg) rotateZ(-15deg) scale(1);
  }
  50% {
    opacity: 1;
    transform: rotateX(63deg) rotateZ(-10deg) scale(1.04);
  }
}

@keyframes floatIcon {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.visual-center {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Botón ── */
.button-container {
  @media (max-width: 768px) {
    align-self: center;
  }
}

:deep(.u-button) {
  background: var(--main-yellow) !important;
  color: var(--strong-gray-dark) !important;
  font-weight: 600;

  @media (max-width: 768px) {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }
}

.hero-badge-float {
  display: none;
}

/* ── Insignia de administrador (solo desktop) ── */
.admin-corner-badge {
  display: none;

  @media (min-width: 769px) {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 239, 61, 0.08);
    border: 1px solid rgba(255, 239, 61, 0.25);
    border-radius: 999px;
    color: var(--main-yellow);
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 50;
  }
}
</style>
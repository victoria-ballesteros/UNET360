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
              <UButton :text="button.label" type="contrast" />
            </RouterLink>
          </div>
        </div>

        <!-- RIGHT: visual con anillos orbitales + logo pin -->
        <div class="hero-visual">
          <div class="orbit orbit-3"></div>
          <div class="orbit orbit-2"></div>
          <div class="orbit orbit-1"></div>

          <div class="orbit-icon oi-1">
            <UIcon name="icons/search" size="16" color="var(--main-yellow)" />
          </div>
          <div class="orbit-icon oi-2">
            <UIcon name="icons/route-arrow" size="16" color="var(--main-yellow)" />
          </div>
          <div class="orbit-icon oi-3">
            <UIcon name="icons/camera" size="16" color="var(--main-yellow)" />
          </div>

          <div class="visual-center">
            <UIcon name="images/home-image" :size="isMobile ? 160 : 280" />
          </div>
        </div>
      </div>

      <div class="hero-badge-float">
        <span>360°</span>
      </div>
    </section>

  </div>
</template>

<script setup>
import UIcon from "@/components/UIcon.vue"
import UButton from "@/components/UButton.vue"
import { ref, onMounted, onBeforeMount } from "vue"
import { getGeneralInfo, getButtonData } from "@/service/global_dialogs"
import { useAuthStore } from "@/service/stores/auth"

let authStore = null
const generalInfo = getGeneralInfo()
const isAuthenticated = ref(false)
const button = ref(null)
const heroRef = ref(null)
const isMobile = ref(window.innerWidth <= 768)

onBeforeMount(() => {
  authStore = useAuthStore()
  isAuthenticated.value = authStore.isAuthenticated
  button.value = getButtonData(isAuthenticated.value)
})

onMounted(() => {
  // altura manejada por flex del layout
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
  background: var(--strong-gray-dark);
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

  .hero-dots {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255, 239, 61, 0.1) 1px, transparent 1px);
    background-size: 24px 24px;
    pointer-events: none;
    z-index: 0;
  }

  .hero-vignette {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 70% at 50% 50%, transparent 20%, var(--strong-gray-dark) 100%);
    pointer-events: none;
    z-index: 1;
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
    align-items: flex-start;
    padding: 0 0.5rem;
    order: 2;
  }
}

.hero-eyebrow {
  @include paragraph-small;
  color: rgba(255, 255, 255, 0.4);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.65rem;

  .eyebrow-dot {
    width: 4px;
    height: 4px;
    background: var(--main-yellow);
    border-radius: 50%;
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
    color: var(--main-yellow);
  }

  @media (max-width: 768px) {
    font-size: 1.6rem;
    line-height: 1.2;
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
    font-size: 0.85rem;
    margin-bottom: 1.25rem;
    max-width: 85%;
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
    height: 220px;
    margin-bottom: 0rem;
    justify-content: center;
  }
}

.orbit {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 239, 61, 0.18);
  transform: rotateX(65deg) rotateZ(-15deg);

  &.orbit-1 { width: 220px; height: 220px; @media (max-width: 768px) { width: 150px; height: 150px; } }
  &.orbit-2 { width: 290px; height: 290px; border-color: rgba(255, 239, 61, 0.1); @media (max-width: 768px) { width: 200px; height: 200px; } }
  &.orbit-3 { width: 360px; height: 360px; border-color: rgba(255, 239, 61, 0.05); @media (max-width: 768px) { width: 260px; height: 260px; } }
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

  @media (max-width: 768px) {
    width: 28px;
    height: 28px;
  }

  &.oi-1 { top: 18%; right: 12%; }
  &.oi-2 { bottom: 22%; right: 8%; }
  &.oi-3 { top: 40%; left: 6%; }
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
</style>
<template>
  <div class="about-container">

    <!-- HERO -->
    <section class="hero">
      <div class="hero-noise"></div>
      <div class="hero-grid"></div>

      <div class="hero-inner">
        <div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          Primera app de mapas de la UNET
        </div>

        <h1 class="hero-title">
          Navega tu<br />
          <em>universidad</em><br />
          en 360°
        </h1>

        <p class="hero-sub">
          Encuentra salones, rutas y más —<br />sin perderte nunca más.
        </p>

        <UButton
          type="contrast"
          text="Probar ahora"
          @click="navigateToMap"
          class="hero-btn"
        />
      </div>

      <!-- decorative floating badge -->
      <div class="hero-badge-float">
        <span>360°</span>
      </div>
    </section>

    <!-- FEATURES SECTION -->
    <section class="features">
      <div class="features-header">
        <p class="overline">Funcionalidades</p>
        <h2 class="features-title">Todo lo que necesitas para moverte en el campus</h2>
      </div>

      <div class="features-grid">
        <div class="feat-card" v-for="(feat, i) in features" :key="i" :style="`--i: ${i}`">
          <div class="feat-number">0{{ i + 1 }}</div>
          <div class="feat-icon-wrap">
            <UIcon :name="feat.icon" size="24" color="var(--main-yellow)" />
          </div>
          <h3 class="feat-title">{{ feat.title }}</h3>
          <p class="feat-desc">{{ feat.desc }}</p>
        </div>
      </div>
    </section>

    <!-- COMPARISON SECTION -->
    <section class="comparison">
      <div class="comparison-header">
        <p class="overline">¿Por qué UNET360?</p>
        <h2 class="comparison-title">Mapa tradicional vs. UNET360</h2>
        <p class="comparison-sub">¿Cansado de perderte en el campus? Los mapas estáticos no ayudan, y preguntar a cada rato tampoco es la solución.</p>
      </div>

      <div class="comparison-grid">
        <div class="comp-col comp-col--old">
          <div class="comp-col-header">
            <span class="comp-tag comp-tag--bad">Antes</span>
            <p class="comp-col-title">Mapa tradicional</p>
          </div>
          <ul class="comp-list">
            <li v-for="item in oldWay" :key="item">
              <span class="comp-icon comp-icon--bad">✕</span>
              {{ item }}
            </li>
          </ul>
        </div>

        <div class="comp-divider">
          <div class="comp-divider-line"></div>
          <div class="comp-divider-vs">VS</div>
          <div class="comp-divider-line"></div>
        </div>

        <div class="comp-col comp-col--new">
          <div class="comp-col-header">
            <span class="comp-tag comp-tag--good">Ahora</span>
            <p class="comp-col-title">UNET360</p>
          </div>
          <ul class="comp-list">
            <li v-for="item in newWay" :key="item">
              <span class="comp-icon comp-icon--good">✓</span>
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- FOOTER / CREDITS -->
    <footer class="credits">
      <div class="credits-inner">
        <div class="credits-mark">UNET360</div>
        <h3 class="credits-title">Creado por estudiantes UNETENSES</h3>
        <p class="credits-desc">
          Somos estudiantes de Informática. Desarrollamos esta app para hacer la vida universitaria más fácil y accesible para todos.
        </p>
      </div>
    </footer>

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
import UIcon from '@/components/UIcon.vue'
import USidebar from '@/components/USidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const isPanelOpen = ref(false)

const features = [
  {
    icon: 'icons/camera',
    title: 'Fotos en 360°',
    desc: 'Explora edificios y salones como si estuvieras parado justo ahí, desde tu celular.',
  },
  {
    icon: 'icons/route-arrow',
    title: 'Rutas inteligentes',
    desc: 'Navega del punto A al punto B con instrucciones visuales claras y directas.',
  },
  {
    icon: 'icons/search',
    title: 'Buscador global',
    desc: 'Encuentra cualquier salón, laboratorio o departamento en cuestión de segundos.',
  },
]

const oldWay = [
  'Mapas en papel desactualizados',
  'Sin rutas de navegación',
  'Imposible ver el interior',
  'Preguntar a cada persona que encuentras',
]

const newWay = [
  'Vistas 360° inmersivas y actualizadas',
  'Rutas paso a paso visuales',
  'Recorre el campus virtualmente',
  'Buscador instantáneo por nombre',
]

const togglePanel = () => { isPanelOpen.value = !isPanelOpen.value }
const closePanel = () => { isPanelOpen.value = false }
const navigateToMap = () => { router.push({ name: 'Map' }) }
const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'Login' })
  closePanel()
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

/* ─── BASE ─────────────────────────────────────────────── */
.about-container {
  min-height: 100vh;
  background: var(--strong-gray);
  color: var(--full-white);
  padding-bottom: 4rem;
}

.overline {
  @include paragraph-small;
  color: var(--main-yellow);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 0.75rem;
}

/* ─── HERO ──────────────────────────────────────────────── */
.hero {
  position: relative;
  background: var(--strong-gray-dark);
  min-height: 72vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 5rem 2rem 6rem;

  /* subtle dot-grid texture */
  .hero-grid {
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(circle, rgba(255,239,61,0.12) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
  }

  /* vignette on top of grid */
  .hero-noise {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 70% 60% at 50% 50%, transparent 30%, var(--strong-gray-dark) 100%);
    pointer-events: none;
    z-index: 1;
  }
}

.hero-inner {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 560px;
}

.hero-eyebrow {
  @include paragraph-medium-light;
  font-size: 1.125rem;
  color: rgba(255,255,255,0.45);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.75rem;

  .eyebrow-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--main-yellow);
    display: inline-block;
  }
}

.hero-title {
  @include paragraph-h1;
  font-size: 3rem;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 1.25rem;
  color: var(--full-white);

  em {
    font-style: normal;
    color: var(--main-yellow);
  }

  @media (min-width: 768px) {
    font-size: 4rem;
  }
}

.hero-sub {
  @include paragraph-medium-light;
  color: rgba(255,255,255,0.5);
  margin-bottom: 2.5rem;
  line-height: 1.7;

  @media (min-width: 768px) {
    font-size: 1.25rem;
  }
}

.hero-btn {
  position: relative;
  z-index: 2;
  margin: 0 auto;
  display: block;
}

/* floating 360 badge */
.hero-badge-float {
  position: absolute;
  z-index: 3;
  bottom: 2.5rem;
  right: 2rem;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 1.5px solid rgba(255,239,61,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,239,61,0.06);

  span {
    @include paragraph-small;
    color: var(--main-yellow);
    letter-spacing: 0.05em;
  }

  @media (max-width: 480px) {
    display: none;
  }
}

/* ─── FEATURES ──────────────────────────────────────────── */
.features {
  max-width: 1100px;
  margin: 0 auto;
  padding: 5rem 1.5rem 4rem;
}

.features-header {
  margin-bottom: 3rem;

  .features-title {
    @include section-title;
    color: var(--full-white);
    max-width: 420px;
    line-height: 1.25;

    @media (min-width: 768px) {
      font-size: 2rem;
    }
  }
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1px;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;

  @media (min-width: 768px) {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feat-card {
  padding: 2rem 1.75rem;
  background: var(--strong-gray-dark);
  position: relative;
  transition: background 0.25s ease;

  /* right border between cards */
  &:not(:last-child) {
    border-right: 1px solid rgba(255,255,255,0.08);
  }

  &:hover {
    background: rgba(255, 239, 61, 0.04);
  }

  .feat-number {
    @include paragraph-extra-small;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
  }

  .feat-icon-wrap {
    margin-bottom: 1.25rem;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255,239,61,0.25);
    border-radius: 10px;
    background: rgba(255,239,61,0.07);
  }

  .feat-title {
    @include paragraph-medium;
    color: var(--full-white);
    margin-bottom: 0.6rem;

    @media (min-width: 768px) {
      font-size: 1.25rem;
    }
  }

  .feat-desc {
    @include paragraph-small;
    color: rgba(255,255,255,0.45);
    font-weight: 400;
    line-height: 1.6;
  }
}

/* ─── COMPARISON ────────────────────────────────────────── */
.comparison {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem 5rem;
}

.comparison-header {
  margin-bottom: 2.5rem;

  .comparison-title {
    @include section-title;
    color: var(--full-white);
    margin-bottom: 0.75rem;

    @media (min-width: 768px) {
      font-size: 2rem;
    }
  }

  .comparison-sub {
    @include paragraph-medium-light;
    font-size: 1.125rem;
    color: rgba(255,255,255,0.45);
    max-width: 480px;
    line-height: 1.7;
    font-weight: 400;
  }
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 0;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.comp-col {
  padding: 2rem 1.75rem;
  background: var(--strong-gray-dark);

  &--new {
    background: rgba(255,239,61,0.03);
  }
}

.comp-col-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.comp-tag {
  @include paragraph-extra-small;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-weight: 600;

  &--bad {
    background: rgba(211, 49, 36, 0.15);
    color: #e8695f;
    border: 1px solid rgba(211, 49, 36, 0.3);
  }

  &--good {
    background: rgba(255, 239, 61, 0.1);
    color: var(--main-yellow);
    border: 1px solid rgba(255, 239, 61, 0.25);
  }
}

.comp-col-title {
  @include paragraph-medium;
  font-size: 1.125rem;
  color: var(--full-white);
}

.comp-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;

  li {
    @include paragraph-medium-light;
    color: rgba(255,255,255,0.55);
    font-weight: 400;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    line-height: 1.5;
  }
}

.comp-icon {
  font-style: normal;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;

  &--bad {
    background: rgba(211, 49, 36, 0.15);
    color: #e8695f;
  }

  &--good {
    background: rgba(255, 239, 61, 0.12);
    color: var(--main-yellow);
  }
}

.comp-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 0;
  border-left: 1px solid rgba(255,255,255,0.08);
  border-right: 1px solid rgba(255,255,255,0.08);

  @media (max-width: 640px) {
    flex-direction: row;
    padding: 0 2rem;
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }

  .comp-divider-line {
    flex: 1;
    width: 1px;
    background: rgba(255,255,255,0.08);

    @media (max-width: 640px) {
      width: auto;
      height: 1px;
    }
  }

  .comp-divider-vs {
    @include paragraph-extra-small;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.15em;
    padding: 0.6rem 0.75rem;
  }
}

/* ─── CREDITS / FOOTER ──────────────────────────────────── */
.credits {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.credits-inner {
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  background: var(--strong-gray-dark);
  position: relative;
  overflow: hidden;

  /* subtle yellow top accent line */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,239,61,0.4), transparent);
  }
}

.credits-mark {
  @include paragraph-extra-small;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--main-yellow);
  text-transform: uppercase;
  margin-bottom: 1.25rem;
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border: 1px solid rgba(255,239,61,0.2);
  border-radius: 4px;
  background: rgba(255,239,61,0.06);
}

.credits-title {
  @include section-title;
  color: var(--full-white);
  margin-bottom: 0.85rem;
}

.credits-desc {
  @include paragraph-medium-light;
  color: rgba(255,255,255,0.4);
  max-width: 420px;
  margin: 0 auto;
  line-height: 1.75;
  font-weight: 400;
}

/* ─── SIDEBAR NAV ITEMS ─────────────────────────────────── */
:deep(.nav-item) {
  @include section-title;
  color: var(--full-white);
  text-transform: uppercase;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
  padding: 0;
  display: block;

  &:hover { opacity: 0.7; }

  &.router-link-active { color: var(--main-yellow); }
}
</style>
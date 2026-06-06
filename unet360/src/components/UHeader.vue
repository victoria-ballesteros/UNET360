<template>
  <header class="header-container">

    <!-- Logo (siempre visible) -->
    <RouterLink :to="{ name: 'Home' }" class="logo-link">
      <UIcon name="icons/logo" size="43" class="cursor-pointer" />
    </RouterLink>

    <!-- ══ DESKTOP: navbar horizontal ══ -->
    <nav v-if="navOptions.length" class="desktop-nav" aria-label="Navegación principal">
      <template v-for="(option, i) in navLinks" :key="i">
        <RouterLink :to="option.to" class="nav-link">
          {{ option.label }}
        </RouterLink>
      </template>

      <!-- Separador visual -->
      <span v-if="logoutOption" class="nav-divider" aria-hidden="true" />

      <!-- Cerrar sesión -->
      <UButton
        v-if="logoutOption"
        class="nav-logout-btn"
        icon="close-session"
        :text="logoutOption.label"
        type="danger"
        size="sm"
        @click="emit('logout')"
      />
    </nav>

    <!-- ══ MOBILE: ícono hamburguesa ══ -->
    <UButton
      class="hamburger-btn"
      icon="list"
      type="tertiary"
      size="lg"
      aria-label="Abrir menú"
      @click="emit('isPanelOpen')"
    />

  </header>
</template>

<script setup>
import UButton from '@/components/UButton.vue';
import UIcon from '@/components/UIcon.vue';
import { RouterLink } from 'vue-router';
import { computed } from 'vue';

const props = defineProps({
  /** Array de opciones de navegación de getSidebarOptions() */
  navOptions: { type: Array, default: () => [] },
});

const emit = defineEmits(['isPanelOpen', 'isPanelOpenFromLogo', 'logout']);

/** Links de ruta (excluye acciones como logout) */
const navLinks = computed(() => props.navOptions.filter(o => o.to && !o.action));

/** Opción de logout si existe */
const logoutOption = computed(() => props.navOptions.find(o => o.action === 'logout'));
</script>

<style scoped lang="scss">
// ══════════════════════════════════════════════════
// ═══  Header / Navbar                           ═══
// ══════════════════════════════════════════════════

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.625rem 1.125rem;
  z-index: 100;
  position: relative;

  // ── Desktop: aspecto de navbar completa ───────────────────
  @media (min-width: 768px) {
    padding: 1rem 2rem;
    height: 56px;
  }
}

// ── Logo ──────────────────────────────────────────
.logo-link {
  display: inline-flex;
  line-height: 0;
  text-decoration: none;
  flex-shrink: 0;
}

// ══ DESKTOP NAV ═══════════════════════════════════

.desktop-nav {
  display: none; // Oculto en mobile

  @media (min-width: 768px) {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
}

.nav-link {
  position: relative;
  padding: 0.45rem 0.85rem;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.03em;
  transition: color 0.18s ease, background 0.18s ease;
  white-space: nowrap;

  &:hover {
    color: var(--full-white);
    background: rgba(255, 255, 255, 0.07);
  }

  // Link de la ruta activa actual
  &.router-link-active {
    color: var(--main-yellow, #ffef3d);
    background: rgba(255, 239, 61, 0.08);
    font-weight: 600;
  }
}

// Separador vertical entre links y logout
.nav-divider {
  display: block;
  width: 1px;
  height: 18px;
  background: rgba(255, 255, 255, 0.12);
  margin: 0 0.5rem;
  flex-shrink: 0;
}

// Botón "Cerrar sesión" con estilo de peligro sutil
.nav-logout-btn {
  :deep(button) {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    border: 1px solid rgba(229, 57, 53, 0.35);
    background: rgba(229, 57, 53, 0.08);
    color: rgba(229, 57, 53, 0.85);
    font-size: 0.8rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
    white-space: nowrap;

    svg {
      flex-shrink: 0;
      opacity: 0.8;
      transition: opacity 0.18s ease;
    }

    &:hover {
      background: rgba(229, 57, 53, 0.18);
      border-color: rgba(229, 57, 53, 0.6);
      color: #ff5252;

      svg { opacity: 1; }
    }
  }
}

// ══ MOBILE: hamburguesa ════════════════════════════

.hamburger-btn {
  // En desktop se oculta (la navbar reemplaza al hamburgesa)
  @media (min-width: 768px) {
    display: none;
  }

  :deep(button) {
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 6px;
    width: auto;
    height: auto;
    transition: background 0.15s ease;

    &:hover { background: rgba(255, 255, 255, 0.07); }
  }
}
</style>
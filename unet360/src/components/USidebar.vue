<template>
  <Teleport to="body">
    <transition name="overlay-fade">
      <div
        v-if="isOpen"
        class="sidebar-overlay"
        @click="closePanel"
      />
    </transition>

    <transition name="panel-slide">
      <aside
        v-if="isOpen"
        class="sidebar-panel"
        @click.stop
      >
        <UHeader @isPanelOpen="emit('close', $event)" @isPanelOpenFromLogo="emit('close', $event)" />
        
        <div v-if="authStore.isAuthenticated && authStore.user" class="user-info">
          
          <div class="user-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16">
              <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
            </svg>
          </div>

          <span class="user-name" :title="formattedUserName || authStore.user.email">
            {{ formattedUserName || authStore.user.email }}
          </span>
          
          <div 
            v-if="authStore.user.is_admin || authStore.user.role === 'admin'" 
            class="admin-icon" 
            title="Administrador"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="var(--main-yellow)" viewBox="0 0 16 16">
              <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
            </svg>
          </div>
        </div>

        <nav class="menu">
          <slot />
        </nav>
      </aside>
    </transition>
  </Teleport>
</template>

<script setup>
import { computed } from "vue";
import { defineProps, defineEmits } from "vue";
import UHeader from "./UHeader.vue";
import { useAuthStore } from "@/service/stores/auth";
import { formatUserName } from "@/service/shared/utils";

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close"]);

// Inicializar la store de autenticación
const authStore = useAuthStore();

const formattedUserName = computed(() => {
  if (!authStore.user) return "";
  return formatUserName(authStore.user.name || authStore.user.email);
});

function closePanel() {
  emit("close");
}
</script>

<style lang="scss">
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 1000;

  // En desktop la navbar reemplaza al sidebar
  @media (min-width: 768px) {
    display: none !important;
  }
}

.sidebar-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 1001;
  background: var(--strong-gray);
  width: 100vw;
  padding: 1.5rem 0 2rem;
  box-shadow: -4px 0 32px rgba(0, 0, 0, 0.35);
  overflow-x: hidden;
  overflow-y: auto;
  display: flex;
  flex-direction: column;

  // En desktop la navbar reemplaza al sidebar
  @media (min-width: 768px) {
    display: none !important;
  }

  @media (min-width: 768px) {
    width: 25vw;
    min-width: 280px;
    max-width: 420px;
    border-left: 1px solid rgba(255, 255, 255, 0.06);
  }

  /* Estilos para la sección del usuario */
  .user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0 1.5rem;
    margin-top: 1.5rem;

    .user-icon {
      display: flex;
      align-items: center;
      color: var(--main-yellow);
      flex-shrink: 0;
    }

    .user-name {
      @include paragraph-medium;
      font-weight: 600;
      letter-spacing: 0.03em;
      color: var(--main-yellow);
      flex-grow: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .admin-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
  }

  .menu {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    flex: 1 1 auto;
    padding: 2rem 1.5rem;
    justify-content: center;

    .nav-item {
      @include paragraph-medium;
      color: rgba(255, 255, 255, 0.65);
      text-transform: uppercase;
      text-decoration: none;
      background: none;
      border: none;
      cursor: pointer;
      width: 100%;
      text-align: left;
      padding: 0.75rem 1rem;
      display: block;
      border-radius: 10px;
      letter-spacing: 0.06em;
      transition: color 0.18s ease, background 0.18s ease;

      &:hover {
        color: var(--fill-white);
        background: rgba(255, 255, 255, 0.07);
      }

      &.router-link-active,
      &.active {
        color: var(--fill-white);
        background: rgba(255, 255, 255, 0.1);
      }
    }
  }
}

// Overlay — fade only
.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.3s ease;
}
.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}

// Panel — slide only, no opacity involved
.panel-slide-enter-active,
.panel-slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.panel-slide-enter-from,
.panel-slide-leave-to {
  transform: translateX(100%);
}
</style>
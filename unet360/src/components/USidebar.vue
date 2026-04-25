<template>
  <Teleport to="body">
    <!-- Overlay: only fades -->
    <transition name="overlay-fade">
      <div
        v-if="isOpen"
        class="sidebar-overlay"
        @click="closePanel"
      />
    </transition>

    <!-- Panel: only slides -->
    <transition name="panel-slide">
      <aside
        v-if="isOpen"
        class="sidebar-panel"
        @click.stop
      >
        <UHeader @isPanelOpen="emit('close', event)" />
        <nav class="menu">
          <slot />
        </nav>
      </aside>
    </transition>
  </Teleport>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import UHeader from "./UHeader.vue";

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close"]);

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

  @media (min-width: 768px) {
    width: 25vw;
    min-width: 280px;
    max-width: 420px;
    border-left: 1px solid rgba(255, 255, 255, 0.06);
  }

  .menu {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    flex: 1 1 auto;
    padding: 2rem 1.5rem;
    justify-content: center;

    .nav-item {
      @include section-title;
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
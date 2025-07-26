<template>
  <transition name="slide">
    <div v-if="isOpen" class="overlay" @click.self="closePanel">
      <aside class="panel" @click.stop>
        <UHeader @isPanelOpen="emit('close', event)"></UHeader>
        <nav class="menu">
          <slot />
        </nav>
      </aside>
    </div>
  </transition>
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
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000;
  display: flex;
}

.panel {
  background: var(--strong-gray);
  width: 100vw;
  height: 100vh;
  padding: 1.5rem 1rem;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.3);
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;

  .close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    position: absolute;
    top: 1rem;
    right: 1rem;
  }

  .menu {
    display: flex;
    flex-direction: column;
    gap: 1.738rem;
    justify-content: center;
    flex: 1 1 auto;

    .nav-item {
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
    }
  }
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.slide-enter-to {
  transform: translateX(0);
  opacity: 1;
}
.slide-leave-from {
  transform: translateX(0);
  opacity: 1;
}
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>

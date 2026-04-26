<template>
  <transition name="dialog-fade">
    <div v-if="modelValue" class="dialog-backdrop" @click.self="close">
      <div class="dialog-content">
        <div class="dialog-header" v-if="headerTitle?.trim()">
          <p class="header-title">{{ headerTitle }}</p>
          <button class="dialog-close" @click="close">
            <UIcon name="x-lg" size="16" color="currentColor" />
          </button>
        </div>
        <div class="dialog-body">
          <slot />
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import UIcon from './UIcon.vue'

const props = defineProps({
  modelValue: Boolean,
  headerTitle: {
    type: String,
    default: 'Formulario'
  }
})
const emit = defineEmits(['update:modelValue'])

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped lang="scss">
.dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.dialog-content {
  position: relative;
  background: var(--strong-gray);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  width: 92%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
  display: flex;
  flex-direction: column;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  flex-shrink: 0;

  .header-title {
    margin: 0;
    color: var(--full-white);
    font-weight: 600;
    @include paragraph-medium;
  }
}

.dialog-close {
  background: rgba(255, 255, 255, 0.07);
  border: none;
  border-radius: 8px;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s ease, color 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.13);
    color: var(--full-white);
  }
}

.dialog-body {
  padding: 1.5rem;
  color: var(--full-white);
}

// Transition
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.2s ease;

  .dialog-content {
    transition: transform 0.2s ease, opacity 0.2s ease;
  }
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;

  .dialog-content {
    transform: scale(0.96) translateY(8px);
    opacity: 0;
  }
}
</style>
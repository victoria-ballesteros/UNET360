<template>
  <Teleport to="body">
    <Transition name="um-fade">
      <div
        v-if="modelValue"
        class="um-backdrop"
        :class="{ 'um-no-close': !closable }"
        @click.self="handleBackdropClick"
        role="dialog"
        aria-modal="true"
        :aria-label="title || 'Modal'"
      >
        <div
          class="um-panel"
          :class="[`um-panel--${size}`, { 'um-panel--danger': danger }]"
        >
          <!-- ── Header ─────────────────────────────────── -->
          <div v-if="$slots.header || title" class="um-header" :class="{ 'um-header--danger': danger }">
            <slot name="header">
              <h2 class="um-title">{{ title }}</h2>
            </slot>
            <UButton v-if="closable" class="um-close" icon="x-lg" type="tertiary" size="sm" @click="close" />
          </div>

          <!-- ── Body ──────────────────────────────────── -->
          <div class="um-body" :class="{ 'um-body--no-padding': noPadding }">
            <slot />
          </div>

          <!-- ── Footer ────────────────────────────────── -->
          <div v-if="$slots.footer" class="um-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import UButton from './UButton.vue';

const props = defineProps({
  modelValue: { type: Boolean, required: true },
  title:      { type: String,  default: '' },
  size:       { type: String,  default: 'md', validator: v => ['sm', 'md', 'lg', 'auto'].includes(v) },
  closable:   { type: Boolean, default: true },
  danger:     { type: Boolean, default: false },
  noPadding:  { type: Boolean, default: false },
});

const emit = defineEmits(['update:modelValue', 'close']);

function close() {
  emit('update:modelValue', false);
  emit('close');
}

function handleBackdropClick() {
  if (props.closable) close();
}

// Trap scroll & Esc key
function onKeydown(e) {
  if (e.key === 'Escape' && props.modelValue && props.closable) close();
}

onMounted(() => window.addEventListener('keydown', onKeydown));
onUnmounted(() => window.removeEventListener('keydown', onKeydown));
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

// ── Backdrop ─────────────────────────────────────────────
.um-backdrop {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(10, 12, 16, 0.7);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 1000;
  box-sizing: border-box;
}

// ── Panel ─────────────────────────────────────────────────
.um-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-height: calc(100dvh - 3rem);
  background: var(--strong-gray, #303745);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 18px;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.04),
    0 24px 64px rgba(0, 0, 0, 0.55),
    0 8px 24px rgba(0, 0, 0, 0.35);
  overflow: hidden;

  // Sizes
  &--sm   { max-width: 380px; }
  &--md   { max-width: 520px; }
  &--lg   { max-width: 760px; }
  &--auto { max-width: 90vw; }

  // Danger tint: borde y shimmer rojo sutil
  &--danger {
    border-color: rgba(211, 49, 36, 0.25);
    box-shadow:
      0 0 0 1px rgba(211, 49, 36, 0.08),
      0 24px 64px rgba(0, 0, 0, 0.55);
  }
}

// ── Header ────────────────────────────────────────────────
.um-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.02);

  &--danger {
    background: rgba(211, 49, 36, 0.07);
    border-bottom-color: rgba(211, 49, 36, 0.15);
  }
}

.um-title {
  margin: 0;
  @include paragraph-medium;
  font-size: 1rem;
  color: var(--full-white);
  letter-spacing: -0.01em;
}

// ── Close button ──────────────────────────────────────────
.um-close {
  flex-shrink: 0;

  :deep(.ub) {
    width: 2rem;
    height: 2rem;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.45);
    padding: 0;

    &:hover {
      background: rgba(255, 255, 255, 0.09);
      color: var(--full-white);
      transform: none;
    }
  }
}

// ── Body ──────────────────────────────────────────────────
.um-body {
  padding: 1.5rem;
  color: var(--full-white);
  overflow-y: auto;
  flex: 1;
  min-height: 0;

  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.12) transparent;

  &::-webkit-scrollbar       { width: 4px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.12); border-radius: 4px; }

  &--no-padding {
    padding: 0;
  }
}

// ── Footer ────────────────────────────────────────────────
.um-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.625rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.01);
}

// ── Transitions ───────────────────────────────────────────
.um-fade-enter-active {
  transition: opacity 0.22s ease;
  .um-panel {
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.22s ease;
  }
}
.um-fade-leave-active {
  transition: opacity 0.18s ease;
  .um-panel {
    transition: transform 0.18s ease, opacity 0.18s ease;
  }
}

.um-fade-enter-from {
  opacity: 0;
  .um-panel {
    opacity: 0;
    transform: scale(0.93) translateY(12px);
  }
}
.um-fade-leave-to {
  opacity: 0;
  .um-panel {
    opacity: 0;
    transform: scale(0.96) translateY(6px);
  }
}
</style>

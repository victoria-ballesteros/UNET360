<template>
  <button
    :class="[
      'ub',
      `ub--${type}`,
      `ub--${size}`,
      { 'ub--full': full, 'ub--loading': loading, 'ub--icon-only': icon && !text }
    ]"
    :disabled="loading || type === 'deactivated'"
    @click="handleClick"
    type="button"
  >
    <!-- Loading spinner -->
    <span v-if="loading" class="ub-spinner" aria-hidden="true">
      <svg viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="35 15"/>
      </svg>
    </span>

    <!-- Icon -->
    <UIcon
      v-if="icon && !loading"
      :name="icon"
      :size="iconSizeMap[size]"
      :color="iconColor"
      class="ub-icon"
    />

    <!-- Label -->
    <span v-if="text" class="ub-label">{{ text }}</span>
  </button>
</template>

<script setup>
import UIcon from './UIcon.vue';

const props = defineProps({
  type: {
    type: String,
    default: 'primary',
    validator: v => ['primary','secondary','tertiary','contrast','contrast-2','blue','danger','deactivated'].includes(v),
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v),
  },
  text:     { type: String,  required: false },
  icon:     { type: String,  required: false },
  iconColor:{ type: String,  required: false },
  loading:  { type: Boolean, default: false },
  full:     { type: Boolean, default: false },
});

const emit = defineEmits(['click']);
const handleClick = (e) => emit('click', e);

const iconSizeMap = { sm: '14', md: '16', lg: '18' };
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

// ══════════════════════════════════════════════
// Base
// ══════════════════════════════════════════════
.ub {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  letter-spacing: 0.01em;
  white-space: nowrap;
  overflow: hidden;
  transition:
    background 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.15s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.2s ease;
  outline: none;
  text-decoration: none;
  -webkit-font-smoothing: antialiased;

  &:focus-visible {
    outline: 2px solid rgba(255, 239, 61, 0.7);
    outline-offset: 3px;
  }

  &:hover:not(:disabled) {
    transform: translateY(-1.5px);
  }

  &:active:not(:disabled) {
    transform: translateY(0.5px) scale(0.98);
    transition-duration: 0.06s;
  }
}

// ── Sizes ──────────────────────────────────────
.ub--sm {
  padding: 0.4rem 0.875rem;
  font-size: 0.75rem;
  border-radius: 8px;
  .ub-spinner svg { width: 13px; height: 13px; }
}
.ub--md {
  padding: 0.6rem 1.25rem;
  font-size: 0.875rem;
  .ub-spinner svg { width: 15px; height: 15px; }
}
.ub--lg {
  padding: 0.75rem 1.625rem;
  font-size: 1rem;
  border-radius: 12px;
  .ub-spinner svg { width: 17px; height: 17px; }
}

.ub--full { width: 100%; }

// ── Icon-only circular ─────────────────────────
.ub--icon-only {
  padding: 0;
  border-radius: 50%;

  &.ub--sm  { width: 2rem;    height: 2rem; }
  &.ub--md  { width: 2.375rem; height: 2.375rem; }
  &.ub--lg  { width: 2.75rem; height: 2.75rem; }
}

// ── Loading ────────────────────────────────────
.ub--loading {
  pointer-events: none;
  opacity: 0.75;
}

.ub-spinner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  animation: ub-spin 0.8s linear infinite;

  svg { display: block; }
}

@keyframes ub-spin {
  to { transform: rotate(360deg); }
}

// ══════════════════════════════════════════════
// Types
// ══════════════════════════════════════════════

// ── Primary: dark glass / minimalist ───────────
.ub--primary {
  background: var(--strong-gray, #303745);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);

  &:hover:not(:disabled) {
    background: #394151;
    border-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }
}

// ── Secondary: outline ghost ───────────────────
.ub--secondary {
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);

  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.06);
    color: var(--full-white);
    border-color: rgba(255, 255, 255, 0.45);
  }
}

// ── Tertiary: ghost text ───────────────────────
.ub--tertiary {
  background: transparent;
  color: rgba(255, 255, 255, 0.55);
  border: 1px solid transparent;
  padding-left: 0.75rem;
  padding-right: 0.75rem;

  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
  }
}

// ── Contrast / Contrast-2: amarillo UNET ──────
.ub--contrast,
.ub--contrast-2 {
  background: var(--main-yellow, #FFEF3D);
  color: #1a1d24;
  border: 1px solid transparent;
  box-shadow: 0 1px 2px rgba(255, 239, 61, 0.1);

  &:hover:not(:disabled) {
    background: #fbe624;
    box-shadow: 0 4px 12px rgba(255, 239, 61, 0.2);
  }
}

// ── Blue ───────────────────────────────────────
.ub--blue {
  background: var(--main-blue, #4285F4);
  color: #fff;
  border: 1px solid transparent;
  box-shadow: 0 1px 2px rgba(66, 133, 244, 0.15);

  &:hover:not(:disabled) {
    background: #3376e4;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.25);
  }
}

// ── Danger ─────────────────────────────────────
.ub--danger {
  background: var(--main-red, #D33124);
  color: #fff;
  border: 1px solid transparent;
  box-shadow: 0 1px 2px rgba(211, 49, 36, 0.15);

  &:hover:not(:disabled) {
    background: #c2291d;
    box-shadow: 0 4px 12px rgba(211, 49, 36, 0.25);
  }
}

// ── Deactivated ────────────────────────────────
.ub--deactivated {
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
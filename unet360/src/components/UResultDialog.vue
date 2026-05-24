<template>
  <UBaseModal :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)" size="sm">
    <div class="result-dialog" :class="{ 'success-theme': success, 'error-theme': !success }">
      
      <!-- Premium interactive SVG animations -->
      <div class="icon-container">
        <div class="icon-glow-backdrop"></div>
        <svg v-if="success" class="success-checkmark animate-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
          <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
          <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
        </svg>
        <svg v-else class="error-cross animate-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
          <circle class="cross-circle" cx="26" cy="26" r="25" fill="none"/>
          <path class="cross-line-1" fill="none" d="M16 16 36 36"/>
          <path class="cross-line-2" fill="none" d="M36 16 16 36"/>
        </svg>
      </div>

      <!-- Text Content -->
      <div class="text-container">
        <h3 class="result-title">{{ title }}</h3>
        <p class="result-message">{{ message }}</p>
      </div>

      <!-- Action Buttons -->
      <div class="actions-container">
        <slot name="actions">
          <UButton 
            v-if="secondaryBtnText" 
            :text="secondaryBtnText" 
            type="tertiary" 
            @click="emit('secondary-click')" 
          />
          <UButton 
            v-if="primaryBtnText" 
            :text="primaryBtnText" 
            type="contrast-2" 
            @click="emit('primary-click')" 
          />
        </slot>
      </div>
      
    </div>
  </UBaseModal>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import UBaseModal from './UBaseModal.vue';
import UButton from './UButton.vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  success: {
    type: Boolean,
    default: true
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  primaryBtnText: {
    type: String,
    default: ''
  },
  secondaryBtnText: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'primary-click', 'secondary-click']);
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

.result-dialog {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.5rem;
  padding: 0.5rem 0;
}

.icon-container {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

// Background glow effect behind the icon
.icon-glow-backdrop {
  position: absolute;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  filter: blur(25px);
  opacity: 0.25;
  transition: all 0.4s ease;
  z-index: 1;
}

.success-theme .icon-glow-backdrop {
  background: #10B981;
  box-shadow: 0 0 40px rgba(16, 185, 129, 0.4);
}

.error-theme .icon-glow-backdrop {
  background: #EF4444;
  box-shadow: 0 0 40px rgba(239, 68, 68, 0.4);
}

.animate-svg {
  position: relative;
  z-index: 2;
  width: 80px;
  height: 80px;
  display: block;
}

.checkmark-circle, .cross-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2.5;
  stroke-miterlimit: 10;
  fill: none;
  animation: draw-circle 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-circle {
  stroke: #10B981;
}

.cross-circle {
  stroke: #EF4444;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  stroke-width: 3.5;
  stroke: #10B981;
  stroke-linecap: round;
  animation: draw-stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.5s forwards;
}

.cross-line-1, .cross-line-2 {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  stroke-width: 3.5;
  stroke: #EF4444;
  stroke-linecap: round;
}

.cross-line-1 {
  animation: draw-stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.4s forwards;
}

.cross-line-2 {
  animation: draw-stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.6s forwards;
}

@keyframes draw-circle {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes draw-stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

/* Text Styles */
.text-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 90%;
}

.result-title {
  @include paragraph-contrast;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--full-white);
  margin: 0;
  letter-spacing: -0.02rem;
}

.result-message {
  @include paragraph-small;
  color: rgba(255, 255, 255, 0.65);
  margin: 0;
  line-height: 1.45;
}

/* Actions Styles */
.actions-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  width: 100%;
  margin-top: 0.5rem;
  flex-wrap: wrap;

  :deep(.button) {
    min-width: 130px;
    justify-content: center;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  }

  // A subtle glow on the active confirmation button
  .success-theme :deep(.button-contrast-2) {
    box-shadow: 0 4px 15px rgba(255, 239, 61, 0.2);
    &:hover {
      box-shadow: 0 6px 20px rgba(255, 239, 61, 0.35);
      transform: translateY(-1px);
    }
  }

  .error-theme :deep(.button-contrast-2) {
    box-shadow: 0 4px 15px rgba(255, 239, 61, 0.2);
    &:hover {
      box-shadow: 0 6px 20px rgba(255, 239, 61, 0.35);
      transform: translateY(-1px);
    }
  }

  @media (max-width: 480px) {
    flex-direction: column-reverse;
    gap: 0.75rem;

    :deep(.button) {
      width: 100%;
    }
  }
}
</style>

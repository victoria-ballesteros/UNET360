<template>
  <button :class="`button button-${type}`" @click="handleClick" type="button">
    <UIcon
      v-if="props.icon"
      :name="props.icon"
      size="24"
      :color="props.iconColor"
    />
    <span v-if="props.text">{{ props.text }}</span>
  </button>
</template>

<script setup>
import UIcon from "./UIcon.vue";

const props = defineProps({
  type: {
    type: String,
    default: "default",
  },
  text: {
    type: String,
    required: false,
  },
  icon: {
    type: String,
    required: false,
  },
  iconColor: {
    type: String,
    required: false,
  },
});

const emit = defineEmits(["click"]);

const handleClick = (event) => {
  emit("click", event);
};
</script>

<style scoped lang="scss">
.button {
  padding: 0.625rem 1.875rem;
  border: none;
  cursor: pointer;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  position: relative;
  overflow: hidden;

  @include paragraph-small;

  transition:
    box-shadow 0.2s ease,
    background-color 0.2s ease,
    color 0.2s ease,
    outline-color 0.2s ease,
    outline-offset 0.2s ease,
    filter 0.2s ease;

  &:active {
    transform: scale(0.97);
    transition-duration: 0.08s;
  }

  // Shine sweep layer — used by contrast + blue
  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    opacity: 0;
    transition: opacity 0.2s ease, background-position 0.5s ease;
    background: linear-gradient(
      105deg,
      transparent 40%,
      rgba(255, 255, 255, 0.38) 50%,
      transparent 60%
    );
    background-size: 200% 100%;
    background-position: 200% 0;
    pointer-events: none;
  }
}

// Primary — darkens on hover
.button-primary {
  background: var(--strong-gray);
  color: var(--fill-white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

  &:hover {
    filter: brightness(1.18);
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.32);
  }
}

// Secondary — border materialises, background lifts to white
.button-secondary {
  background: var(--fill-gray);
  color: var(--strong-gray);
  box-shadow: none;
  outline: 1.5px solid transparent;
  outline-offset: 0;

  &:hover {
    background: var(--fill-white);
    outline-color: var(--strong-gray);
  }
}

// Tertiary — inverts: white → dark, dark text → white
.button-tertiary {
  background: var(--fill-white);
  color: var(--strong-gray);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  &:hover {
    background: var(--strong-gray);
    color: var(--fill-white);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
  }
}

// Contrast / Contrast-2 — shine sweep across the yellow CTA
.button-contrast,
.button-contrast-2 {
  background-color: var(--main-yellow);
  color: var(--strong-gray);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);

  &:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
    filter: brightness(1.06);

    &::after {
      opacity: 1;
      background-position: -200% 0;
    }
  }
}

.button-contrast {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 1.875rem;

  span {
    @include paragraph-contrast;
  }
}

// Blue — brightens + glow intensifies
.button-blue {
  background: var(--main-blue);
  color: var(--fill-white);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);

  &:hover {
    filter: brightness(1.14);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.24);

    &::after {
      opacity: 1;
      background-position: -200% 0;
    }
  }
}

// Danger — outline pulse, no movement
.button-danger {
  background: var(--main-red);
  color: var(--fill-white);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);
  outline: 2px solid transparent;
  outline-offset: 0;

  &:hover {
    filter: brightness(1.1);
    outline-color: var(--main-red);
    outline-offset: 3px;
  }
}

// Deactivated
.button-deactivated {
  background: var(--border-gray);
  color: var(--fill-white);
  pointer-events: none;
  box-shadow: none;
  opacity: 0.55;
}
</style>
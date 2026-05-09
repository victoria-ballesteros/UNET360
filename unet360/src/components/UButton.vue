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
  // Valores base (Desktop)
  padding: 0.625rem 1.875rem;
  gap: 0.375rem;
  border: none;
  cursor: pointer;
  border-radius: 12px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  transition: all 0.2s ease;

  @include paragraph-small;

  @media (max-width: 1024px) {
    padding: 0.5rem 1.5rem;
    font-size: 0.9rem;
    gap: 0.25rem;
  }

  @media (max-width: 768px) {
    padding: 0.4rem 1.2rem;
    font-size: 0.8rem;
    border-radius: 10px;
    gap: 0.2rem;
  }

  &:active {
    transform: scale(0.97);
    transition-duration: 0.08s;
  }

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

.button-contrast {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 1.875rem; // Base

  @media (max-width: 768px) {
    padding: 0.75rem 1.4rem;
  }

  span {
    @include paragraph-contrast;
    @media (max-width: 768px) {
      font-size: 0.85rem;
    }
  }
}

.button-primary {
  background: var(--strong-gray);
  color: var(--fill-white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  &:hover { filter: brightness(1.18); box-shadow: 0 4px 18px rgba(0, 0, 0, 0.32); }
}

.button-secondary {
  background: var(--fill-gray);
  color: var(--strong-gray);
  outline: 1.5px solid transparent;
  &:hover { background: var(--fill-white); outline-color: var(--strong-gray); }
}

.button-tertiary {
  background: var(--fill-white);
  color: var(--strong-gray);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  &:hover { background: var(--strong-gray); color: var(--fill-white); }
}

.button-contrast, .button-contrast-2 {
  background-color: var(--main-yellow);
  color: var(--strong-gray);
  &:hover {
    filter: brightness(1.06);
    &::after { opacity: 1; background-position: -200% 0; }
  }
}

.button-blue {
  background: var(--main-blue);
  color: var(--fill-white);
  &:hover {
    filter: brightness(1.14);
    &::after { opacity: 1; background-position: -200% 0; }
  }
}

.button-danger {
  background: var(--main-red);
  color: var(--fill-white);
  outline: 2px solid transparent;
  &:hover { filter: brightness(1.1); outline-color: var(--main-red); outline-offset: 3px; }
}

.button-deactivated {
  background: var(--border-gray);
  color: var(--fill-white);
  pointer-events: none;
  opacity: 0.55;
}
</style>
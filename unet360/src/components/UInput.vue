<template>
  <div :class="`input-wrapper input-wrapper-${type}`">
    <input
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      :class="`input input-${type}`"
      type="text"
    />
    <UIcon
      v-if="icon"
      :name="icon"
      :size="20"
      :color="iconColor"
      class="input-icon"
    />
  </div>
</template>

<script setup>
import UIcon from './UIcon.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'default',
  },
  placeholder: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    required: false,
  },
  iconColor: {
    type: String,
    required: false,
    default: 'currentColor'
  }
})

const emit = defineEmits(['update:modelValue'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped lang="scss">
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0.9375rem 1rem;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.input {
  border: none;
  background: transparent;
  outline: none;
  font-family: inherit;
  font-size: 1rem;
  flex-grow: 1;
  color: inherit;
  padding-right: 2.5rem;
}

.input-icon {
  position: absolute;
  right: 1rem;
  pointer-events: none;
  top: 50%;
  transform: translateY(-50%);
}

.input-default {
  font-weight: 500;
  color: var(--white);
  &::placeholder {
    color: var(--white);
    opacity: 0.7;
  }
}

.input-secondary {
  font-weight: 500;
  color: var(--gray70);
  &::placeholder {
    color: var(--gray70);
    opacity: 0.7;
  }
}
</style>

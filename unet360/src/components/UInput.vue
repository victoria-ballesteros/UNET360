<template>
  <div
    :class="[
      `input-wrapper input-wrapper-${styleType}`,
      { 'has-value': modelValue.length > 0 },
      { 'is-disabled': props.disabled }
    ]"
  >
    <input
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      :class="`input input-${styleType}`"
      :type="type"
      :step="step"
      :disabled="disabled"
      :inputMode="inputMode"
      :pattern="pattern"
    />
    <UIcon
      v-if="icon"
      :name="props.icon"
      :size="16"
      :color="props.iconColor"
      :rotation="props.iconRotation"
      @click="emitIconClick"
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
  styleType: {
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
  },
  iconRotation: {
    type: Number,
    default: 0
  },
  disabled: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'text'
  },
  step: {
    type: Number,
    default: 1
  },
  inputMode: {
    type: String,
    default: 'text'
  },
  pattern: {
    type: String,
    default: '\\d+'
  }
})

const emit = defineEmits(['update:modelValue', 'icon-click'])

const handleInput = (event) => {
  let value = event.target.value

  if (props.pattern === '[0-9]*' || props.pattern === '[0-9.]*') {
    let cleaned = value.replace(/[^0-9.]/g, '')
    const parts = cleaned.split('.')
    if (parts.length > 2) {
      cleaned = parts[0] + '.' + parts.slice(1).join('')
    }
    event.target.value = cleaned
    value = cleaned
  }

  emit('update:modelValue', event.target.value)
}

const emitIconClick = () => {
  emit('icon-click');
};
</script>

<style scoped lang="scss">
.input-wrapper {
  background: var(--fill-gray);
  border-radius: 12px;
  padding: 0.938rem 1rem;
  display: flex;
  align-items: center;
  position: relative;

  .input {
    border: none;
    background: transparent;
    outline: none;
    @include paragraph-small;
    flex: 1;
    min-width: 0;

    &::placeholder {
      color: var(--border-gray);
      opacity: 1;
    }
  }
}
.input-wrapper.has-value {
  .input {
    color: var(--strong-gray);
  }
}

.input-wrapper.is-disabled {
  background: var(--fill-gray);
  pointer-events: none;

  .input {
    color: var(--border-gray);
    pointer-events: none;
  }

  svg {
    color: var(--border-gray);
  }
}
</style>

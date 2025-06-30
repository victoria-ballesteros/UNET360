<template>
  <div
    :class="[
      `input-wrapper input-wrapper-${type}`,
      { 'has-value': modelValue.length > 0 }
    ]"
  >
    <input
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      :class="`input input-${type}`"
      type="text"
    />
    <UIcon
      v-if="icon"
      :name="props.icon"
      :size="16"
      :color="props.iconColor"
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
  background: var(--fill-gray);
  border-radius: 12px;
  padding: 0.938rem 1rem;
  display: flex;
  align-items: center;
  position: relative;
  width: 21.563rem;

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
</style>
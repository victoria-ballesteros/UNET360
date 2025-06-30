<template>
  <button 
    :class="`button button-${type}`"
    @click="handleClick"
  >
    <UIcon v-if="props.icon" :name="props.icon" size="16" :color="props.iconColor" />
    <span v-if="props.text">{{ props.text }}</span>
  </button> 
</template>

<script setup>
import UIcon from './UIcon.vue';

const props = defineProps({
  type: {
    type: String,
    default: 'default',
  },
  text: {
    type: String,
    required: false,
  },
  icon: {
    type: String,
    required: false,
  },
  iconColor : {
    type: String,
    required: false,
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  emit('click', props.type)
}

</script>

<style scoped lang="scss">
.button {
  padding: 0.625rem 1.875rem;
  border: none;
  cursor: pointer;
  border-radius: 12px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  display: flex;
  align-items: center;
  gap: 0.375rem;
  @include paragraph-small;

  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  }

  &:active {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
}

.button-primary {
  background: var(--strong-gray);
  color: var(--fill-white);
}

.button-secondary {
  background: var(--fill-gray);
  color: var(--strong-gray);
}

.button-tertiary {
  background: var(--fill-white);
  color: var(--strong-gray);
}

.button-deactivated {
  background: var(--border-gray);
  color: var(--fill-white);
  pointer-events: none;
  box-shadow: none;
}

</style>
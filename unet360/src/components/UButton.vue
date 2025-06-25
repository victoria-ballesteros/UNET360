<template>
  <button 
    :class="`button button-${type}`"
    @click="handleClick"
  >
    <UIcon v-if="props.icon" :name="props.icon" size="24" :color="props.iconColor" />
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
  padding: 0.9375rem 5rem;
  border: none;
  cursor: pointer;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.button-default {
  font-weight: 500 !important;
  background: var(--gray70);
  color: var(--white);
}

.button-secondary {
  font-weight: 500 !important;
  background: var(--gray30);
  color: var(--gray70);
}

.button-deactivated {
  font-weight: 500 !important;
  background: var(--gray50);
  color: var(--gray30);
  pointer-events: none;
}

</style>
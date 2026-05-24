<template>
  <!-- Thin wrapper de UBaseModal — mantenido por retrocompatibilidad -->
  <UBaseModal
    :model-value="modelValue"
    :title="headerTitle?.trim() ? headerTitle : ''"
    :closable="true"
    size="md"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <slot />
  </UBaseModal>
</template>

<script setup>
import UBaseModal from './UBaseModal.vue';

defineProps({
  modelValue:  { type: Boolean, default: false },
  headerTitle: { type: String,  default: '' },
});
const emit = defineEmits(['update:modelValue']);
</script>
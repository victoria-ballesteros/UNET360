<template>
  <component
    :is="IconComponent"
    v-if="IconComponent"
    :width="size"
    :height="size"
    :fill="color"
    :style="{
      transform: `rotate(${props.rotation}deg)`,
    }"
  />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [Number, String],
    default: 24
  },
  color: {
    type: String,
    default: 'currentColor'
  },
  rotation: {
    type: Number,
    default: 0
  }
})

const icons = import.meta.glob('@/assets/icons/*.svg', { eager: true, import: 'default' })

const IconComponent = computed(() => {
  const path = `/src/assets/icons/${props.name}.svg`
  return icons[path] || null
})
</script>

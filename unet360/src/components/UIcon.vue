<template>
  <component
    :is="IconComponent"
    v-if="IconComponent"
    :height="size"
    :fill="color"
    :style="{
      transform: `rotate(${props.rotation}deg)`,
    }"
  />
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  size: {
    type: [Number, String],
  },
  color: {
    type: String,
    default: "currentColor",
  },
  rotation: {
    type: Number,
    default: 0,
  },
});

const icons = import.meta.glob("@/assets/*/*.svg", {
  eager: true,
  import: "default",
});

const IconComponent = computed(() => {
  const path = `/src/assets/${props.name}.svg`;
  return icons[path] || null;
});
</script>

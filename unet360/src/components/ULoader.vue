<template>
  <div class="loading-bar-container" :style="containerStyles">
    <div class="loading-bar" :style="barStyles" />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  width: {
    type: [String, Number],
    default: '25%'
  },
  height: {
    type: Number,
    default: 3
  }
});

const containerStyles = computed(() => {
  return {
    width: '100%',
    height: `${props.height + 4}px`
  };
});

const barStyles = computed(() => {
  const w = typeof props.width === 'number' ? `${props.width}px` : props.width;
  return {
    width: w,
    height: `${props.height}px`
  };
});
</script>

<style scoped>
.loading-bar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background: transparent;
}

.loading-bar {
  background: linear-gradient(to right,
    transparent 0%,
    var(--main-blue) 25%,
    #0056b3 50%,
    var(--main-blue) 75%,
    transparent 100%);
  background-size: 200% 100%;
  animation: loading 1.2s infinite ease-in-out;
  border-radius: 2px;
}

@keyframes loading {
  0%   { background-position: -100% 0; }
  100% { background-position: 100% 0; }
}
</style>
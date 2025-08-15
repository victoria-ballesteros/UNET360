<template>
  <div v-if="visible" class="toast">
    {{ message }}
  </div>
</template>

<script setup>
import { ref } from "vue";

const visible = ref(false);
const message = ref("");

function showToast(text, duration = 5000) {
  message.value = text;
  visible.value = true;

  setTimeout(() => {
    visible.value = false;
  }, duration);
}

defineExpose({ showToast });
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #333;
  color: white;
  padding: 10px 15px;
  border-radius: 6px;
  box-shadow: 0px 2px 8px rgba(0,0,0,0.2);
  animation: fadeInOut 3s forwards;
  z-index: 9999;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; }
  100% { opacity: 0; transform: translateY(20px); }
}
</style>

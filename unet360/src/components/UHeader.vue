<template>
  <header class="header-container">
    <UIcon name="icons/logo" size="43" />
    <UIcon
      name="icons/list"
      size="30"
      color="var(--fill-white)"
      @click="emit('isPanelOpen', event)"
    />
  </header>
</template>

<script setup>
import UIcon from "@/components/UIcon.vue";
const emit = defineEmits(["isPanelOpen"]);
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 10;
  padding: 0px 0px 0px 0px;
}
</style>

<template>
  <header class="header-container">
    <RouterLink :to="{ name: 'Home' }">
      <UIcon
        name="icons/logo"
        size="43"
        class="cursor-pointer"
      />
    </RouterLink>
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
import { RouterLink } from "vue-router";

const emit = defineEmits(["isPanelOpen"]);
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 10;
  padding: 0rem 1.125rem;
}
</style>

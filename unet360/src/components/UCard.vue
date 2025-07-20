<template>
  <div class="card-container">
    <UIcon :name="icon" size="40" color="var(--main-yellow)" />
    <p>{{ text }}</p>
  </div>
</template>

<script setup>
import UIcon from "@/components/UIcon.vue";

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    default: "icons/camera",
  },
});
</script>

<style scoped lang="scss">
.card-container {
  max-width: 100%;
  height: 100%;
  background: var(--main-blue);
  border-radius: 20px;
  padding: 1.875rem 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;

  p {
    @include paragraph-medium-light;
    margin: 0px;
    text-align: center;
    color: var(--full-white);
  }
}
</style>

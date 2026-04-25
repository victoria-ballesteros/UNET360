<template>
  <div class="home-upper-container">
    <div class="hero-section" ref="heroRef">
      <div class="hero-content">
        <div class="badge">Asistente Universitario</div>
        <h1 class="upper-paragraph">
          Tu guía inteligente para explorar la <span class="highlight">UNET</span> con un solo click.
        </h1>
        <p class="lower-paragraph">{{ generalInfo }}</p>
        <RouterLink :to="{ name: button.route }" class="no-underline-link">
          <UButton :text="button.label" type="contrast" />
        </RouterLink>
      </div>
      <div class="hero-visual">
        <div class="visual-ring ring-3"></div>
        <div class="visual-ring ring-2"></div>
        <div class="visual-ring ring-1"></div>
        <UIcon name="images/home-image" size="280" />
      </div>
    </div>

    <div class="card-wrapper">
      <div v-for="(item, index) in cardsInfo" :key="index" class="box">
        <UCard :text="item.text" :icon="item.icon" />
      </div>
    </div>
  </div>
</template>

<script setup>
import UIcon from "@/components/UIcon.vue";
import UButton from "@/components/UButton.vue";
import UCard from "@/components/UCard.vue";
import { ref, onMounted, onBeforeMount } from "vue";
import { getCardsInfo, getGeneralInfo, getButtonData } from "@/service/global_dialogs";
import { useAuthStore } from "@/service/stores/auth";

let authStore = null;

const cardsInfo = getCardsInfo();
const generalInfo = getGeneralInfo();
const isAuthenticated = ref(false);
const button = ref(null);
const heroRef = ref(null);

onBeforeMount(() => {
  authStore = useAuthStore();
  isAuthenticated.value = authStore.isAuthenticated;
  button.value = getButtonData(isAuthenticated.value);
});

onMounted(async () => {
  const headerHeightVar = getComputedStyle(document.documentElement).getPropertyValue("--header-height");
  const headerHeight = parseFloat(headerHeightVar) || 0;
  const fixedHeight = window.innerHeight - headerHeight;

  if (heroRef.value) {
    heroRef.value.style.minHeight = `${fixedHeight}px`;
  }
});
</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_home.scss";
</style>
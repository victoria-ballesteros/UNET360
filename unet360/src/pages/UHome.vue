<template>
  <div class="upper-container">
    <div class="hero-section" ref="heroRef">
      <p class="upper-paragrah">
        Tu guía inteligente para explorar la <b>UNET</b> con solo un clic.
      </p>
      <UIcon name="images/home-image" size="280" />
      <p class="lower-paragraph">{{ generalInfo }}</p>
      <RouterLink
        :to="{ name: 'Login' }"
        class="no-underline-link"
      >
        <UButton
          text="Empieza ahora"
          type="contrast"
        />
      </RouterLink>
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
import { ref, onMounted } from "vue";
import { getCardsInfo, getGeneralInfo, getButtonLabel } from "@/service/global_dialogs";
import { useAuthStore } from "@/service/stores/auth";

const cardsInfo = getCardsInfo();
const generalInfo = getGeneralInfo();
const authStore = useAuthStore();
const isAuthenticated = ref(false);
const buttonLabel = ref(null);

const heroRef = ref(null);

onMounted(async () => {
  isAuthenticated.value = authStore.isAuthenticated;
  buttonLabel.value = getButtonLabel(isAuthenticated.value);

  const headerHeightVar = getComputedStyle(
    document.documentElement
  ).getPropertyValue("--header-height");
  const headerHeight = parseFloat(headerHeightVar) || 0;
  const fixedHeight = window.innerHeight - headerHeight;

  if (heroRef.value) {
    heroRef.value.style.height = `${fixedHeight}px`;
  }
});
</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_home.scss";
</style>

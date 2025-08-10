<template>
  <div class="wrapper">
    <div class="upper-container">
      <UHeader v-if="route.name != 'Map'" @isPanelOpen="isPanelOpen = !isPanelOpen"
        class="provisional-header-container"></UHeader>
      <main class="content-container">
        <router-view />
      </main>
    </div>
    <footer v-if="route.name != 'NodeCreate' && route.name != 'Map'" class="footer-container">
      <p class="footer-description">© 2025 UNET360. All Rights Reserved.</p>
    </footer>
  </div>
  <USidebar :isOpen="isPanelOpen" @close="isPanelOpen = false">
    <template v-for="(option, index) in sidebarOptions" :key="index">
      <RouterLink v-if="option.to && !option.action" :to="option.to" class="nav-item" @click="isPanelOpen = false">
        {{ option.label }}
      </RouterLink>
      <button v-else-if="option.action === 'logout'" class="nav-item" @click="handleLogout">
        {{ option.label }}
      </button>
    </template>
  </USidebar>
</template>

<script setup>
import USidebar from "./components/USidebar.vue";
import UHeader from "./components/UHeader.vue";
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getSidebarOptions } from "./service/global_dialogs";
import { useAuthStore } from "@/service/stores/auth";
import { obtainData } from "./service/shared/utils";

const route = useRoute();
const router = useRouter();

const authStore = useAuthStore();

const headerHeight = ref(0);
const isPanelOpen = ref(false);
const sidebarOptions = computed(() => getSidebarOptions(authStore.isAuthenticated, authStore.user?.role));

function handleLogout() {
  console.log("Logout clicked");
  isPanelOpen.value = false;
  authStore.logout();
  router.push({ name: 'Login' });
}

onMounted(async () => {
  router.isReady().then(async () => {
    await obtainData();
  });

  const headerEl = document.querySelector(".header-container");
  if (headerEl) {
    headerHeight.value = headerEl.getBoundingClientRect().height;
  }

  document.documentElement.style.setProperty(
    "--header-height",
    `${headerHeight.value}px`
  );
});
</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_layout.scss";
</style>

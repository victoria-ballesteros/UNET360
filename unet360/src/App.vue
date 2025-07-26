<template>
  <div class="wrapper">
    <div class="upper-container">
      <UHeader @isPanelOpen="isPanelOpen = !isPanelOpen"></UHeader>
      <main class="content-container">
        <router-view />
      </main>
    </div>
    <footer v-if="route.name != 'NodeCreate'" class="footer-container">
      <p class="footer-description">© 2025 UNET360. All Rights Reserved.</p>
    </footer>
  </div>
  <USidebar :isOpen="isPanelOpen" @close="isPanelOpen = false">
    <template v-for="(option, index) in sidebarOptions" :key="index">
      <RouterLink
        v-if="option.to"
        :to="option.to"
        class="nav-item"
        @click="isPanelOpen = false"
      >
        {{ option.label }}
      </RouterLink>
      <button
        v-else-if="option.action === 'logout'"
        class="nav-item"
        @click="handleLogout"
      >
        {{ option.label }}
      </button>
    </template>
  </USidebar>
</template>

<script setup>
import USidebar from "./components/USidebar.vue";
import UHeader from "./components/UHeader.vue";
import { ref, onBeforeMount, onMounted, computed } from "vue";
import { useNodeStore } from "./service/stores/nodes.js";
import { useTagStore } from "./service/stores/tags.js";
import { useUserStore } from "./service/stores/user";
import { useRoute } from "vue-router";
import { getSidebarOptions } from "./service/global_dialogs";
import { useAuthStore } from "@/service/stores/auth";

const route = useRoute();

const nodeStore = useNodeStore();
const tagStore = useTagStore();
const userStore = useUserStore();
const authStore = useAuthStore();

const headerHeight = ref(0);
const isPanelOpen = ref(false);
const sidebarOptions = computed(() => getSidebarOptions(authStore.isAuthenticated, authStore.isAdmin));

function handleLogout() {
  isPanelOpen.value = false;
  authStore.logout();
}

onBeforeMount(async () => {
  if (userStore.authState == null || !userStore.authState) {
    await userStore.fetchUserState();
  }

  if (userStore.authState) {
    if (!nodeStore.nodes) {
      await nodeStore.fetchNodes();
    }

    if (!tagStore.tags) {
      await tagStore.fetchTags();
    }
  }
});

onMounted(async () => {
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

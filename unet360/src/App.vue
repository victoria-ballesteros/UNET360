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
    <RouterLink
      v-for="(option, index) in sidebarOptions"
      :key="index"
      :to="option.to"
      class="nav-item"
      @click="isPanelOpen = false"
    >
      {{ option.label }}
    </RouterLink>
  </USidebar>
</template>

<script setup>
import USidebar from "./components/USidebar.vue";
import UHeader from "./components/UHeader.vue";
import { ref, onBeforeMount, onMounted } from "vue";
import { useNodeStore } from "./service/stores/nodes.js";
import { useTagStore } from "./service/stores/tags.js";
import { useUserStore } from "./service/stores/user";
import { useRoute } from "vue-router";
import { getSidebarOptions } from "./service/global_dialogs";

const route = useRoute();

const nodeStore = useNodeStore();
const tagStore = useTagStore();
const userStore = useUserStore();

const headerHeight = ref(0);
const isPanelOpen = ref(false);
const sidebarOptions = ref(null);

onBeforeMount(async () => {
  if (userStore.authState == null) {
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

  sidebarOptions.value = getSidebarOptions(userStore.authState);

  // Para debugging:
  // console.log("Nodos disponibles: ", nodeStore.nodes);
  // console.log("Tags disponibles: ", tagStore.tags);
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

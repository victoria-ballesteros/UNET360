<template>
  <div class="wrapper">
    <div class="upper-container">
      <UHeader
        class="header-container"
        @isPanelOpen="isPanelOpen = !isPanelOpen"
      ></UHeader>
      <main class="content-container">
        <router-view />
      </main>
    </div>
    <footer v-if="route.name != 'NodeCreate'" class="footer-container">
      <p class="footer-description">© 2025 UNET360. All Rights Reserved.</p>
    </footer>
  </div>
  <USidebar :isOpen="isPanelOpen" @close="isPanelOpen = false">
    <div class="nav-item">Inicio</div>
    <div class="nav-item">Mapa</div>
    <div class="nav-item">Configuración</div>
  </USidebar>
</template>

<script setup>
import USidebar from "./components/USidebar.vue";
import UHeader from "./components/UHeader.vue";
import { ref, onBeforeMount, onMounted } from "vue";
import { useNodeStore } from "./service/stores/nodes.js";
import { useTagStore } from "./service/stores/tags.js";
import { useRoute } from "vue-router";

const route = useRoute();

const nodeStore = useNodeStore();
const tagStore = useTagStore();

const headerHeight = ref(0);

const isPanelOpen = ref(false);

onBeforeMount(async () => {
  await nodeStore.fetchNodes();
  await tagStore.fetchTags();
  // console.log("Nodos disponibles: ", nodeStore.nodes);
  // console.log("Tags disponibles: ", tagStore.tags)
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
.wrapper {
  // height: 100lvh;
  min-height: 100lvh;
  // max-height: 100lvh;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;

  background: var(--main-blue);

  .upper-container {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    flex-grow: 1;

    padding: 0px 10px;

    .header-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 10;
      padding: 24px 0px 0px 0px;
    }

    .content-container {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
    }
  }

  .footer-container {
    display: flex;
    align-items: center;
    justify-content: end;
    background: var(--strong-gray);
    padding: 14px 16px;
    .footer-description {
      @include paragraph-extra-small;
      color: var(--full-white);
    }
  }
}
</style>

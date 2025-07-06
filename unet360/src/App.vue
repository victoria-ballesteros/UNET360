<template>
  <div class="wrapper">
    <header class="header-container">
      <UIcon name="logo" size="41" />
      <UIcon name="list" size="30" color="var(--fill-white)" />
    </header>
    <main class="content-container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import UIcon from '@/components/UIcon.vue';
import { onBeforeMount } from 'vue';
import { useNodeStore } from './service/stores/nodes.js'
import { useTagStore } from './service/stores/tags.js';

const nodeStore = useNodeStore()
const tagStore = useTagStore()

onBeforeMount(async () => {
  await nodeStore.fetchNodes()
  await tagStore.fetchTags()
  // console.log("Nodos disponibles: ", nodeStore.nodes)
  // console.log("Tags disponibles: ", tagStore.tags)
})

</script>

<style scoped lang="scss">
.wrapper {
  height: 100lvh;
  min-height: 100lvh;
  max-height: 100lvh;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;

  background: linear-gradient(to bottom, var(--main-blue), var(--strong-gray));
  padding: 24px 10px 0px 10px;

  .header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
    margin-bottom: 1rem;
  }

  .content-container {
    flex-grow: 1;
    display: flex;
    flex-direction: column;

    min-height: 0;
  }
}
</style>
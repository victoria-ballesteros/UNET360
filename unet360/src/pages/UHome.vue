<template>
  <div class="upper-container">
    <div class="hero-section" ref="heroRef">
      <p class="upper-paragrah">
        Tu guía inteligente para explorar la <b>UNET</b> con solo un clic.
      </p>
      <UIcon name="images/home-image" size="280" />
      <p class="lower-paragraph">{{ generalInfo }}</p>
      <UButton
        text="Empieza ahora"
        @click="handleButtonClick"
        type="contrast"
      />
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

const cardsInfo = [
  {
    text: "Encuentra aulas, baños o servicios en segundos",
    icon: "icons/binoculars",
  },
  {
    text: "Explora el campus como si estuvieras allí",
    icon: "icons/aperture",
  },
  {
    text: "Llega rápido con señalamiento paso a paso",
    icon: "icons/route",
  },
];

const generalInfo =
  "Navega el campus con mapas 360°, rutas personalizadas y búsqueda inteligente. Olvídate de perderte y disfruta de una experiencia universitaria fluida.";

// Para mantener constante el tamaño de la sección hero

const heroRef = ref(null);

onMounted(() => {
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
.upper-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0.6rem 1.125rem !important;
}

.hero-section {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: calc(100dvh - var(--header-height));
  box-sizing: border-box;
  padding: 0rem 0rem 3.5rem 0rem;

  .upper-paragrah {
    @include paragraph-h1;
    color: var(--full-white);
    margin: 0rem 0rem 1rem 0rem !important;
    b {
      color: var(--main-blue);
    }
  }

  .lower-paragraph {
    @include paragraph-medium-light;
    color: var(--full-white);
    text-align: center;
  }
}
.card-wrapper {
  max-width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.box {
  display: flex;
  flex-direction: column;
}

.box:nth-child(3) {
  grid-column: span 2;
}
</style>

<template>
    <div class="showcase-container">
        <div class="showcase-header">
            Showcase
        </div>
        <div class="showcase-subcontainer">
            <UButton text='Default' @click="handleButtonClick" type="default" />
            <UButton text='Icon' @click="handleButtonClick" type="secondary" icon="cloud-upload" />
            <UButton text='Deactivated' @click="handleButtonClick" type="deactivated" />
        </div>
        <div class="showcase-subcontainer">
            <UInput
                v-model="inputValue"
                type="secondary"
                placeholder="Escribe algo..."
                icon="search"
                iconColor="#666"
            />
            <p>Valor actual: {{ inputValue }}</p>
        </div>
    </div>
</template>

<script setup>
import UButton from '@/components/UButton.vue'
import UInput from '@/components/UInput.vue'

import { ref } from 'vue'

// Button showcase functions
const handleButtonClick = (type) => {
    console.log(`${type} button clickeado.`)
};

// Input showcase functions
const inputValue = ref('')

</script>

<style scoped lang="scss">
.showcase-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;

    .showcase-header {
        padding: 1rem;
    }

    .showcase-subcontainer {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }
}
</style>
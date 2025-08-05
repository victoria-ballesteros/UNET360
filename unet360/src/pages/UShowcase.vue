<template>
    <div class="showcase-header">
        Showcase
    </div>
    <div class="showcase-container">
        <div class="showcase-subcontainer">
            <p class="showcase-subcontainer-header"> UI buttons</p>
            <UButton text='Primary' @click="handleButtonClick" type="primary" />
            <UButton text='Secondary' @click="handleButtonClick" type="secondary" icon="icons/cloud-upload" />
            <UButton text='Tertiary' @click="handleButtonClick" type="tertiary" />
            <UButton text='Deactivated' @click="handleButtonClick" type="deactivated" />
        </div>
        <div class="showcase-subcontainer">
            <p class="showcase-subcontainer-header"> UI inputs</p>
            <UInput
                v-model="textInput"
                type="default"
                placeholder="Input"
                icon="icons/arrow-up"
            />
            <UInput
                v-model="textInputNoIcon"
                type="default"
                placeholder="Input"
            />
        </div>
        <div class="showcase-subcontainer">
            <p class="showcase-subcontainer-header"> UI imagotypes</p>
            <div class="showcase-group">
                <UIcon name="icons/arrow-up" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/arrow-up" size="32" color="var(--strong-gray)" :rotation="90" />
                <UIcon name="icons/arrow-up" size="32" color="var(--strong-gray)" :rotation="180" />
                <UIcon name="icons/arrow-up" size="32" color="var(--strong-gray)" :rotation="-90" />
            </div>
            <div class="showcase-group">
                <UIcon name="icons/cloud-upload" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/pc-display" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/person-standing" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/person-standing-dress" size="32" color="var(--strong-gray)" />
            </div>
            <div class="showcase-group">
                <UIcon name="icons/journal-text" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/arrow-bar-up" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/caret-up-fill" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/chevron-down" size="32" color="var(--strong-gray)" />
            </div>
            <div class="showcase-group">
                <UIcon name="icons/geo-alt-fill" size="32" color="var(--strong-gray)" />
                <UIcon name="icons/x-lg" size="32" color="var(--strong-gray)" />
            </div>
        </div>
    </div>
</template>

<script setup>
import UButton from '@/components/UButton.vue'
import UInput from '@/components/UInput.vue'
import UIcon from '@/components/UIcon.vue';

import { ref, watch } from 'vue'

// Button showcase functions
const handleButtonClick = (type) => {
    console.log(`${type} button clickeado.`)
};

// Input showcase functions
const textInput = ref('')
const textInputNoIcon = ref('')

watch(textInput, (newValue) => {
  console.log('textInput:', newValue)
})

watch(textInputNoIcon, (newValue) => {
  console.log('textInputNoIcon:', newValue)
})

</script>

<style scoped lang="scss">
.showcase-header {
    @include section-title;
    color: var(--strong-gray);
}

.showcase-container {
    display: flex;
    justify-content: start;
    align-items: start;
    margin: 1.25rem;
    gap: 4rem;

    .showcase-subcontainer {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 1rem;

        .showcase-subcontainer-header {
            @include paragraph-medium;
            color: var(--strong-gray);
        }

        .showcase-group {
            display: flex;
            gap: 1rem;
        }
    }
}
</style>
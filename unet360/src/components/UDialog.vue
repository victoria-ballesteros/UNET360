<template>
    <transition name="fade">
    <div v-if="modelValue" class="dialog-backdrop" @click.self="close">
            <div class="dialog-content">
                <div class="dialog-header" v-if="headerTitle">
                    <p class="header-title">{{ headerTitle }}</p>
            <UIcon @click="close" name="x-lg" size="16" color="var(--strong-gray)" />
                </div>
                <slot />
            </div>
        </div>
    </transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import UIcon from './UIcon.vue'

const props = defineProps({
    modelValue: Boolean,
    headerTitle: {
        type: String,
        default: 'Formulario'
    }
})
const emit = defineEmits(['update:modelValue'])

function close() {
    emit('update:modelValue', false)
}
</script>

<style scoped lang="scss">
.dialog-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

.dialog-content {
    position: relative;
    background: var(--fill-white);
    padding: 2rem 1rem;
    border-radius: 8px;
    min-width: 80%;
    max-height: 90%;
    overflow-y: auto;

    .dialog-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        .header-title {
            @include paragraph-medium;
            color: var(--strong-gray);
            width: 100%;
        }
    }
}
</style>

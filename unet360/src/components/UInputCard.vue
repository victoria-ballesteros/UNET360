<template>
    <div class="menu-wrapper">
        <div class="search-wrapper">
            <UIcon v-if="!routeSearcherActive" name="icons/list" size="32" color="var(--fill-white)"
                :rotation=listIconRotation @click="toggleMenu" class="menu-toggle-icon" />
            <input v-model="searchText" type="text" class="search-input" :placeholder="searcherInputPlaceholder" />
            <UIcon v-if="!menuVisible" name="icons/route-arrow" size="32" color="var(--fill-white)"
                @click="toggleRouteSearcher" />
            <UIcon v-if="routeSearcherActive" name="icons/x-lg" size="26" color="var(--fill-white)"
                @click="toggleMenu" />
        </div>
        <div v-if="menuVisible" class="dropdown-menu-wrapper">
            <div v-if="!routeSearcherActive" class="dropdown-menu">
                <div v-for="[label, icon] in Object.entries(menuOptions)" :key="label" class="menu-item"
                    @click="toggleMenu(label)">
                    <UIcon :name="'icons/' + icon" size="20" color="var(--fill-white)" />
                    <span>{{ label }}</span>
                </div>
            </div>
            <div v-else class="route-searcher">
                <div class="route-icons-container">
                    <UIcon name="icons/dot-inside-dot" size="20" />
                    <div class="three-dots-container">
                        <span>•</span>
                        <span>•</span>
                        <span>•</span>
                    </div>
                    <UIcon name="icons/point-sign" size="20" />
                </div>
                <div class="route-inputs-container">
                    <input :value="searchSource" type="text" class="route-input" placeholder="Ingresa el origen"
                        @input="handleSource" />
                    <input :value="searchTarget" type="text" class="route-input" placeholder="Ingresa el destino"
                        @input="handleTarget" />
                </div>
                <UIcon name="icons/arrows-crossed" size="23" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import UIcon from './UIcon.vue'
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/service/stores/auth";

const props = defineProps({
    searchSource: {
        type: String,
        required: true
    },
    searchTarget: {
        type: String,
        required: true
    }
});

const emit = defineEmits(['update:searchSource', 'update:searchTarget'])

const handleSource = (event) => {
    emit('update:searchSource', event.target.value)
}

const handleTarget = (event) => {
    emit('update:searchTarget', event.target.value)
}

const router = useRouter();
const authStore = useAuthStore();

const menuVisible = ref(false)
const searchText = ref('')
const listIconRotation = ref(0)
const routeSearcherActive = ref(false)
const searcherInputPlaceholder = ref("Ej. Edificio A");

const menuOptions = {
    "Ruta": "route-arrow",
    "Inicio": "house",
    "Acerca de": "about",
    "Cerrar sesión": "close-session"
}

const menuRouter = {
    "Ruta": "route-arrow",
    "Inicio": "Home",
    "Acerca de": "About",
    "Cerrar sesión": "About"
}

function toggleMenu(label = null) {
    menuVisible.value = !menuVisible.value
    listIconRotation.value = menuVisible.value ? 90 : 0
    routeSearcherActive.value = false
    searcherInputPlaceholder.value = "Ej. Edificio A"

    if (label === "Ruta") {
        toggleRouteSearcher();
    } else if (label === "Cerrar sesión") {
        authStore.logout();
        router.push({ name: 'Login' });
    } else {
        const route = menuRouter?.[label];
        if (route != undefined) {
            router.push({ name: route });
        }
    }
}

function toggleRouteSearcher() {
    menuVisible.value = true
    routeSearcherActive.value = !routeSearcherActive.value
    searcherInputPlaceholder.value = "Ruta"
}

</script>

<style scoped lang="scss">
.menu-wrapper {
    position: relative;
    background-color: var(--strong-gray);
    border-radius: 0.75rem;
    width: 100%;
    color: var(--fill-white);
    border-radius: 24px !important;
}

.search-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    margin: 14px 1rem 14px 1rem;
}

.menu-toggle {
    background: transparent;
    border: none;
    cursor: pointer;
    margin-bottom: 0.5rem;
}

.search-input {
    all: unset;
    width: 100%;
    padding: 0.4rem 0.6rem;
    background-color: var(--strong-gray);
    @include paragraph-small();
    color: var(--fill-white);
}

.dropdown-menu-wrapper {
    border-top: 1px var(--main-blue) solid;
}

.dropdown-menu {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    animation: fadeIn 0.3s ease-out forwards;
    padding: 14px 62px 14px 62px;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.3rem 0.4rem;
    border-radius: 0.4rem;
    cursor: pointer;
    transition: background 0.2s;

    &:hover {
        background-color: #374151;
    }
}

.menu-toggle-icon {
    transition: transform 0.3s ease;
}

.route-searcher {
    display: flex;
    padding: 14px 48px 14px 48px;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
}

.route-icons-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
    flex-grow: 1;
}

.route-input {
    all: unset;
    width: 100%;
    padding: 0.5rem;
    background-color: var(--fill-gray);
    @include paragraph-small();
    border-radius: 12px;
    color: var(--strong-gray);
}

input::placeholder {
    color: var(--border-gray);
}

.route-inputs-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
    align-items: center;
}

.three-dots-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0px;
    font-size: 10px;
    font-weight: 900;
    line-height: 1;
    padding: 3px 0px 3px 0px;
}

.three-dots-container span {
    padding: 0;
    margin: 0;
    line-height: 1;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
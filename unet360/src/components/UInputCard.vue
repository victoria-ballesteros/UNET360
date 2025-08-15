<template>
    <div class="menu-wrapper">
        <div class="search-wrapper">
            <UIcon v-if="!routeSearcherActive" name="icons/list" size="32" color="var(--fill-white)"
                :rotation="listIconRotation" @click="toggleMenu" class="menu-toggle-icon" />
            <input :value="searchBar" type="text" class="search-input" :placeholder="searcherInputPlaceholder"
                @input="handleSearchBar" />
            <UIcon v-if="!menuVisible" name="icons/route-arrow" size="32" color="var(--fill-white)"
                @click="toggleRouteSearcher" />
            <UIcon v-if="routeSearcherActive" name="icons/x-lg" size="26" color="var(--fill-white)"
                @click="toggleMenu" />
        </div>

        <div v-if="menuVisible" class="dropdown-menu-wrapper">
            <div v-if="Object.keys(searchResults ?? {}).length > 0" class="dropdown-menu">
                <div v-for="[key, value] in Object.entries(searchResults)" :key="label" class="menu-item"
                    @click="handleSearchClick(value)">
                    <span>{{ key }}</span>
                </div>
            </div>
            <div v-else-if="!routeSearcherActive" class="dropdown-menu">
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
                        @input="handleSource" list="source-suggestions" />

                    <datalist id="source-suggestions">
                        <option v-for="(value, key) in routeSearcherResult" :key="key" :value="key">
                            {{ value }}
                        </option>
                    </datalist>

                    <input :value="searchTarget" type="text" class="route-input" placeholder="Ingresa el destino"
                        @input="handleTarget" list="source-suggestions-2" />

                    <datalist id="source-suggestions-2">
                        <option v-for="(value, key) in routeSearcherTargetResult" :key="key" :value="key">
                            {{ value }}
                        </option>
                    </datalist>
                </div>
                <UIcon name="icons/arrows-crossed" size="23" @click="searchPath" />
            </div>
        </div>
    </div>
    <UToast ref="toastRef" />
</template>

<script setup>
import { ref, watch } from 'vue'
import UIcon from './UIcon.vue'
import UToast from './UToast.vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/service/stores/auth";
import { searchNodeByKeyword } from '@/service/shared/utils';
import { fetchShortestPath } from '@/service/requests/graph';

const props = defineProps({
    searchSource: {
        type: String,
        required: true
    },
    searchTarget: {
        type: String,
        required: true
    },
    searchBar: {
        type: String,
        required: true
    },
    searchResults: {
        type: Object,
        required: false,
        default: () => ({})
    },
    actualRoute: {
        type: Object,
        required: true,
        default: () => ({})
    },
    actualNode: {
        type: Object,
        required: true,
        default: () => ({})
    }
});

const emit = defineEmits(['update:searchSource', 'update:searchTarget', 'update:searchBar', 'update:searchedNode', 'update:actualRoute'])

const handleSource = (event) => {
    emit('update:searchSource', event.target.value);
    routeSearcherResult.value = searchNodeByKeyword(event.target.value);
    routeSearcherResult.value["Posición actual"] = props.actualNode.name;
    routeSearcherResult.value = { ...routeSearcherResult.value };
    console.log(routeSearcherResult.value)
    sourceValue.value = event.target.value;
}

const handleTarget = (event) => {
    emit('update:searchTarget', event.target.value)
    routeSearcherTargetResult.value = searchNodeByKeyword(event.target.value);
    targetValue.value = event.target.value;
}

const handleSearchBar = (event) => {
    emit('update:searchBar', event.target.value)
}

const handleSearchClick = (value) => {
    emit('update:searchedNode', value)
}

const router = useRouter();
const authStore = useAuthStore();

const menuVisible = ref(false)
const listIconRotation = ref(0)
const routeSearcherActive = ref(false)
const searcherInputPlaceholder = ref("Ej. Edificio A");

const routeSearcherResult = ref({});
const routeSearcherTargetResult = ref({});

const sourceValue = ref(null);
const targetValue = ref(null);

const route = ref([]);
const toastRef = ref(null);

function notify() {
    toastRef.value.showToast("¡Error!: por favor asegúrate de que los puntos entre los que te vas a trasladar sean válidos.");
}

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

const searchPath = async () => {
    route.value = await fetchShortestPath(routeSearcherResult.value?.[sourceValue.value], routeSearcherTargetResult.value?.[targetValue.value])
    if (route.value.status == true && route.value.response_obj.total_weight != 0) {
        console.log("ROUTE: ", route.value.response_obj.path);
        console.log("WEIGHT: ", parseFloat(route.value.response_obj.total_weight) * 10);
        emit('update:actualRoute', { 'route': route.value.response_obj.path, 'weight': parseFloat(route.value.response_obj.total_weight) * 10 })
    } else {
        notify();
    }
}

watch(
    () => props.searchResults,
    (newVal, oldVal) => {
        if (newVal == null || newVal == {}) {
            menuVisible.value = false;
            return;
        } else if (Object.keys(newVal).length > 0) {
            menuVisible.value = true;
            return;
        }

        menuVisible.value = false;
    },
    { deep: true }
);

watch(
    () => props.searchBar,
    (newVal, oldVal) => {
        if (newVal.trim() !== '') {
            return;
        } else {
            menuVisible.value = false;
        }
    }
);

watch(
    () => props.actualNode,
    (newVal, oldVal) => {
        console.log("Name: ", props.actualNode.name);
    }
)

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

.autocomplete-list {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    max-height: 200px;
    overflow-y: auto;
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    z-index: 1000;
    list-style: none;
    margin: 0;
    padding: 0;
}

.autocomplete-list li {
    padding: 8px;
    cursor: pointer;
}

.autocomplete-list li:hover {
    background-color: #eee;
}
</style>
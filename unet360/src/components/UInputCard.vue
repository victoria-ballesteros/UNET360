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
    },
    searchedNode: {
        type: String,
        default: ""
    }
});

const emit = defineEmits(['update:searchSource', 'update:searchTarget', 'update:searchBar', 'update:searchedNode', 'update:actualRoute'])

const handleSource = (event) => {
    emit('update:searchSource', event.target.value);
    routeSearcherResult.value = searchNodeByKeyword(event.target.value);
    routeSearcherResult.value["Posición actual"] = props.actualNode.name;
    routeSearcherResult.value = { ...routeSearcherResult.value };
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

    if (label === null) {
        return;
    }

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
    (newVal, _) => {
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
    (newVal, _) => {
        if (newVal.trim() !== '') {
            return;
        } else {
            menuVisible.value = false;
        }
    }
);

</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_input_card.scss";
</style>
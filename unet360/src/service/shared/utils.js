import { useNodeStore } from "../stores/nodes.js";
import { useTagStore } from "../stores/tags.js";
import { useAuthStore } from "../stores/auth.js";

export async function obtainData() {
    const authStore = useAuthStore();
    const nodeStore = useNodeStore();
    const tagStore = useTagStore();

    if (authStore.isAuthenticated) {
        if (!nodeStore.nodes) {
            await nodeStore.fetchNodes();
            console.log(nodeStore.nodes)
        }
        if (!tagStore.tags) {
            await tagStore.fetchTags();
        }
    }
}

export async function obtainMockNodes() {
    return [
        {
            "name": "001",
            "location": null,
            "url_image": "https://uurpcauxzloqxdltglns.supabase.co/storage/v1/object/public/virtual-environment-images//01.PHOTOSPHERE.jpg",
            "adyacent_nodes": [
                { "002": 3 },
                { "003": 4 },
                {},
                {}
            ],
            "tags": [
                {
                    "Aula": ["15A", "14A"],
                    "Baño de damas": ["Baño oeste del A"]
                }
            ],
            "minimap": {
                "image": "map-A1.jpg",
                "x": 185,
                "y": 568
            }
        },
        {
            "name": "002",
            "location": null,
            "url_image": "https://uurpcauxzloqxdltglns.supabase.co/storage/v1/object/public/virtual-environment-images//21.PHOTOSPHERE.jpg",
            "adyacent_nodes": [
                {},
                { "001": 3 },
                {},
                {}
            ],
            "tags": [
                {
                    "Aula": ["15A", "14A"],
                    "Baño de damas": ["Baño oeste del A"]
                }
            ],
            "minimap": {
                "image": "map-A1.jpg",
                "x": 121,
                "y": 903
            }
        },
        {
            "name": "003",
            "location": null,
            "url_image": "https://uurpcauxzloqxdltglns.supabase.co/storage/v1/object/public/virtual-environment-images//25.PHOTOSPHERE.jpg",
            "adyacent_nodes": [
                {},
                {},
                {},
                { "001": 4 }
            ],
            "tags": [
                {
                    "Aula": ["15A", "14A"],
                    "Baño de damas": ["Baño oeste del A"]
                }
            ],
            "minimap": {
                "image": "campus-map.jpg",
                "x": 300,
                "y": 350
            }
        },
    ]
}

export function adjustAngle(anguloBase, lastDirection) {
    const directionOffsets = {
        Frente: 0,
        Derecha: Math.PI / 2,
        Atrás: Math.PI,
        Izquierda: -Math.PI / 2
    };

    const offset = directionOffsets[lastDirection] ?? 0;
    let nuevoAngulo = anguloBase + offset;

    if (nuevoAngulo > Math.PI) nuevoAngulo -= 2 * Math.PI;
    if (nuevoAngulo < -Math.PI) nuevoAngulo += 2 * Math.PI;

    return nuevoAngulo;
}

export function getImagePath(fileName) {
    return new URL(`../../assets/images/icons-images/${fileName}.png`, import.meta.url).href;
}

export function searchNodeByKeyword(keyword) {
    const nodeStore = useNodeStore();

    const keywords = keyword.trim().split(/\s+/);
    const lowerKeywords = keywords.map(k => k.toLowerCase());
    const searchableText = {};

    for (const node of nodeStore.nodes) {
        const nameText = node.name.toLowerCase();
        const locationText = node.location ? String(node.location).toLowerCase() : '';

        const matchesKeyword = lowerKeywords.some(kw => nameText.includes(kw) || locationText.includes(kw));

        if (matchesKeyword) {
            searchableText[node.location] = node.name ?? '';
        }

        if (Object.keys(node.tags).length > 0) {
            for (const [_, value] of Object.entries(node.tags)) {
                for (const [tagKey, _] of Object.entries(value)) {
                    const tagMatches = lowerKeywords.some(kw => tagKey.toLowerCase().includes(kw));

                    if (tagMatches) {
                        searchableText[tagKey] = node.name ?? '';
                    }
                }
            }
        }
    }

    return searchableText;
}
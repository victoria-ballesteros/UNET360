import { useNodeStore } from "../stores/nodes.js";
import { useTagStore } from "../stores/tags.js";
import { useAuthStore } from "../stores/auth.js";

export async function obtainData() {
    const authStore = useAuthStore();
    const nodeStore = useNodeStore();
    const tagStore = useTagStore();

    if (authStore.isAuthenticated) {
        console.log("Está autenticado")
        if (!nodeStore.nodes) {
            console.log("Busca nodos")
            await nodeStore.fetchNodes();
            console.log(nodeStore.nodes)
        }
        if (!tagStore.tags) {
            console.log("Busca tags")
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
                {
                    "002": 3, // Frente
                },
                {
                    "003": 4 // Derecha
                },
                {},          // Atrás
                {}           // Izquierda
            ],
            "tags": [
                {
                    "Aula": [
                        "15A",
                        "14A"
                    ],
                    "Baño de damas": [
                        "Baño oeste del A"
                    ]
                }
            ]
        },
        {
            "name": "002",
            "location": null,
            "url_image": "https://uurpcauxzloqxdltglns.supabase.co/storage/v1/object/public/virtual-environment-images//21.PHOTOSPHERE.jpg",
            "adyacent_nodes": [
                {},
                {
                    "001": 3
                },
                {},
                {}
            ],
            "tags": [
                {
                    "Aula": [
                        "15A",
                        "14A"
                    ],
                    "Baño de damas": [
                        "Baño oeste del A"
                    ]
                }
            ]
        },
        {
            "name": "003",
            "location": null,
            "url_image": "https://uurpcauxzloqxdltglns.supabase.co/storage/v1/object/public/virtual-environment-images//25.PHOTOSPHERE.jpg",
            "adyacent_nodes": [
                {},
                {},
                {},
                {
                    "001": 4
                }
            ],
            "tags": [
                {
                    "Aula": [
                        "15A",
                        "14A"
                    ],
                    "Baño de damas": [
                        "Baño oeste del A"
                    ]
                }
            ]
        },
    ]
}
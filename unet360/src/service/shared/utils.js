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

export function formatUserName(rawName = "") {
    const name = String(rawName).trim();
    if (!name) return "";
    if (name.includes("@")) return name;

    const parts = name.split('.').filter(Boolean);
    const formattedParts = parts.map(part => {
        const lower = part.trim().toLowerCase();
        return lower ? `${lower.charAt(0).toUpperCase()}${lower.slice(1)}` : "";
    }).filter(Boolean);

    return formattedParts.length ? formattedParts.join(' ') : name;
}

export function searchNodeByKeyword(keyword) {
    const nodeStore = useNodeStore();

    const keywords = keyword.trim().split(/\s+/).filter(k => k.toLowerCase() !== 'de' && k.toLowerCase() !== 'del');
    const lowerKeywords = keywords.map(k => k.toLowerCase());

    if (lowerKeywords.length === 0) {
        return {};
    }

    const matchesMap = new Map();

    for (const node of nodeStore.nodes) {
        const nameText = node.name.toLowerCase();
        const locationText = node.location ? String(node.location).toLowerCase() : '';

        const matchedKeywords = lowerKeywords.filter(kw => nameText.includes(kw) || locationText.includes(kw));

        if (matchedKeywords.length > 0) {
            const label = node.location || node.name;
            const lowerLabel = label.toLowerCase();
            
            // Calcular puntuación de relevancia basada en la cantidad de palabras coincidentes
            let score = 0;
            for (const kw of lowerKeywords) {
                if (lowerLabel.includes(kw)) {
                    score += 10;
                    if (lowerLabel === kw) score += 5;
                }
            }
            if (lowerLabel.startsWith(lowerKeywords[0])) {
                score += 5;
            }

            const existing = matchesMap.get(label);
            if (!existing || score > existing.score) {
                matchesMap.set(label, { nodeName: node.name, score });
            }
        }

        if (Object.keys(node.tags).length > 0) {
            for (const [_, value] of Object.entries(node.tags)) {
                for (const [tagKey, _] of Object.entries(value)) {
                    const tagText = tagKey.toLowerCase();
                    const tagMatchedKeywords = lowerKeywords.filter(kw => tagText.includes(kw));

                    if (tagMatchedKeywords.length > 0) {
                        let score = 0;
                        for (const kw of lowerKeywords) {
                            if (tagText.includes(kw)) {
                                score += 10;
                                if (tagText === kw) score += 5;
                            }
                        }
                        if (tagText.startsWith(lowerKeywords[0])) {
                            score += 5;
                        }

                        const existing = matchesMap.get(tagKey);
                        if (!existing || score > existing.score) {
                            matchesMap.set(tagKey, { nodeName: node.name, score });
                        }
                    }
                }
            }
        }
    }

    // Ordenar resultados por puntuación descendente, luego alfabéticamente
    const sortedEntries = Array.from(matchesMap.entries()).sort((a, b) => {
        if (b[1].score !== a[1].score) {
            return b[1].score - a[1].score;
        }
        return a[0].localeCompare(b[0]);
    });

    const result = {};
    for (const [label, data] of sortedEntries) {
        result[label] = data.nodeName;
    }

    return result;
}

export function generateRandomStartNode() {
    const nodes = ['074', '075', '076', '105', '106', '119', '059', '079', '054'];
    const randomIndex = Math.floor(Math.random() * nodes.length);
    return nodes[randomIndex];
}

export function formatFileSize(bytes) {
  if (!bytes) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
let streetViewData = [];

const Z1_URL = "{% static 'street_views/geojson/Z1.geojson' %}";
const Z2_URL = "{% static 'street_views/geojson/Z2.geojson' %}";
const Z3_URL = "{% static 'street_views/geojson/Z3.geojson' %}";
const Z4_URL = "{% static 'street_views/geojson/Z4.geojson' %}";
const Z5_URL = "{% static 'street_views/geojson/Z5.geojson' %}";

// Index du point dans le tableau 'streetViewData' qui est actuellement affiché
let currentIndex = 0;
// L'objet carte Leaflet
let map;
// Le marqueur spécial qui indique la position actuelle sur la carte
let currentMarker;
// VARIABLE GLOBALE pour le visualiseur Pannellum (360°)
let pannellumViewer = null;

// --- DÉFINITION DE LA PROJECTION CORRIGÉE (UTM zone 30N vers WGS84) ---
// Projection d'entrée (EPSG:32630 - WGS 84 / UTM zone 30N)
const UTM_PROJECTION = "+proj=utm +zone=30 +datum=WGS84 +units=m +no_defs";
// Coordonnées de sortie (EPSG:4326 - WGS84 Lat/Lon)
const WGS84 = "EPSG:4326";

// Fonction de conversion des coordonnées X/Y (mètres) vers Lat/Lon (degrés)
function convertCoordinates(x, y) {
    if (typeof proj4 !== 'undefined') {
        // proj4(source, destination, [x, y]) retourne [lon, lat]
        const [lon, lat] = proj4(UTM_PROJECTION, WGS84, [x, y]);
        return { lat, lon };
    }
    console.error("Proj4js non chargé. La carte ne s'affichera pas correctement.");
    return { lat: 0, lon: 0 };
}
// -----------------------------------------------------------------


// --- CONFIGURATION : DÉFINITION DES ZONES ET LEURS CHEMINS FIXES ---

const ZONES = [
    { name: 'Z1', geojson: '/static/street_views/geojson/Z1.geojson', parentFolder: 'http://10.128.3.40/panoramas/Z1/' },
    { name: 'Z2', geojson: '/static/street_views/geojson/Z2.geojson', parentFolder: 'http://10.128.3.40/panoramas/Z2/' },
    { name: 'Z3', geojson: '/static/street_views/geojson/Z3.geojson', parentFolder: 'http://10.128.3.40/panoramas/Z3/' },
    { name: 'Z4', geojson: '/static/street_views/geojson/Z4.geojson', parentFolder: 'http://10.128.3.40/panoramas/Z4/' },
    { name: 'Z5', geojson: '/static/street_views/geojson/Z5.geojson', parentFolder: 'http://10.128.3.40/panoramas/Z5/' }
];


// --- ICONE POUR LA POSITION ACTUELLE (Point rouge) ---
const currentPosIcon = L.divIcon({
    className: 'current-pos-marker',
    html: '<div style="background-color: red; border: 2px solid white; width: 10px; height: 10px; border-radius: 50%;"></div>',
    iconSize: [14, 14],
    iconAnchor: [7, 7]
});


// --- FONCTION UTILITAIRE POUR CRÉER LE VIEWER PANNELLUM ---
function createPannellumViewer(imageURL, initialYaw) {
    return pannellum.viewer('pannellum-viewer', {
        "type": "equirectangular",
        "panorama": imageURL,
        "yaw": initialYaw,
        "autoLoad": true,
        "showZoom": false,
        "mouseZoom": false,
        "showLoadin": true,
        "preview": null
    });
}


// --- FONCTION DE GESTION DU DÉPLACEMENT DE LA FENÊTRE (Draggable) ---
function makeDraggable(element, header) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    if (header) {
        header.onmousedown = dragMouseDown;
    } else {
        element.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();

        pos3 = e.clientX;
        pos4 = e.clientY;

        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();

        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        element.style.top = (element.offsetTop - pos2) + "px";
        element.style.left = (element.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}


// --- FONCTION D'INITIALISATION DE LA CARTE ---
function initMap() {
    const firstPoint = streetViewData[0];
    // Initialisation avec les coordonnées WGS84 converties
    map = L.map('map').setView([firstPoint.lat, firstPoint.lon], 16);

    // FOND DE CARTE OSM
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: "© OpenStreetMap"
    }).addTo(map);

    // // --- INTÉGRATION DU SERVICE WMS GEOSERVER ---
    // const WMS_URL = 'http://10.128.3.34:8080/geoserver/panneautage/wms';
    // const WMS_LAYER_NAME = 'panneautage:FOND_DE_CARTE_CODE_QR'; // Nom du groupe/couche

    // L.tileLayer.wms(WMS_URL, {
    //     layers: WMS_LAYER_NAME,
    //     format: 'image/png',
    //     transparent: true,
    //     version: '1.1.0',
    //     tiled: true,
    //     crs: L.CRS.EPSG4326,
    //     attribution: '© Service Géomatique Interne - GeoServer'
    // }).addTo(map);
    // // ---------------------------------------------



    //AFFICHAGE DES POINTS
    streetViewData.forEach((point, index) => {
        // Utiliser L.circleMarker pour un petit point propre et cliquable
        L.circleMarker([point.lat, point.lon], {
            radius: 3,          // Encore plus petit
            color: '#000000',   // Noir pour le contour
            fillColor: '#FFFFFF', // Remplissage Blanc
            fillOpacity: 0.5,    // Remplissage semi-transparent
            weight: 1           // Épaisseur du contour
        })
            .on('click', function () {
                // Au clic, charge le panorama correspondant
                loadPoint(index);
            })
            .addTo(map);
    });
   
}



// --- FONCTION DE CHARGEMENT D'UN POINT (Ouvre/Met à Jour la Fenêtre Modale) ---
function loadPoint(index) {
    if (index < 0 || index >= streetViewData.length) {
        return;
    }

    currentIndex = index;
    const point = streetViewData[currentIndex];

    // Afficher la fenêtre modale et mettre à jour le titre
    document.getElementById('modal-viewer-window').style.display = 'block';
    document.getElementById('current-point-id').textContent = `Point actuel: ${point.id} (Zone ${point.zoneName})`;

    // Le chemin complet utilise maintenant le chemin relatif du serveur 
    const imageURL = point.imagePathBase + point.id;
    const initialYaw = point.heading || 0;

    // Création ou rechargement du viewer.
    if (pannellumViewer) {
        try {
            pannellumViewer.loadScene({
                "type": "equirectangular",
                "panorama": imageURL,
                "yaw": initialYaw,
                "autoLoad": true
            });
        } catch (e) {
            pannellumViewer.destroy();
            pannellumViewer = createPannellumViewer(imageURL, initialYaw);
        }
    } else {
        pannellumViewer = createPannellumViewer(imageURL, initialYaw);
    }

    // --- AJOUT ET MISE À JOUR DU MARQUEUR DE POSITION ACTUELLE ---
    if (currentMarker) {
        map.removeLayer(currentMarker);
    }

    currentMarker = L.marker([point.lat, point.lon], {
        icon: currentPosIcon
    }).addTo(map);

    // Centre la carte sur la position actuelle
    map.setView([point.lat, point.lon], map.getZoom());
}



// --- FONCTION DE NAVIGATION (Séquentielle) ---
function navigate(direction) {
    const newIndex = currentIndex + direction;
    loadPoint(newIndex);
}


// --- FONCTION : Rotation de la vue à 360° ---
function turnView(degrees) {
    if (pannellumViewer) {
        const currentYaw = pannellumViewer.getYaw();
        const newYaw = currentYaw + degrees;

        pannellumViewer.setYaw(newYaw, 500, 'easeInOutQuad');
    }
}


// --- FONCTION PRINCIPALE : DÉMARRAGE DE L'APPLICATION (Charge les 5 GeoJSON) ---
async function main() {
    try {
        const allDataPromises = ZONES.map(async (zone) => {
            const response = await fetch(zone.geojson);

            if (!response.ok) {
                console.error(`Impossible de charger ${zone.geojson}: ${response.statusText}`);
                return [];
            }

            const data = await response.json();

            // Le nom de la colonne corrigé : 'CHEMIN'
            const SUB_FOLDER_PROPERTY_NAME = 'CHEMIN';

            return data.features.map((feature, i) => {
                const subFolder = feature.properties[SUB_FOLDER_PROPERTY_NAME];

                if (!subFolder) {
                    return null;
                }

                // -------------------------------------------------------------
                // Conversion des coordonnées UTM (feature.geometry.coordinates)
                // -------------------------------------------------------------
                const utmX = feature.geometry.coordinates[0];
                const utmY = feature.geometry.coordinates[1];
                const { lat, lon } = convertCoordinates(utmX, utmY); // Conversion ici

                const fullImagePathBase = zone.parentFolder + subFolder;

                return {
                    id: feature.properties.nom_image,
                    lat: lat, // Latitude WGS84 convertie
                    lon: lon, // Longitude WGS84 convertie
                    heading: feature.properties.HEADING || 0,
                    zoneName: zone.name,
                    imagePathBase: fullImagePathBase
                };
            }).filter(p => p !== null);
        });

        const results = await Promise.all(allDataPromises);
        streetViewData = results.flat();

        streetViewData.forEach((point, i) => point.index = i);

        if (streetViewData.length > 0) {
            initMap();
        } else {
            alert("Aucune donnée de panorama n'a été chargée. Vérifiez les fichiers GeoJSON et les chemins.");
        }

        // --- GESTION DE LA FENÊTRE MODALE (Écouteurs d'événements) ---
        const modalWindow = document.getElementById('modal-viewer-window');
        const modalHeader = document.getElementById('modal-header');
        const closeBtn = document.getElementById('close-button');

        makeDraggable(modalWindow, modalHeader);

        closeBtn.addEventListener('click', () => {
            modalWindow.style.display = 'none';
        });

        document.getElementById('forward-button').addEventListener('click', () => navigate(1));
        document.getElementById('backward-button').addEventListener('click', () => navigate(-1));
        document.getElementById('turn-left-button').addEventListener('click', () => turnView(-30));
        document.getElementById('turn-right-button').addEventListener('click', () => turnView(30));

        window.addEventListener('keydown', (event) => {
            if (modalWindow.style.display === 'block') {
                switch (event.key) {
                    case 'ArrowUp': navigate(1); break;
                    case 'ArrowDown': navigate(-1); break;
                    case 'ArrowLeft': turnView(-30); break;
                    case 'ArrowRight': turnView(30); break;
                }
            }
        });

    } catch (error) {
        console.error("Échec de l'initialisation de l'application:", error);
        alert("Impossible de charger les données ou le format GeoJSON est inattendu.");
    }
}

// Lancement de la fonction principale au chargement du script
main();
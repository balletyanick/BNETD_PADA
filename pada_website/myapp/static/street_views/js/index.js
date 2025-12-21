let streetViewData = [];

// Index du point dans le tableau 'streetViewData' qui est actuellement affiché
let currentIndex = 0;
// L'objet carte Leaflet
let map;
// Le marqueur spécial qui indique la position actuelle sur la carte
let currentMarker;
// VARIABLE GLOBALE pour le visualiseur Pannellum (360°)
let pannellumViewer = null;

// --- DÉFINITION DE LA PROJECTION CORRIGÉE (UTM zone 30N vers WGS84) ---
const UTM_PROJECTION = "+proj=utm +zone=30 +datum=WGS84 +units=m +no_defs";
const WGS84 = "EPSG:4326";

// Fonction de conversion des coordonnées X/Y (mètres) vers Lat/Lon (degrés)
function convertCoordinates(x, y) {
    if (typeof proj4 !== 'undefined') {
        const [lon, lat] = proj4(UTM_PROJECTION, WGS84, [x, y]);
        return { lat, lon };
    }
    console.error("Proj4js non chargé. La carte ne s'affichera pas correctement.");
    return { lat: 0, lon: 0 };
}

// --- CONFIGURATION : DÉFINITION DES ZONES ET LEURS CHEMINS FIXES ---
const ZONES = [
    { name: 'Z1', geojson: '/static/street_views/geojson/Z1.geojson', parentFolder: '/static/views/Z1/panoramas_hd/' },
    { name: 'Z2', geojson: '/static/street_views/geojson/Z2.geojson', parentFolder: 'http://10.128.3.27/views/Z2/panoramas_hd/' },
    { name: 'Z3', geojson: '/static/street_views/geojson/Z3.geojson', parentFolder: 'http://10.128.3.27/views/Z3/panoramas_hd/' },
    { name: 'Z4', geojson: '/static/street_views/geojson/Z4.geojson', parentFolder: 'http://10.128.3.27/views/Z4/panoramas_hd/' },
    { name: 'Z5', geojson: '/static/street_views/geojson/Z5.geojson', parentFolder: 'http://10.128.3.27/views/Z5/panoramas_hd/' }
];

// --- ICONE POUR LA POSITION ACTUELLE (Point rouge) ---
const currentPosIcon = L.divIcon({
    className: 'current-pos-marker',
    html: '<div style="background-color: red; border: 2px solid white; width: 10px; height: 10px; border-radius: 50%;"></div>',
    iconSize: [14, 14],
    iconAnchor: [7, 7]
});

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
    map = L.map('map').setView([firstPoint.lat, firstPoint.lon], 16);

    // FOND DE CARTE OSM
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: "© OpenStreetMap"
    }).addTo(map);

    // AFFICHAGE DES POINTS
    streetViewData.forEach((point, index) => {
        L.circleMarker([point.lat, point.lon], {
            radius: 3,
            color: '#000000',
            fillColor: '#FFFFFF',
            fillOpacity: 0.5,
            weight: 1
        })
        // .on('click', function () {
        //     loadPoint(index);
        // })
        .addTo(map);
    });
}

// --- FONCTION DE CHARGEMENT D'UN POINT (Ouvre/Met à Jour la Fenêtre Modale) ---
function loadPoint(index) {
    if (index < 0 || index >= streetViewData.length) {
        console.warn(`Index invalide: ${index} (min: 0, max: ${streetViewData.length - 1})`);
        return;
    }

    currentIndex = index;
    const point = streetViewData[currentIndex];

    // console.log(`Chargement du point ${index}:`, point);

    // Afficher la fenêtre modale et mettre à jour le titre
    document.getElementById('modal-viewer-window').style.display = 'block';
    document.getElementById('current-point-id').textContent = `Point actuel: ${point.id} (Zone ${point.zoneName})`;

    // Construction de l'URL complète de l'image
    const imageURL = point.imagePathBase + point.id;
    // console.log(`URL de l'image: ${imageURL}`);


    // ... début de la fonction loadPoint ...
    // Au lieu de mettre le heading dans yaw, on le garde pour le Nord
    const carHeading = point.heading || 0;
    const carPitch = point.pitch || 0;
    const carRoll = point.roll || 0;

    // console.log(`Données d'orientation -> Heading: ${carHeading}, Pitch: ${carPitch}, Roll: ${carRoll}`);



pannellumViewer = pannellum.viewer('pannellum-viewer', {
    "type": "equirectangular",
    "panorama": imageURL,
    
    // yaw: 0 signifie "Regarde le centre de l'image" (donc la route devant)
    "yaw": 0, 
    
    // pitch: 0 signifie "Regarde l'horizon", pas le ciel ni le sol
    "pitch": 0,

    // northOffset: Indique à Pannellum où se trouve le Nord par rapport au centre de l'image.
    // Cela permet d'avoir la boussole juste, tout en regardant la route.
    "northOffset": carHeading,

    // horizonPitch: Compense la montée/descente de la route
    "horizonPitch": carPitch,

    /* --- OPTIONS STANDARDS --- */
    "autoLoad": true,
    "showZoom": false,
    "mouseZoom": false,
    "showLoading": true,
    "compass": true, // Affiche la boussole pour vérifier le Nord
    "preview": null
});

    // console.log('Viewer créé avec succès');

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
    // console.log(`Navigation: currentIndex=${currentIndex}, direction=${direction}, newIndex=${newIndex}`);
    loadPoint(newIndex);
}

// --- FONCTION : Rotation de la vue à 360° ---
function turnView(degrees) {
    if (pannellumViewer) {
        const currentYaw = pannellumViewer.getYaw();
        const newYaw = currentYaw + degrees;
        // console.log(`Rotation: ${currentYaw}° → ${newYaw}°`);
        pannellumViewer.setYaw(newYaw, 500, 'easeInOutQuad');
    }
}

// --- FONCTION POUR TROUVER LE POINT LE PLUS PROCHE ---
function findClosestPointIndex(targetLat, targetLon) {
    let minDistance = Infinity;
    let closestIndex = 0;

    streetViewData.forEach((point, index) => {
        // Formule de distance simple (Pythagore) suffisante pour des points proches
        const dist = Math.sqrt(Math.pow(point.lat - targetLat, 2) + Math.pow(point.lon - targetLon, 2));
        
        if (dist < minDistance) {
            minDistance = dist;
            closestIndex = index;
        }
    });

    return closestIndex;
}

//FONCTION PRINCIPALE : DÉMARRAGE DE L'APPLICATION (Charge les 5 GeoJSON) ---
async function main() {
    try {
        // console.log('Démarrage de l\'application...');

        const allDataPromises = ZONES.map(async (zone) => {
            // console.log(`Chargement de ${zone.name}...`);
            const response = await fetch(zone.geojson);

            if (!response.ok) {
                // console.error(`Impossible de charger ${zone.geojson}: ${response.statusText}`);
                return [];
            }

            const data = await response.json();
            // console.log(`${zone.name} chargé: ${data.features.length} points`);

            const SUB_FOLDER_PROPERTY_NAME = 'CHEMIN';

            return data.features.map((feature, i) => {
                const subFolder = feature.properties[SUB_FOLDER_PROPERTY_NAME];

                if (!subFolder) {
                    console.warn(`Pas de CHEMIN pour la feature ${i} dans ${zone.name}`);
                    return null;
                }

                // Conversion des coordonnées UTM vers WGS84
                const utmX = feature.geometry.coordinates[0];
                const utmY = feature.geometry.coordinates[1];
                const { lat, lon } = convertCoordinates(utmX, utmY);

                const fullImagePathBase = zone.parentFolder + subFolder;

                return {
                    id: feature.properties.nom_image,
                    lat: lat,
                    lon: lon,
                    // HEADING est la direction de la voiture par rapport au Nord
                    heading: feature.properties.HEADING || 0, 
                    // PITCH : inclinaison avant/arrière (montée/descente)
                    pitch: feature.properties.PITCH || 0,
                    // ROLL : inclinaison gauche/droite (horizon penché)
                    roll: feature.properties.ROLL || 0,
                    zoneName: zone.name,
                    imagePathBase: fullImagePathBase
                };
            }).filter(p => p !== null);
        });

        const results = await Promise.all(allDataPromises);
        streetViewData = results.flat();

        streetViewData.forEach((point, i) => point.index = i);

        // console.log(`Total de points chargés: ${streetViewData.length}`);
        // console.log('Premier point:', streetViewData[0]);

       if (streetViewData.length > 0) {
            initMap();

            const urlParams = new URLSearchParams(window.location.search);
            const paramX = urlParams.get('x');
            const paramY = urlParams.get('y');

            if (paramX && paramY && paramX !== "None") {
                const valX = parseFloat(paramX);
                const valY = parseFloat(paramY);

                let targetLat, targetLon;

                // DETECTION : Si valX est entre -180 et 180, ce sont des DEGRÉS (WGS84)
                if (Math.abs(valX) <= 180) {
                    console.log("Mode Degrés détecté (GPS)");
                    targetLon = valX;
                    targetLat = valY;
                } else {
                    // Sinon, on considère que ce sont des MÈTRES (UTM) et on convertit
                    console.log("Mode Mètres détecté (UTM)");
                    const converted = convertCoordinates(valX, valY);
                    targetLat = converted.lat;
                    targetLon = converted.lon;
                }

                // console.log(`Recherche du point le plus proche de : Lat ${targetLat}, Lon ${targetLon}`);

                // Trouver l'index dans le tableau global streetViewData
                const closestIndex = findClosestPointIndex(targetLat, targetLon);
                
                if (closestIndex !== -1) {
                    // console.log(`Trouvé ! Zone: ${streetViewData[closestIndex].zoneName}, Index: ${closestIndex}`);
                    loadPoint(closestIndex);
                    
                    // Optionnel : Forcer la carte à se centrer
                    if (map) {
                        map.setView([targetLat, targetLon], 18);
                    }
                }
            }
        } else {
            alert("Aucune donnée de panorama n'a été chargée.");
            return;
        }

        // --- GESTION DE LA FENÊTRE MODALE (Écouteurs d'événements) ---
        const modalWindow = document.getElementById('modal-viewer-window');
        const modalHeader = document.getElementById('modal-header');
        const closeBtn = document.getElementById('close-button');

        if (!modalWindow || !modalHeader || !closeBtn) {
            console.error('Éléments de la modale non trouvés dans le DOM');
            return;
        }

        makeDraggable(modalWindow, modalHeader);

        closeBtn.addEventListener('click', () => {
            // console.log('Fermeture de la modale');
            modalWindow.style.display = 'none';
        });

        // BOUTONS DE NAVIGATION
        const forwardBtn = document.getElementById('forward-button');
        const backwardBtn = document.getElementById('backward-button');
        const turnLeftBtn = document.getElementById('turn-left-button');
        const turnRightBtn = document.getElementById('turn-right-button');

        if (forwardBtn) {
            forwardBtn.addEventListener('click', () => {
                console.log('⬆️ Bouton Avancer cliqué');
                navigate(1);
            });
        } else {
            console.error('forward-button non trouvé');
        }

        if (backwardBtn) {
            backwardBtn.addEventListener('click', () => {
                // console.log('Bouton Reculer cliqué');
                navigate(-1);
            });
        } else {
            console.error('backward-button non trouvé');
        }

        if (turnLeftBtn) {
            turnLeftBtn.addEventListener('click', () => {
                // console.log('Bouton Gauche cliqué');
                turnView(-30);
            });
        } else {
            console.error('turn-left-button non trouvé');
        }

        if (turnRightBtn) {
            turnRightBtn.addEventListener('click', () => {
                // console.log('➡️ Bouton Droite cliqué');
                turnView(30);
            });
        } else {
            console.error('turn-right-button non trouvé');
        }

        // RACCOURCIS CLAVIER
        window.addEventListener('keydown', (event) => {
            if (modalWindow.style.display === 'block') {
                console.log(`⌨️ Touche pressée: ${event.key}`);
                switch (event.key) {
                    case 'ArrowUp':
                        navigate(1);
                        break;
                    case 'ArrowDown':
                        navigate(-1);
                        break;
                    case 'ArrowLeft':
                        turnView(-30);
                        break;
                    case 'ArrowRight':
                        turnView(30);
                        break;
                }
            }
        });

        // console.log('Application initialisée avec succès');

    } catch (error) {
        // console.error("Échec de l'initialisation de l'application:", error);
        alert("Impossible de charger les données ou le format GeoJSON est inattendu.");
    }
}

// Lancement de la fonction principale au chargement du script
main();
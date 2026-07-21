// Carte centrée sur Thiès, Sénégal
const map = L.map("map").setView([14.7833, -16.9333], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

let markersLayer = L.layerGroup().addTo(map);

const colors = {
  doctors: "#2E86AB",
  pharmacy: "#27AE60",
  dentist: "#8E44AD",
  hospital: "#C0392B",
  clinic: "#E67E22",
};

function colorFor(type) {
  return colors[type] || "#555555";
}

async function chargerEtablissements(type = "") {
  const url = type ? `/api/etablissements?type=${encodeURIComponent(type)}` : "/api/etablissements";
  const res = await fetch(url);
  const data = await res.json();

  markersLayer.clearLayers();

  data.features.forEach((feature) => {
    if (!feature.geometry) return;
    const [lon, lat] = feature.geometry.coordinates;
    const props = feature.properties;

    const marker = L.circleMarker([lat, lon], {
      radius: 7,
      color: colorFor(props.amenity),
      fillColor: colorFor(props.amenity),
      fillOpacity: 0.8,
      weight: 1,
    });

    marker.bindPopup(`
      <strong>${props.name}</strong><br/>
      Type : ${props.amenity}<br/>
      ${props.healthcare ? "Santé : " + props.healthcare : ""}
    `);

    markersLayer.addLayer(marker);
  });
}

async function chargerStats() {
  const res = await fetch("/api/stats");
  const data = await res.json();

  const select = document.getElementById("filtreType");
  const list = document.getElementById("statsList");
  list.innerHTML = "";

  data.forEach((item) => {
    // Options du filtre
    const opt = document.createElement("option");
    opt.value = item.type;
    opt.textContent = item.type;
    select.appendChild(opt);

    // Ligne de stats
    const li = document.createElement("li");
    li.innerHTML = `<span>${item.type}</span><strong>${item.count}</strong>`;
    list.appendChild(li);
  });
}

document.getElementById("filtreType").addEventListener("change", (e) => {
  chargerEtablissements(e.target.value);
});

chargerEtablissements();
chargerStats();

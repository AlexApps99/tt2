const offcanvas = new bootstrap.Offcanvas(document.getElementById("offcanvas"));
const offcanvas2el = document.getElementById("offcanvas2");
const lat = document.getElementById("lat");
const lon = document.getElementById("lon");
const offcanvas2 = (() => {
  if (offcanvas2el != null) {
    return new bootstrap.Offcanvas(offcanvas2el);
} else {
  return null;
}
})();
const offcanvasLabel = document.getElementById("offcanvasLabel");
const qual = document.getElementById("quality");
const tests = document.getElementById("tests");


const ICON = L.Icon.Default.extend({});
const GOOD_ICON = new ICON({iconUrl: 'good-icon.png', iconRetinaUrl: 'good-icon-2x.png'});
const RISKY_ICON = new ICON({iconUrl: 'risky-icon.png', iconRetinaUrl: 'risky-icon-2x.png'});
const UNSAFE_ICON = new ICON({iconUrl: 'unsafe-icon.png', iconRetinaUrl: 'unsafe-icon-2x.png'});

function testentry(t) {
  console.log(t);
  return `<table class="table caption-top">
  <caption>${t.date}</caption>
  <tbody>
    <tr class="table-${RATINGS[t.qualities[0]][0]}">
      <th scope="row">Nitrate</th>
      <td>${t.nitrate} ppm</td>
    </tr>
    <tr class="table-${RATINGS[t.qualities[1]][0]}">
      <th scope="row">Nitride</th>
      <td>${t.nitride} ppm</td>
    </tr>
    <tr class="table-${RATINGS[t.qualities[2]][0]}">
      <th scope="row">pH</th>
      <td>${t.ph}</td>
    </tr>
    <tr class="table-${RATINGS[t.qualities[3]][0]}">
      <th scope="row">Free Chlorine</th>
      <td>${t.free_cl} ppm</td>
    </tr>
    <tr class="table-${RATINGS[t.qualities[4]][0]}">
      <th scope="row">Total Chlorine</th>
      <td>${t.total_cl} ppm</td>
    </tr>
    <tr class="table-${RATINGS[t.qualities[5]][0]}">
      <th scope="row">Hardness</th>
      <td>${t.hardness} ppm</td>
    </tr>
</table>`;
}



const RATINGS = [
  ["danger", "Deadly", UNSAFE_ICON],
  ["danger", "Unsafe", UNSAFE_ICON],
  ["warning", "Risky", RISKY_ICON],
  ["success", "Safe", GOOD_ICON],
];

// change image
let editing_marker = L.marker([0.0, 0.0]);
editing_marker.setOpacity(1/3);
if (offcanvas2 != null) {
  offcanvas2el.addEventListener('hide.bs.offcanvas', () => editing_marker.remove());
}

// Find a way to cancel older async if its pressed multiple times
function pop2(o) {
  //console.log(o);
  fetch(o.layer.options.internal_id.toString() + ".json").then(r => r.json()).then(j => {
    if (j == null) return;
    //console.log(j);
    offcanvasLabel.innerText = j.name;
    tests.innerHTML = `<div>${j.description}</div>`;

	for (const t of j.tests) {
	  tests.innerHTML += testentry(t);
	}

    qual.innerText = RATINGS[j.tests[0].quality][1];
    qual.className = "badge bg-" + RATINGS[j.tests[0].quality][0];
    offcanvas.show();
  });
}

let cluster = true;

let map = L.map('map').setView([-36.85, 174.75], 10);
L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(map);
let markers = cluster ? L.markerClusterGroup({ showCoverageOnHover: false }) : L.layerGroup();


fetch('map.json').then(r => r.json()).then(j => {
  j.forEach(e => {
    let marker = L.marker(e[1], {internal_id: e[0], icon: RATINGS[e[2]][2]});
    markers.addLayer(marker);
  });
});
markers.on('click', pop2);
map.addLayer(markers);

// fetch('map.json').then(r => r.json()).then(j => {
//   let geoJsonLayer = L.geoJson(j, {
//     onEachFeature: function (feature, layer) {
//       layer.bindPopup(pop2(feature.properties));
//     }
//   });
//   markers.addLayer(geoJsonLayer);
// });
// map.addLayer(markers);

if (offcanvas2 != null) {
map.on("click", o => {
  editing_marker.setLatLng(o.latlng);
  editing_marker.addTo(map);
  lat.value = o.latlng.lat;
  lon.value = o.latlng.lng;
  offcanvas2.show();
})
}

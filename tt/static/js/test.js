function pop(m) {
  return `<table class="table">
  <thead>
	<tr>
	  <th scope="col">Property</th>
	  <th scope="col">Value</th>
	</tr>
  </thead>
  <tbody>
	<tr>
	  <th scope="row">pH</th>
	  <td>7</td>
	</tr>
	<tr>
	  <th scope="row">Salinity</th>
	  <td>3.1</td>
	</tr>
	<tr>
	  <th scope="row">Extra crunch</th>
	  <td>Yes</td>
	</tr>
  </tbody>
</table>`;
}

function pop2(o) {
  let out = '<table class="table"><thead><tr><th scope="col">Property</th><th scope="col">Value</th></tr></thead><tbody>';
  for (const [key, value] of Object.entries(o)) {
	if (key !== "ID") {
      out += `<tr><th scope="row">${key}</th><td>${value}</td></tr>`;
	}
  }
  return out + '</tbody></table>';
}

let cluster = true;

let map = L.map('map').setView([-36.85, 174.75], 10);
L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(map);
let markers = cluster ? L.markerClusterGroup({ showCoverageOnHover: false }) : L.layerGroup();


fetch('map.json').then(r => r.json()).then(j => {
  j.forEach(e => {
    let marker = L.marker(e[1]);
    //marker.bindPopup(pop2(e));
    markers.addLayer(marker);
  });
});
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


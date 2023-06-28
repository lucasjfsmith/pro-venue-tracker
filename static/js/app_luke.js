let streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

let map = L.map("map", {
    center: [37.09, -95.71],
    zoom: 5
  });

streetmap.addTo(map);

let layers = {
    NBA: new L.LayerGroup(),
    NFL: new L.LayerGroup(),
    MLB: new L.LayerGroup(),
    NHL: new L.LayerGroup(),
    MLS: new L.LayerGroup()
  };

let overlayMaps = {
    "NBA": layers.NBA,
    "NFL": layers.NFL,
    "MLB": layers.MLB,
    "NHL": layers.NHL,
    "MLS": layers.MLS
  };

L.control.layers(null, overlayMaps).addTo(map);

let colors = {
    NBA: "orange",
    NFL: "blue",
    MLB: "red",
    NHL: "white",
    MLS: "green"
}

d3.json("/api/teams").then(teams => {

    for (let i = 0; i < teams.length; i++) {

        let latlng = [teams[i].venue_lat, teams[i].venue_lon]

        let marker = L.marker(latlng);

        marker.bindPopup(`<h2>${teams[i].venue_name}</h2><br>` +
                         `<h3>${teams[i].league} Team: ${teams[i].team}</h3><hr>` +
                         `<p>${teams[i].venue_address}</p>`
        );

        marker.addTo(layers[teams[i].league]);
    };
});
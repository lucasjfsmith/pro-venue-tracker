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

d3.json("api/venues").then(venues => {

  for (const venue in venues) {
    let teams = venues[venue];

    let latlng = [teams[0].venue_lat, teams[0].venue_lon];
    let marker = L.marker(latlng);
    let venue_html = `<h1>${teams[0].venue_name}</h1><br><p>${teams[0].venue_address}</p>`;

    let leagues = [];

    for (let i = 0; i<teams.length; i++) {
      console.log(teams[i]);
      let team_html = `<h2>${teams[i].league} Team: ${teams[i].team}</h2><br>`;

      let event_html = ``
      if (teams[i].league == "NBA") {
        event_html = `NBA Schedule not available.`;
      } else {
        event_html = `<h3>Next Event: ${teams[i].next_event[0]} vs. ${teams[i].next_event[1]}</h3>`;
      };

      venue_html = venue_html + team_html + event_html + '<hr>';
      leagues.push(teams[i].league)
    };

    marker.bindPopup(venue_html);

    for (let i = 0; i<leagues.length; i++) {
      marker.addTo(layers[leagues[i]]);
    };
  };
});
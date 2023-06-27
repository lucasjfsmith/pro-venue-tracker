// Marker lists for each league
let nflMarkers = [];
let nbaMarkers = [];
let mlbMarkers = [];
let nhlMarkers = [];
let mlsMarkers = [];

d3.json("/api/teams").then(teams => {

    console.log(teams);
});

// for (let i = 0; i < locations.length; i++)


let streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});




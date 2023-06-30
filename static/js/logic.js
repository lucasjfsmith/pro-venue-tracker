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

// Fetch the data from the '/api/teams' route
fetch('/api/teams')
  .then(response => response.json())
  .then(data => {
    // Extract the venue states and count their occurrences
    const stateCounts = {};
    data.forEach(team => {
      const state = team.venue_state;
      stateCounts[state] = (stateCounts[state] || 0) + 1;
    });
    // Prepare the data for the bar chart
    const labels = Object.keys(stateCounts);
    const counts = Object.values(stateCounts);
    // Create bar chart
    const ctx = document.getElementById('barChart').getContext('2d');
    const barChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Number of Venues',
            data: counts,
            backgroundColor: 'lightgreen',
            borderColor: 'green',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'States',
              font: {
                size: 16,
                weight: 'bold'
              }
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Total',
              font: {
                size: 16,
                weight: 'bold'
              }
            },
            ticks: {
              beginAtZero: true,
              stepSize: 1
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Number of Venues in each State',
            font: {
              size: 22,
              weight: 'bold'
            }
          },
          datalabels: {
            anchor: 'end',
            align: 'top',
            formatter: function (value) {
              return value;
            },
            color: 'black',
            font: {
              weight: 'bold'
            },
            display: 'auto'
          }
        }
      }
    })
  });

// d3.json('/api/teams').then(data => {
//   // Extract the venue states and count their occurrences
//   let stateCounts = {};
//   data.forEach(team => {
//     let state = team.venue_state;
//     stateCounts[state] = (stateCounts[state] || 0) + 1;
//   });

//   // Prepare the data for the bar chart
//   let labels = Object.keys(stateCounts);
//   let counts = Object.values(stateCounts);
//   // Create bar chart
//   let ctx = document.getElementById('barChart').getContext('2d');

//   let barChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: labels,
//       datasets: [
//         {
//           label: 'Number of Venues',
//           data: counts,
//           backgroundColor: 'lightgreen',
//           borderColor: 'green',
//           borderWidth: 1
//         }
//       ]
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false,
//       aspectRatio: 1,
//       scales: {
//         x: {
//           display: true,
//           title: {
//             display: true,
//             text: 'States',
//             font: {
//               size: 16,
//               weight: 'bold'
//             }
//           }
//         },
//         y: {
//           display: true,
//           title: {
//             display: true,
//             text: 'Total',
//             font: {
//               size: 16,
//               weight: 'bold'
//             }
//           },
//           ticks: {
//             beginAtZero: true,
//             stepSize: 1
//           }
//         }
//       },
//       plugins: {
//         title: {
//           display: true,
//           text: 'Number of Venues in each State',
//           font: {
//             size: 22,
//             weight: 'bold'
//           }
//         },
//         datalabels: {
//           anchor: 'end',
//           align: 'top',
//           formatter: function (value) {
//             return value;
//           },
//           color: 'black',
//           font: {
//             weight: 'bold'
//           },
//           display: 'auto'
//         }
//       }
//     }
//     })
// });
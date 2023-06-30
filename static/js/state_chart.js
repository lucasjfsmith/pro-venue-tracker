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
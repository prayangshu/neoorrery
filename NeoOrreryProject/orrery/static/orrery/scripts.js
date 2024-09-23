// Fetching values from hidden elements in the HTML
const totalPlanets = parseFloat(document.getElementById('totalPlanets').textContent);
const totalAsteroids = parseFloat(document.getElementById('totalAsteroids').textContent);
const totalPHA = parseFloat(document.getElementById('totalPHA').textContent);
const totalComets = parseFloat(document.getElementById('totalComets').textContent);

// Calculating the total number of celestial bodies
const totalBodies = totalPlanets + totalAsteroids + totalPHA + totalComets;

// Calculate percentages for each celestial body type
const planetsPercentage = ((totalPlanets / totalBodies) * 100).toFixed(2);
const asteroidsPercentage = ((totalAsteroids / totalBodies) * 100).toFixed(2);
const phaPercentage = ((totalPHA / totalBodies) * 100).toFixed(2);
const cometsPercentage = ((totalComets / totalBodies) * 100).toFixed(2);

// Update the percentages in the HTML
document.getElementById('planets-percentage').textContent = planetsPercentage + '%';
document.getElementById('asteroids-percentage').textContent = asteroidsPercentage + '%';
document.getElementById('pha-percentage').textContent = phaPercentage + '%';
document.getElementById('comets-percentage').textContent = cometsPercentage + '%';

// Setting up the pie chart using Chart.js
const ctx = document.getElementById('celestial-body-chart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Planets', 'Asteroids', 'PHA', 'Comets'],
        datasets: [{
            label: 'Celestial Bodies',
            data: [totalPlanets, totalAsteroids, totalPHA, totalComets],
            backgroundColor: ['#FFD700', '#B0B0B0', '#A9A9A9', '#32CD32'],  // Yellow for Planets, Grey for Asteroids, Dark Grey for PHA, Green for Comets
            hoverOffset: 8,  // Add some hover offset for better effect
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }
                        const total = context.dataset.data.reduce((sum, value) => sum + value, 0);
                        const value = context.raw;
                        label += value + ' (' + ((value / total) * 100).toFixed(2) + '%)';
                        return label;
                    }
                }
            }
        },
        animation: {
            animateScale: true, // Animate the scaling of the pie chart
            animateRotate: true, // Animate rotation
        }
    }
});

// Set the current year in the footer
document.getElementById('currentYear').textContent = new Date().getFullYear();

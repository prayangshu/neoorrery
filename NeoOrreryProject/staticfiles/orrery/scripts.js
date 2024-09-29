// Fetching values from hidden elements in the HTML
const totalPlanets = parseFloat(document.getElementById('totalPlanets').textContent);
const totalAsteroids = parseFloat(document.getElementById('totalAsteroids').textContent);
const totalPHA = parseFloat(document.getElementById('totalPHA').textContent);
const totalComets = parseFloat(document.getElementById('totalComets').textContent);

// Calculating the total number of celestial bodies
const totalBodies = totalPlanets + totalAsteroids + totalPHA + totalComets;

// Responsive setup for chart scaling
function getResponsiveSize() {
    const width = window.innerWidth;

    if (width <= 480) {
        return 200;  // Small chart for mobile screens
    } else if (width <= 768) {
        return 300;  // Medium chart for tablets
    } else {
        return 400;  // Large chart for desktops
    }
}

// Create and update the chart based on screen size
function createPieChart() {
    const chartSize = getResponsiveSize();

    const ctx = document.getElementById('celestial-body-chart').getContext('2d');

    return new Chart(ctx, {
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
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: chartSize * 0.1,  // Adjust legend size based on chart size
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
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
                animateScale: true,  // Animate the scaling of the pie chart
                animateRotate: true,  // Animate rotation
            },
            layout: {
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        }
    });
}

// Initialize the chart only if data is available
if (totalBodies > 0) {
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

    // Create the pie chart
    let pieChart = createPieChart();

    // Redraw the chart on window resize for responsiveness
    window.addEventListener('resize', function () {
        pieChart.destroy();  // Destroy the old chart
        pieChart = createPieChart();  // Create a new chart
    });

} else {
    console.warn('No celestial bodies data available for chart generation.');
}

// Set the current year in the footer
const footerYearElement = document.getElementById('currentYear');
if (footerYearElement) {
    footerYearElement.textContent = new Date().getFullYear();
} else {
    console.warn('Footer year element not found.');
}

const totalPlanets = parseFloat('{{ total_planets }}');
const totalAsteroids = parseFloat('{{ total_asteroids }}');
const totalPHA = parseFloat('{{ total_pha }}');
const totalComets = parseFloat('{{ total_comets }}');
const totalBodies = totalPlanets + totalAsteroids + totalPHA + totalComets;

const planetsPercentage = ((totalPlanets / totalBodies) * 100).toFixed(2);
const asteroidsPercentage = ((totalAsteroids / totalBodies) * 100).toFixed(2);
const phaPercentage = ((totalPHA / totalBodies) * 100).toFixed(2);
const cometsPercentage = ((totalComets / totalBodies) * 100).toFixed(2);

document.getElementById('planets-percentage').textContent = planetsPercentage + '%';
document.getElementById('asteroids-percentage').textContent = asteroidsPercentage + '%';
document.getElementById('pha-percentage').textContent = phaPercentage + '%';
document.getElementById('comets-percentage').textContent = cometsPercentage + '%';

const ctx = document.getElementById('celestial-body-chart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Planets', 'Asteroids', 'PHA', 'Comets'],
        datasets: [{
            label: 'Celestial Bodies',
            data: [totalPlanets, totalAsteroids, totalPHA, totalComets],
            backgroundColor: ['yellow', 'grey', 'darkgrey', 'green'],
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
                        label += value + ' (' + Math.round((value / total) * 100) + '%)';
                        return label;
                    }
                }
            }
        }
    }
});

document.getElementById('currentYear').textContent = new Date().getFullYear();

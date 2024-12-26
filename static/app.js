document.addEventListener('DOMContentLoaded', function () {
    updateDateTime();
    fetchDataAndRenderCharts();
});

function updateDateTime() {
    const now = new Date();
    const dateElement = document.getElementById('date');
    const timeElement = document.getElementById('time');

    const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' };
    const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit' };

    dateElement.textContent = now.toLocaleDateString(undefined, optionsDate);
    timeElement.textContent = now.toLocaleTimeString(undefined, optionsTime);
}

updateDateTime();
setInterval(updateDateTime, 1000);

function fetchDataAndRenderCharts() {
    const playstoreChartElement = document.getElementById('playstoreChart');
    const applestoreChartElement = document.getElementById('applestoreChart');

    if (playstoreChartElement) {
        fetch('/api/playstore_top_apps')
            .then(response => response.json())
            .then(data => {
                const labels = data.map(app => app.App);
                const reviews = data.map(app => app.Reviews);

                new Chart(playstoreChartElement, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Reviews',
                            data: reviews,
                            backgroundColor: [
                                'rgba(153, 102, 255, 1)',
                                'rgba(238, 130, 238, 1)',
                                'rgba(255, 159, 64, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 99, 71, 1)',
                                'rgba(255, 159, 64, 1)',
                                'rgba(54, 162, 235, 1)'
                            ],
                            borderColor: 'rgba(255, 255, 255, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                ticks: {
                                    color: 'white' // X-axis labels color
                                }
                            },
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    color: 'white' // Y-axis labels color
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching playstore comparison data:', error));
    }

    if (applestoreChartElement) {
        fetch('/api/applestore_top_apps')
            .then(response => response.json())
            .then(data => {
                const labels = data.map(app => app.track_name);
                const ratingCounts = data.map(app => app.rating_count_tot);

                new Chart(applestoreChartElement, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Rating Count',
                            data: ratingCounts,
                            backgroundColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)',
                                'rgba(201, 203, 207, 1)',
                                'rgba(255, 99, 71, 1)',
                                'rgba(144, 238, 144, 1)',
                                'rgba(238, 130, 238, 1)'
                            ],
                            borderColor: 'rgba(255, 255, 255, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                ticks: {
                                    color: 'black' // X-axis labels color
                                }
                            },
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    color: 'black' // Y-axis labels color
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching applestore comparison data:', error));
    }
}

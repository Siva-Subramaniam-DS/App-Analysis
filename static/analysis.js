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

function fetchDataAndRenderCharts() {
    const playstoreChartElement = document.getElementById('playstoreChart');
    const applestoreChartElement = document.getElementById('applestoreChart');
    const playstoreChart_Element = document.getElementById('playstoreChartbar');
    const applestoreChart_Element = document.getElementById('applestoreChartbar');

    // Fetch and render Google Play Store genre chart
    fetch('/api/playstore_genre_counts')
        .then(response => response.json())
        .then(data => {
            renderChart(playstoreChartElement, data, 'genre', 'Number of Apps', ['rgba(153, 102, 255, 0.7)',
                'rgba(255, 99, 132, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(255, 159, 64, 0.7)',   
                'rgba(54, 162, 235, 0.7)',   
                'rgba(255, 205, 86, 0.7)',   
                'rgba(201, 203, 207, 0.7)',  
                'rgba(153, 255, 102, 0.7)',  
                'rgba(255, 0, 0, 0.7)',   
                'rgba(54, 162, 235, 0.7)'], 'rgba(75, 192, 192, 1)');
        })
        .catch(error => console.error('Error fetching playstore genre counts:', error));

    // Fetch and render Apple App Store genre chart
    fetch('/api/applestore_genre_counts')
        .then(response => response.json())
        .then(data => {
            renderChart(applestoreChartElement, data, 'prime_genre', 'Number of Apps', ['rgba(75, 192, 75, 0.7)',
                'rgba(255, 105, 180, 0.7)',
                'rgba(75, 0, 130, 0.7)',
                'rgba(191, 255, 0, 0.7)',
                'rgba(0, 255, 255, 0.7)',
                'rgba(255, 182, 193, 0.7)',
                'rgba(221, 160, 221, 0.7)',
                'rgba(189, 252, 201, 0.7)',
                'rgba(135, 206, 250, 0.7)',
                'rgba(255, 255, 204, 0.7)']
                , 'rgba(153, 102, 255, 1)');
        })
        .catch(error => console.error('Error fetching applestore genre counts:', error));

    // Fetch and render Google Play Store top apps by reviews
    fetch('/api/playstore_top_apps')
        .then(response => response.json())
        .then(data => {
            renderChart(playstoreChart_Element, data, 'App', 'Reviews', ['rgba(153, 102, 255, 0.7)',
                'rgba(255, 99, 132, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(255, 159, 64, 0.7)',   
                'rgba(54, 162, 235, 0.7)',   
                'rgba(255, 205, 86, 0.7)',   
                'rgba(201, 203, 207, 0.7)',  
                'rgba(153, 255, 102, 0.7)',  
                'rgba(255, 0, 0, 0.7)',   
                'rgba(54, 162, 235, 0.7)'], 'rgba(255, 255, 255, 1)', true);
        })
        .catch(error => console.error('Error fetching playstore top apps:', error));

    // Fetch and render Apple App Store top apps by rating count
    fetch('/api/applestore_top_apps')
        .then(response => response.json())
        .then(data => {
            renderChart(applestoreChart_Element, data, 'track_name', 'Rating Count', ['rgba(0,0,0, 0.7)',
                'rgba(255, 105, 180, 0.7)',
                'rgba(75, 0, 130, 0.7)',
                'rgba(191, 255, 0, 0.7)',
                'rgba(0, 255, 255, 0.7)',
                'rgba(255, 182, 193, 0.7)',
                'rgba(221, 160, 221, 0.7)',
                'rgba(189, 252, 201, 0.7)',
                'rgba(135, 206, 250, 0.7)',
                'rgba(255, 255, 204, 0.7)'], 'rgba(255, 255, 255, 1)', true);
        })
        .catch(error => console.error('Error fetching applestore top apps:', error));
}

function renderChart(element, data, labelKey, datasetLabel, bgColor, borderColor, isBarChart = false) {
    const labels = data.map(item => item[labelKey]);
    const counts = data.map(item => item.count || item.Reviews || item.rating_count_tot);

    new Chart(element, {
        type: isBarChart ? 'bar' : 'line',
        data: {
            labels: labels,
            datasets: [{
                label: datasetLabel,
                data: counts,
                backgroundColor: bgColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'white'
                    }
                },
                x: {
                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });
}

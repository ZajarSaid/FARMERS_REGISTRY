document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('regionSelect');
    regionSelect.addEventListener('change', fetchData);

    fetchData(); // Fetch initial data

    async function fetchData() {
        const regionId = regionSelect.value;
        let url = '/Production/FarmOutputTrends/';

        if (regionId) {
            url += `?region=${regionId}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        
        // Process data for Chart.js
        const labels = [];
        const outputData = [];

        data.forEach(item => {
            labels.push(item.crop_name);
            outputData.push(item.total_output);
        });
        
        // Create the chart
        const ctx = document.getElementById('cropChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Output per Crop',
                    data: outputData,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Total Output per Crop'
                    }
                }
            }
        });
    }
});

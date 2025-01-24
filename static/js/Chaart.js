document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('regionSelect');
    regionSelect.addEventListener('change', fetchData);

    let chartInstance = null; // Variable to store the chart instance

    fetchData(); // Fetch initial data

    async function fetchData() {
        try {
            const regionId = regionSelect.value;
            let url = '/Production/FarmOutputTrends/'; // Update this URL if necessary

            if (regionId) {
                url += `?region=${regionId}`;
            }

            // Fetch the response from the server
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse the JSON response
            const responseData = await response.json();
            const data = responseData.data;

            // Process data for Chart.js
            const labels = [];
            const outputData = [];

            data.forEach(item => {
                labels.push(item.crop_name);
                outputData.push(item.total_output);
            });

            // Update summary values
            const summary = responseData.summary;
            document.getElementById('totalFarms').textContent = summary.total_farms;
            document.getElementById('totalOutput').textContent = summary.total_output;

            // Destroy the existing chart instance if it exists
            if (chartInstance) {
                chartInstance.destroy();
            }

            // Create a new chart instance
            const ctx = document.getElementById('cropChart1').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'bar',
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
        } catch (error) {
            console.error('Error fetching or processing data:', error);
        }
    }
});

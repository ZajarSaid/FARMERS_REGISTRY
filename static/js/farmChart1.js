async function fetchData() {
    const response = await fetch('/Production/FarmOutputTrends/');
    const data = await response.json();
    
    // Process data for Chart.js
    const labels = [];
    const outputData = [];

    data.forEach(item => {
        labels.push(item.crop_name);
        outputData.push(item.total_output);
    });

    // Create the chart
    const ctx = document.getElementById('cropChart1').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Output per Crop',
                data: outputData,
                // backgroundColor: [
                //     'rgba(255, 0, 0, 0.2)',
                //     'rgba(54, 162, 235, 0.2)',
                //     'rgba(255, 206, 86, 0.2)',
                //     'rgba(75, 192, 192, 0.2)',
                //     'rgba(153, 102, 255, 0.2)',
                //     'rgba(255, 159, 64, 0.2)'
                // ],
                // borderColor: [
                //     'rgba(255, 99, 132, 1)',
                //     'rgba(54, 162, 235, 1)',
                //     'rgba(255, 206, 86, 1)',
                //     'rgba(75, 192, 192, 1)',
                //     'rgba(153, 102, 255, 1)',
                //     'rgba(255, 159, 64, 1)'
                // ],
                // borderWidth: 1
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

document.addEventListener('DOMContentLoaded', fetchData);

document.addEventListener('DOMContentLoaded', () => {
    const dataContainer = document.getElementById('chart-data');
    if (!dataContainer) return;

    const labelsRaw = dataContainer.getAttribute('data-labels');
    const durationsRaw = dataContainer.getAttribute('data-durations');

    if (!labelsRaw || !durationsRaw) return;

    const labels = labelsRaw.split(',');
    const durations = durationsRaw.split(',').map(Number);

    const ctx = document.getElementById('durationChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Duration (mins)',
                data: durations,
                borderColor: '#2D6A4F',
                backgroundColor: 'rgba(45, 106, 79, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Minutes'
                    }
                }
            }
        }
    });
});

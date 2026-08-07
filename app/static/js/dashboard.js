/**
 * AI CAREER CONNECT - Dynamic Dashboard Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    initDashboardChart();
});

function initDashboardChart() {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;

    fetch('/api/dashboard/stats')
        .then(res => res.json())
        .then(data => {
            const chartData = data.chart_data || { labels: ['S1', 'S2', 'S3', 'S4', 'S5'], scores: [70, 78, 84, 88, 92] };

            new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Interview Readiness Score',
                        data: chartData.scores,
                        borderColor: '#6366F1',
                        backgroundColor: 'rgba(99, 102, 241, 0.15)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#A855F7',
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            min: 50,
                            max: 100,
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { color: '#9CA3AF' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#9CA3AF' }
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Failed to load dashboard stats chart:", err));
}

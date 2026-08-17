// ================================
// Prediction Trend Chart
// ================================

const trendCanvas = document.getElementById("ratingChart");

if (trendCanvas) {

    const chartData = window.dashboardData || {};

    new Chart(trendCanvas, {

        type: "line",

        data: {

            labels: chartData.trendLabels || [],

            datasets: [

                {

                    label: "Prediction Rating",

                    data: chartData.trendValues || [],

                    borderWidth: 3,

                    fill: true,

                    tension: 0.4

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {

                    min: 1,

                    max: 5

                }

            }

        }

    });

}

// ================================
// Rating Distribution Chart
// ================================

const pieCanvas = document.getElementById("pieChart");

if (pieCanvas) {

    const chartData = window.dashboardData || {};

    new Chart(pieCanvas, {

        type: "pie",

        data: {

            labels: chartData.ratingLabels || [],

            datasets: [

                {

                    data: chartData.ratingValues || []

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}
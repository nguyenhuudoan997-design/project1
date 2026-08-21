document.addEventListener("DOMContentLoaded", function () {

    console.log("================================");
    console.log("ANALYTICS JS");
    console.log("================================");


    // ==========================================
    // CHECK CHART.JS
    // ==========================================

    if (typeof Chart === "undefined") {

        console.error(
            "❌ Chart.js chưa được tải!"
        );

        return;
    }

    console.log(
        "✅ Chart.js:",
        Chart.version
    );


    // ==========================================
    // GET DATA
    // ==========================================

    const data = window.analyticsData || {};

    const trendLabels =
        data.trendLabels || [];

    const trendValues =
        data.trendValues || [];

    const ratingLabels =
        data.ratingLabels || [];

    const ratingValues =
        data.ratingValues || [];


    console.log(
        "Trend labels:",
        trendLabels
    );

    console.log(
        "Trend values:",
        trendValues
    );

    console.log(
        "Rating labels:",
        ratingLabels
    );

    console.log(
        "Rating values:",
        ratingValues
    );


    // ==========================================
    // TREND CHART
    // ==========================================

    const trendCanvas =
        document.getElementById("trendChart");


    if (!trendCanvas) {

        console.error(
            "❌ Không tìm thấy #trendChart"
        );

        return;
    }


    new Chart(
        trendCanvas,
        {

            type: "line",

            data: {

                labels: trendLabels,

                datasets: [

                    {

                        label: "Rating dự đoán",

                        data: trendValues,

                        borderWidth: 3,

                        tension: 0.4,

                        fill: false,

                        pointRadius: 5,

                        pointHoverRadius: 7

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    y: {

                        min: 0,

                        max: 5,

                        title: {

                            display: true,

                            text: "Rating"

                        }

                    },

                    x: {

                        title: {

                            display: true,

                            text: "Lần dự đoán"

                        }

                    }

                }

            }

        }
    );


    console.log(
        "✅ Trend chart đã được tạo"
    );


    // ==========================================
    // RATING DISTRIBUTION
    // ==========================================

    const ratingCanvas =
        document.getElementById("ratingChart");


    if (!ratingCanvas) {

        console.error(
            "❌ Không tìm thấy #ratingChart"
        );

        return;
    }


    new Chart(
        ratingCanvas,
        {

            type: "pie",

            data: {

                labels: ratingLabels,

                datasets: [

                    {

                        data: ratingValues

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

        }
    );


    console.log(
        "✅ Rating chart đã được tạo"
    );


    console.log(
        "================================"
    );

});
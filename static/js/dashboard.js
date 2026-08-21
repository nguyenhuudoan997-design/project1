document.addEventListener("DOMContentLoaded", function () {

    console.log("=================================");
    console.log("AI RATING PREDICTOR - DASHBOARD");
    console.log("=================================");


    // =====================================================
    // 1. KIỂM TRA CHART.JS
    // =====================================================

    if (typeof Chart === "undefined") {

        console.error("❌ Chart.js chưa được tải!");

        return;
    }

    console.log("✅ Chart.js đã được tải");
    console.log("Chart.js version:", Chart.version);


    // =====================================================
    // 2. KIỂM TRA DASHBOARD DATA
    // =====================================================

    if (typeof window.dashboardData === "undefined") {

        console.error(
            "❌ window.dashboardData không tồn tại!"
        );

        return;
    }

    console.log(
        "✅ window.dashboardData:",
        window.dashboardData
    );


    // =====================================================
    // 3. LẤY DỮ LIỆU TỪ FLASK
    // =====================================================

    const trendLabels =
        window.dashboardData.trendLabels || [];

    const trendValues =
        window.dashboardData.trendValues || [];

    const ratingLabels =
        window.dashboardData.ratingLabels || [];

    const ratingValues =
        window.dashboardData.ratingValues || [];


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


    // =====================================================
    // 4. KIỂM TRA DỮ LIỆU
    // =====================================================

    if (
        trendLabels.length === 0 ||
        trendValues.length === 0
    ) {

        console.warn(
            "⚠️ Không có dữ liệu Prediction Trend"
        );

    } else {

        console.log(
            "✅ Prediction Trend có dữ liệu"
        );
    }


    if (
        ratingLabels.length === 0 ||
        ratingValues.length === 0
    ) {

        console.warn(
            "⚠️ Không có dữ liệu Rating Distribution"
        );

    } else {

        console.log(
            "✅ Rating Distribution có dữ liệu"
        );
    }


    // =====================================================
    // 5. TREND CHART
    // =====================================================

    const trendCanvas =
        document.getElementById("trendChart");


    if (!trendCanvas) {

        console.error(
            "❌ Không tìm thấy canvas #trendChart"
        );

    } else {

        console.log(
            "✅ Đã tìm thấy #trendChart"
        );


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

                            pointRadius: 4,

                            pointHoverRadius: 6
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

                            beginAtZero: false,

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
                    },

                    plugins: {

                        legend: {

                            display: true,

                            position: "top"
                        },

                        tooltip: {

                            enabled: true
                        }
                    }
                }
            }
        );


        console.log(
            "✅ Trend Chart đã được tạo"
        );
    }


    // =====================================================
    // 6. RATING DISTRIBUTION CHART
    // =====================================================

    const ratingCanvas =
        document.getElementById("ratingChart");


    if (!ratingCanvas) {

        console.error(
            "❌ Không tìm thấy canvas #ratingChart"
        );

    } else {

        console.log(
            "✅ Đã tìm thấy #ratingChart"
        );


        new Chart(
            ratingCanvas,
            {
                type: "pie",

                data: {

                    labels: ratingLabels,

                    datasets: [

                        {
                            label: "Số lần dự đoán",

                            data: ratingValues,

                            borderWidth: 1
                        }

                    ]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom"
                        },

                        tooltip: {

                            enabled: true
                        }
                    }
                }
            }
        );


        console.log(
            "✅ Rating Distribution Chart đã được tạo"
        );
    }


    // =====================================================
    // 7. HOÀN TẤT
    // =====================================================

    console.log(
        "================================="
    );

    console.log(
        "✅ Dashboard Chart initialization completed"
    );

    console.log(
        "================================="
    );

});
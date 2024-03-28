document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.canvas-button').forEach(function (button) {
        button.addEventListener('click', function () {

            let navCanvasClasses = ['spent_by_month_card', 'spent_by_quarter_card', 'spent_by_year_card']

            // Iterate over each class name
            navCanvasClasses.forEach(function (navCanvasClass) {
                // Select the div element with the current class name
                let canvasElement = document.querySelector('#' + navCanvasClass);

                // Hide the div if it exists
                if (button.getAttribute('data-canvas') === navCanvasClass) {
                    canvasElement.style.display = 'block';
                    canvasElement.style.width = '500px';
                    canvasElement.style.height = '250px';
                }
                else
                    canvasElement.style.display = 'none';
            });


        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
// Sample data (replace with your actual data)
    const total_monthly_spending_data = {
        labels: Object.keys(spent_by_month_monthly),
        datasets: [{
            label: "הוצאות לפי חודש",
            data: Object.values(spent_by_month_monthly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

    const total_quarterly_spending_data = {
        labels: Object.keys(spent_by_month_quarterly),
        datasets: [{
            label: "הוצאות לפי רבעון",
            data: Object.values(spent_by_month_quarterly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

    const total_yearly_spending_data = {
        labels: Object.keys(spent_by_month_yearly),
        datasets: [{
            label: "הוצאות לפי שנה",
            data: Object.values(spent_by_month_yearly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

// Configure chart
    const spent_by_month_card_ctx = document.getElementById('spent_by_month_card').getContext('2d');
    new Chart(spent_by_month_card_ctx, {
        type: 'bar',
        data: total_monthly_spending_data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    // Configure chart
    const spent_by_quarter_card_ctx = document.getElementById('spent_by_quarter_card').getContext('2d');
    new Chart(spent_by_quarter_card_ctx, {
        type: 'bar',
        data: total_quarterly_spending_data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    // Configure chart
    const spent_by_year_card_ctx = document.getElementById('spent_by_year_card').getContext('2d');
    new Chart(spent_by_year_card_ctx, {
        type: 'bar',
        data: total_yearly_spending_data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });


    const spent_by_merchant_ctx = document.getElementById('spent_by_merchant').getContext('2d');

    // Sample data (replace with your actual data)
    const spent_by_merchant_data = {
        datasets: [{
            label: 'Transactions by Merchant',
            data: [
                {
                    x: 10, // Charge amount
                    y: 5,  // Number of transactions
                    r: 8,   // Bubble radius (adjust based on data range)
                    name: 'Grocery Store A'
                },
                {
                    x: 15,
                    y: 3,
                    r: 12,
                    name: 'Restaurant B'
                },
                {
                    x: 7,
                    y: 7,
                    r: 5,
                    name: 'Clothing Store C'
                }
            ],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
        }]
    };

    new Chart(spent_by_merchant_ctx, {
        type: 'bubble',
        data: spent_by_merchant_data,
        options: {
            scales: {
                x: {
                    title: 'Average Charge Amount'
                },
                y: {
                    title: 'Number of Transactions'
                }
            },
            plugins: {
                legend: {
                    labels: {
                        fontSize: 16
                    }
                }
            }
        }
    });


});
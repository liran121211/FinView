/* ----------------------- Outcome Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    let business_name = 0, business_category = 1, business_price = 2, business_date = 3;

    // Sample data
    const outcome_records = [
        ['Emirates', 'Transport', '- ₪349.99', 'Today'],
        ['ElAl', 'Transport', '- ₪100.0', 'Yesterday'],
        ['ElAl', 'Transport', '- ₪100.0', 'Yesterday']
    ];


    // Get the table body
    const tableBody = document.querySelector('#transactions-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    outcome_records.forEach(item => {
        const outcome_row = document.createElement('tr');
        const transaction_description_col = document.createElement('td');
        const transaction_amount_col = document.createElement('td');

        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        transaction_description_col.classList.add('transaction_description_col');
        transaction_amount_col.classList.add('transaction_amount_col');

        // Create div elements for word1 and word2
        const outcome_name = document.createElement('div');
        const outcome_category = document.createElement('div');
        const outcome_price = document.createElement('div');
        const outcome_date = document.createElement('div');

        // Set content and styling
        outcome_name.textContent = item[business_name];
        outcome_name.classList.add('outcome_name'); // Add the class for styling

        outcome_category.textContent = item[business_category];
        outcome_category.classList.add('outcome_category'); // Add the class for styling

        outcome_price.textContent = item[business_price];
        outcome_price.classList.add('outcome_price'); // Add the class for styling

        outcome_date.textContent = item[business_date];
        outcome_date.classList.add('outcome_date'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        transaction_description_col.appendChild(outcome_name);
        transaction_description_col.appendChild(outcome_category);

        transaction_amount_col.appendChild(outcome_price);
        transaction_amount_col.appendChild(outcome_date);

        // Append the cell to the row
        outcome_row.appendChild(transaction_description_col);
        outcome_row.appendChild(transaction_amount_col);

        // Append the row to the table body
        tableBody.appendChild(outcome_row);
    });
});


/* ----------------------- Income Table -----------------------*/
document.addEventListener('DOMContentLoaded', function () {
    let payer_name = 0, payer_category = 1, payer_amount = 2, payer_date = 3;

    // Sample data
    const income_records = [
        ['Elbit Systems LTD', 'Salary', '- ₪16,234', 'Today'],
        ['BIT', 'Money Transfer & Receive', '- ₪100.0', 'Yesterday']
    ];


    // Get the table body
    const tableBody = document.querySelector('#income-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    income_records.forEach(item => {
        const income_row = document.createElement('tr');
        const income_description_col = document.createElement('td');
        const income_amount_col = document.createElement('td');

        // Add the class name "income_description/income_amount" to the new <td> element
        income_description_col.classList.add('income_description_col');
        income_amount_col.classList.add('income_amount_col');

        // Create div elements for word1 and word2
        const income_name = document.createElement('div');
        const income_category = document.createElement('div');
        const income_amount = document.createElement('div');
        const income_date = document.createElement('div');

        // Set content and styling for word1 and word2
        income_name.textContent = item[payer_name];
        income_name.classList.add('income_name'); // Add the class for styling

        income_category.textContent = item[payer_category];
        income_category.classList.add('income_category'); // Add the class for styling

        income_amount.textContent = item[payer_amount];
        income_amount.classList.add('income_amount'); // Add the class for styling

        income_date.textContent = item[payer_date];
        income_date.classList.add('income_date'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        income_description_col.appendChild(income_name);
        income_description_col.appendChild(income_category);

        income_amount_col.appendChild(income_amount);
        income_amount_col.appendChild(income_date);

        // Append the cell to the row
        income_row.appendChild(income_description_col);
        income_row.appendChild(income_amount_col);

        // Append the row to the table body
        tableBody.appendChild(income_row);
    });
});


/* ----------------------- Balance History ----------------------- */
const balance_history_data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
        label: "Sample Data",
        borderColor: "rgb(75, 192, 192)",
        data: [10, 30, 20, 40, 50, 30, 60],
        fill: false
    }]
};

// Configuration options for the chart
const balance_history_config = {
    type: 'line',
    data: balance_history_data,
    options: {
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Month'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        }
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("balance-history-graph");
    // Create the chart with the provided configuration
    const balance_history_chart = new Chart(canvas, balance_history_config);
});


/* ----------------------- Spent By Category - Doughnut Graph ----------------------- */
document.addEventListener("DOMContentLoaded", function () {
    const spent_by_category_data = {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple"],
        datasets: [{
            label: "My First Dataset",
            data: [30, 10, 20, 15, 25],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
            ]
        }]
    };


    // Configuration options for the doughnut chart

    const spent_by_category_config = {
        type: 'doughnut',
        data: spent_by_category_data,
        options: {
            responsive: true,
            plugins: {
            },
            title: {
                display: true,
                text: 'הוצאות על פי קטגוריה',
                font: {
                    size: 24,
                    style: 'italic',
                    family: 'Helvetica Neue'
                }
            }
        },
    };

    Chart.defaults.global.legend.display = false;
    const spent_by_category_canvas = document.getElementById('upper-dashboard-doughnut-pie-canvas');
    // Create the doughnut chart with the provided configuration
    const doughnutChart = new Chart(spent_by_category_canvas, spent_by_category_config);
});

/* ----------------------- Upper Dashboard Doughnut Pie ----------------------- */
document.addEventListener("DOMContentLoaded", function () {
    var income_outcome_options_1 = {
        type: 'doughnut',
        data: {
            labels: ["Red", "Orange", "Green"],
            datasets: [
                {
                    label: '# of Votes',
                    data: [33, 33, 33],
                    backgroundColor: [
                        'rgba(231, 76, 60, 1)',
                        'rgba(255, 164, 46, 1)',
                        'rgba(46, 204, 113, 1)'
                    ],
                    borderColor: [
                        'rgba(255, 255, 255 ,1)',
                        'rgba(255, 255, 255 ,1)',
                        'rgba(255, 255, 255 ,1)'
                    ],
                    borderWidth: 5
                }
            ]
        },
        options: {
            rotation: Math.PI,
            circumference: Math.PI,
            legend: {
                display: false
            },
            tooltip: {
                enabled: false
            },
            cutoutPercentage: 95
        }
    }

    var io_doughnut_chart_1 = document.getElementById('income-outcome-half-doughnut-chart-1').getContext('2d');
    new Chart(io_doughnut_chart_1, income_outcome_options_1);

    var income_outcome_options_2 = {
        type: 'doughnut',
        data: {
            labels: ["", "Purple", ""],
            datasets: [
                {
                    data: [88.5, 1, 10.5],
                    backgroundColor: [
                        "rgba(0,0,0,0)",
                        "rgba(255,255,255,1)",
                        "rgba(0,0,0,0)",
                    ],
                    borderColor: [
                        'rgba(0, 0, 0 ,0)',
                        'rgba(46, 204, 113, 1)',
                        'rgba(0, 0, 0 ,0)'
                    ],
                    borderWidth: 3

                }]
        },
        options: {
            cutoutPercentage: 95,
            rotation: Math.PI,
            circumference: Math.PI,
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            }
        }
    }


    let io_doughnut_chart_2 = document.getElementById('income-outcome-half-doughnut-chart-2').getContext('2d');
    new Chart(io_doughnut_chart_2, income_outcome_options_2);
});

/* ----------------------- Categories List under Doughnut Pie Chart ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    let category = 0;

    // Sample data
    const categories = [
        'טיפוח ובריאות', 'אוכל', 'פנאי ובידור', 'תחבורה','ממשלה ועירייה'
    ];


    // Get the table body
    const tableBody = document.querySelector('#upper-dashboard-doughnut-pie-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    categories.forEach(item => {
        const category_row = document.createElement('tr');
        const category_col = document.createElement('td');

        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        category_col.classList.add('upper-dashboard-doughnut-pie-table-col');

        // Create div elements for word1 and word2
        const category_name = document.createElement('div');

        // Set content and styling
        category_name.textContent = item;
        category_name.classList.add('upper-dashboard-doughnut-pie-category-name'); // Add the class for styling


        // Add word1 and word2 divs to the cell
        category_col.appendChild(category_name);

        // Append the cell to the row
        category_row.appendChild(category_col);

        // Append the row to the table body
        tableBody.appendChild(category_row);
    });
});

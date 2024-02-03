
/* ----------------------- Outcome Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Get the table body
    const tableBody = document.querySelector('#transactions-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_outcome)[0]
    let numberOfDuplicates = user_outcome[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_outcome.transaction_type[i] !== 'הוצאה')
            continue;

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
        outcome_name.textContent = user_outcome.business_name[i];
        outcome_name.classList.add('outcome_name'); // Add the class for styling

        outcome_category.textContent = user_outcome.category[i];
        outcome_category.classList.add('outcome_category'); // Add the class for styling

        outcome_price.textContent = '- ₪' + Math.abs(user_outcome.total_amount[i]).toFixed(2).toLocaleString();
        outcome_price.classList.add('outcome_price'); // Add the class for styling

        outcome_date.textContent = user_outcome.date_of_transaction[i];
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
    }
});


/* ----------------------- Income Table -----------------------*/
document.addEventListener('DOMContentLoaded', function () {
    // Get the table body
    const tableBody = document.querySelector('#income-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_income)[0]
    let numberOfDuplicates = user_income[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_income.transaction_type[i] !== 'הכנסה')
            continue;

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
        income_name.textContent = user_income.business_name[i];
        income_name.classList.add('income_name'); // Add the class for styling

        income_category.textContent = user_income.category[i];
        income_category.classList.add('income_category'); // Add the class for styling

        income_amount.textContent = '+ ₪' + Math.abs(user_income.total_amount[i]).toFixed(2).toLocaleString();
        income_amount.classList.add('income_amount'); // Add the class for styling

        income_date.textContent = user_income.date_of_transaction[i];
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
    }
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
    const _ = new Chart(canvas, balance_history_config);
});


/* ----------------------- Quick Overview Doughnut-Pie - Doughnut Graph ----------------------- */
document.addEventListener("DOMContentLoaded", function () {
    const quick_overview_data = {
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

    const quick_overview_config = {
        type: 'outlabeledPie',
        data: quick_overview_data,
        options: {
            responsive: false,
            zoomOutPercentage: 55, // makes chart 40% smaller (50% by default, if the property is undefined)
            plugins: {
                legend: false,
                outlabels: {
                    text: '%l %p',
                    color: 'white',
                    stretch: 45,
                    font: {
                        resizable: true,
                        minSize: 12,
                        maxSize: 18
                    }
                }
            }
        }
    };



    const quick_overview_data_canvas_1 = document.getElementById('quick-overview-doughnut-pie-canvas-1');
    // Create the doughnut chart with the provided configuration
    const _1 = new Chart(quick_overview_data_canvas_1, quick_overview_config);

    const quick_overview_data_canvas_2 = document.getElementById('quick-overview-doughnut-pie-canvas-2');
    // Create the doughnut chart with the provided configuration
    const _2 = new Chart(quick_overview_data_canvas_2, quick_overview_config);

    const quick_overview_data_canvas_3 = document.getElementById('quick-overview-doughnut-pie-canvas-3');
    // Create the doughnut chart with the provided configuration
    const _3 = new Chart(quick_overview_data_canvas_3, quick_overview_config);
});

/* ----------------------- Income & Outcome Ratio Dashboard Doughnut Pie ----------------------- */
document.addEventListener("DOMContentLoaded", function () {
    let ior_options_1 = {
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
            plugins: {
                legend: false,
                outlabels: {
                    display: false,
                },
            },

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

    let ior_chart_1 = document.getElementById('income-outcome-half-doughnut-chart-1').getContext('2d');
    new Chart(ior_chart_1, ior_options_1);

    let ior_options_2 = {
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


    let ior_chart_2 = document.getElementById('income-outcome-half-doughnut-chart-2').getContext('2d');
    new Chart(ior_chart_2, ior_options_2);
});


/* ----------------------- Subscription & Direct Debit Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Get the table body
    const tableBody = document.querySelector('#subscriptions-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_payment_records)[0]
    let numberOfDuplicates = user_payment_records[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_payment_records.payment_type[i] !== 'Subscription')
            continue;

        const subscription_row = document.createElement('tr');
        const subscription_name_col = document.createElement('td');
        const subscription_price_col = document.createElement('td');

        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        subscription_price_col.classList.add('subscription-price-col');
        subscription_name_col.classList.add('subscription-name-col');


        // Create div elements for word1 and word2
        const subscription_price_div = document.createElement('div');
        const subscription_name_div = document.createElement('div');

        // Set content and styling
        subscription_price_div.textContent = '- ₪' + user_payment_records.amount[i].toFixed(2).toLocaleString();
        subscription_price_div.classList.add('subscription-price-div'); // Add the class for styling

        subscription_name_div.textContent = user_payment_records.provider_name[i];
        subscription_name_div.classList.add('subscription-name-div'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        subscription_price_col.appendChild(subscription_price_div);
        subscription_name_col.appendChild(subscription_name_div);

        // Append the cell to the row
        subscription_row.appendChild(subscription_price_col);
        subscription_row.appendChild(subscription_name_col);

        // Append the row to the table body
        tableBody.appendChild(subscription_row);
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Get the table body
    const tableBody = document.querySelector('#direct-debit-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_payment_records)[0]
    let numberOfDuplicates = user_payment_records[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_payment_records.payment_type[i] !== 'Direct Debit')
            continue;

        const direct_debit_row = document.createElement('tr');
        const direct_debit_price_col = document.createElement('td');
        const direct_debit_name_col = document.createElement('td');


        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        direct_debit_price_col.classList.add('direct-debit-price-col');
        direct_debit_name_col.classList.add('direct-debit-name-col');


        // Create div elements for word1 and word2
        const direct_debit_price_div = document.createElement('div');
        const direct_debit_name_div = document.createElement('div');


        // Set content and styling
        direct_debit_price_div.textContent = '- ₪' + user_payment_records.amount[i].toFixed(2).toLocaleString();
        direct_debit_price_div.classList.add('direct-debit-price-div'); // Add the class for styling

        direct_debit_name_div.textContent = user_payment_records.provider_name[i];
        direct_debit_name_div.classList.add('direct-debit-name-div'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        direct_debit_price_col.appendChild(direct_debit_price_div);
        direct_debit_name_col.appendChild(direct_debit_name_div);

        // Append the cell to the row
        direct_debit_row.appendChild(direct_debit_price_col);
        direct_debit_row.appendChild(direct_debit_name_col);

        // Append the row to the table body
        tableBody.appendChild(direct_debit_row);
    }
});


/* ----------------------- Credit Cards List ----------------------- */

document.addEventListener('DOMContentLoaded', function () {

    // Get the container element
    let container = document.querySelector('.cards-group');

    // check if at least 1 card has been found.
    if (Object.keys(user_cards).length === 0) {
        let no_cards_title = document.createElement('div');
        no_cards_title.classList.add('no-cards-title');
        no_cards_title.innerHTML = `<p> לא נמצאו כרטיסים פעילים :(</p>`;
        container.appendChild(no_cards_title);
        return;
    }

    // Define the number of times you want to duplicate the HTML
    let col_name = Object.keys(user_cards)[0]
    let numberOfDuplicates = user_cards[col_name].length;  // Change this value as needed

    // Loop to create and insert duplicated HTML
    for (let i = 0; i < numberOfDuplicates; i++) {
        // Create a new div element with class "cards-group"
        let new_card = document.createElement('div');
        new_card.classList.add('card');

        // Chose Card Type logo
        let card_type_logo = '';
        if (user_cards.card_type[i] === 'VISA')
        {
            card_type_logo = '<img class="logo" src="static/images/visa_logo.svg" alt="Card Type Logo">';
        }
        else
        {
            card_type_logo = '<img class="logo" src="static/images/mastercard_logo.svg" alt="NFC Logo">'
        }

        // Set the HTML content for the "cards-group" div
        new_card.innerHTML = `
            <div class="card-inner">
                    <div class="card-front">
                        <div class="card-bg"></div>
            
                        <div class="card-glow"></div>
                            <!-- Card Type Logo SVG  -->
                            ${card_type_logo}
                        <div class="card-contactless">
                            <!-- Contactless Logo SVG  -->
                            <img src="static/images/nfc_logo.svg" alt="NFC Logo">
                        </div>
                        <div class="card-issuer">${JSON.stringify(user_cards.issuer_name[i]).replace(/^"(.*)"$/, '$1')}</div>
                        <div class="card-chip"></div>
                        <div class="card-holder">${JSON.stringify(user_cards.full_name[i]).replace(/^"(.*)"$/, '$1')}</div>
                        <div class="card-number">${JSON.stringify(user_cards.last_four_digits[i]).replace(/^"(.*)"$/, '$1')} **** **** ****</div>
                        <div class="card-valid">--/--</div>
                    </div>
                    <div class="card-back">
                        <div class="card-signature">${JSON.stringify(user_cards.full_name[i]).replace(/^"(.*)"$/, '$1')}</div>
                        <div class="card-seccode">***</div>
                    </div>
                </div>
               `;

        // Append the "cards-group" div to the container
        container.appendChild(new_card);
    }
});

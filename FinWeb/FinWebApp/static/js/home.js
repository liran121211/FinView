/* ----------------------- Outcome Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // check if [user_outcome] was empty
    const empty_transactions_title = document.querySelector('#empty-transactions-description');
    if (Object.keys(user_outcome).length === 0) {
        empty_transactions_title.textContent = 'לא נמצאו הוצאות אחרונות';
        return;
    }

    // Get the table body
    const tableBody = document.querySelector('#transactions-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_outcome)[0]
    let numberOfDuplicates = user_outcome[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {

        const outcome_row = document.createElement('tr');
        const transaction_amount_col = document.createElement('td');
        const transaction_description_col = document.createElement('td');

        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        transaction_description_col.classList.add('transaction_description_col');
        transaction_amount_col.classList.add('transaction_amount_col');

        // Create div elements for word1 and word2
        const outcome_price = document.createElement('div');
        const outcome_date = document.createElement('div');
        const outcome_name = document.createElement('div');
        const outcome_category = document.createElement('div');


        // Set content and styling
        outcome_price.textContent = '- ₪' + intcomma(user_outcome.total_amount[i].toFixed(2).toLocaleString());
        outcome_price.classList.add('outcome_price'); // Add the class for styling

        outcome_date.textContent = user_outcome.date_of_transaction[i];
        outcome_date.classList.add('outcome_date'); // Add the class for styling

        outcome_name.textContent = user_outcome.business_name[i];
        outcome_name.classList.add('outcome_name'); // Add the class for styling

        outcome_category.textContent = user_outcome.transaction_category[i];
        outcome_category.classList.add('outcome_category'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        transaction_description_col.appendChild(outcome_name);
        transaction_description_col.appendChild(outcome_category);

        transaction_amount_col.appendChild(outcome_price);
        transaction_amount_col.appendChild(outcome_date);

        // Append the cell to the row
        outcome_row.appendChild(transaction_amount_col);
        outcome_row.appendChild(transaction_description_col);

        // Other background properties
        outcome_row.style.backgroundPosition = 'right';
        outcome_row.style.backgroundPositionY = '3px';
        outcome_row.style.backgroundRepeat = 'no-repeat';
        outcome_row.style.backgroundSize = '28px';

        switch (user_outcome.transaction_category[i]) {
            case 'ביטוח':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/insurance_logo.svg")';
                break;
            case 'מזון וצריכה':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/grocery_logo.svg")';
                break;
            case 'שרותי תקשורת':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/internet_communication_logo.svg")';
                break;
            case 'רפואה וקוסמטיקה':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/pharmacy_logo.svg")';
                break;
            case 'מחשבים, תוכנות וחשמל':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/electronics_logo.svg")';
                break;
            case 'פנאי ובידור':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/entertainment_logo.svg")';
                break;
            case 'עירייה וממשלה':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/municipal_government_logo.svg")';
                break;
            case 'תחבורה':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/transport_logo.svg")';
                break;
            case 'שונות':
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/other_logo.svg")';
                break;
            default:
                outcome_row.style.backgroundImage = 'url("static/images/credit_card_categories_icons/unknown_category_logo.svg")';
                break;
        }

        // Append the row to the table body
        tableBody.appendChild(outcome_row);

    }
});


/* ----------------------- Income Table -----------------------*/
document.addEventListener("DOMContentLoaded", function () {
    // check if [user_income] was empty
    const empty_income_title = document.querySelector('#empty-income-description');
    if (Object.keys(user_income).length === 0) {
        empty_income_title.textContent = 'לא נמצאו הכנסות אחרונות';
        return;
    }

    // Get the table body
    const tableBody = document.querySelector('#income-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_income)[0]
    let numberOfDuplicates = user_income[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {

        const income_row = document.createElement('tr');
        const income_description_col = document.createElement('td');
        const income_amount_col = document.createElement('td');

        // Add the class name "income_description/income_amount" to the new <td> element
        income_amount_col.classList.add('income_amount_col');
        income_description_col.classList.add('income_description_col');


        // Create div elements for word1 and word2
        const income_amount = document.createElement('div');
        const income_date = document.createElement('div');
        const income_name = document.createElement('div');
        const income_category = document.createElement('div');


        // Set content and styling for word1 and word2
        income_name.textContent = user_income.transaction_description[i];
        income_name.classList.add('income_name'); // Add the class for styling

        income_category.textContent = user_income.transaction_category[i];
        income_category.classList.add('income_category'); // Add the class for styling

        income_amount.textContent = '+ ₪' + intcomma((user_income.income_balance[i]).toFixed(2).toLocaleString());
        income_amount.classList.add('income_amount'); // Add the class for styling

        income_date.textContent = user_income.transaction_date[i];
        income_date.classList.add('income_date'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        income_description_col.appendChild(income_name);
        income_description_col.appendChild(income_category);

        income_amount_col.appendChild(income_amount);
        income_amount_col.appendChild(income_date);

        // Append the cell to the row
        income_row.appendChild(income_amount_col);
        income_row.appendChild(income_description_col);

        // Other background properties
        income_row.style.backgroundPosition = 'right';
        income_row.style.backgroundPositionY = '3px';
        income_row.style.backgroundRepeat = 'no-repeat';
        income_row.style.backgroundSize = '28px';

        switch (user_income.transaction_category[i]) {
            case 'הכנסה':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/income_logo.svg")';
                break;
            case 'הוצאה':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/outcome_logo.svg")';
                break;
            case 'חיסכון והשקעות':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/saving_investment_logo.svg")';
                break;
            case 'הלוואות':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/loan_logo.svg")';
                break;
            case 'עמלות':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/fee_logo.svg")';
                break;
            case 'העברות ומשיכות':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/transfer_withdraw_logo.svg")';
                break;
            case 'מיסים':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/taxes_logo.svg")';
                break;
            case 'שונות':
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/other_logo.svg")';
                break;
            default:
                income_row.style.backgroundImage = 'url("static/images/bank_categories_icons/unknown_category_logo.svg")';
                break;
        }

        // Append the row to the table body
        tableBody.appendChild(income_row);
    }
});


/* ----------------------- Balance History ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    const balance_history_data = {
        labels: Object.values(income_by_month.month_name),
        datasets: [{
            label: "הכנסות לפי חודש",
            borderColor: "rgb(75, 192, 192)",
            data: Object.values(income_by_month.total_amount),
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
                        text: 'חודש'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'ערך'
                    }
                }
            }
        }
    };


    // Create the chart with the provided configuration
    const canvas = document.getElementById("balance-history-graph");
    const _ = new Chart(canvas, balance_history_config);
});


/* ----------------------- Quick Overview Doughnut-Pie - Doughnut Graph ----------------------- */
document.addEventListener("DOMContentLoaded", function () {
    //define size by resolution:
    let screenWidthRatio = window.screen.width / 2560;
    let screenHeightRatio = window.screen.height / 1080;
    let pieChartSize = 50;

    // Spent by Category
    let spent_by_category_labels = Object.values(spent_by_category['transaction_category']);
    let spent_by_category_items = Object.values(spent_by_category['total_amount']);

    // Spent by Card Number
    let spent_by_card_labels_last_4_digits = Object.values(spent_by_card['last_4_digits']);
    let spent_by_card_labels_issuer_name = Object.values(spent_by_card['issuer_name']);
    let spent_by_card_items = Object.values(spent_by_card['total_amount']);
    let spent_by_card_labels = [];

    // Earned by Category
    let bank_transaction_by_category_labels = Object.values(bank_transaction_by_category['transaction_category']);
    let bank_transaction_by_category_items = Object.values(bank_transaction_by_category['total_amount']);

    // Iterate over one of the lists
    for (let i = 0; i < spent_by_card_labels_last_4_digits.length; i++) {
        // Concatenate 'issuer_name' and 'last_4_digits' at the same index
        let concatenatedItem = '(' + spent_by_card_labels_issuer_name[i] + ' ' + spent_by_card_labels_last_4_digits[i] + ')';
        // Push the concatenated item to the result list
        spent_by_card_labels.push(concatenatedItem);
    }

    const spent_by_category_data = {
        labels: spent_by_category_labels,
        datasets: [{
            data: spent_by_category_items,
            backgroundColor: getRandomColors(spent_by_category_items.length),
        }]
    };

    // Configuration options for the doughnut chart
    let spent_by_category_title = 'הוצאות לפי קטגוריה';
    let spent_by_category_font_color = '#4C495A';
    let spent_by_category_font_size = 22;
    if (Object.keys(spent_by_category['transaction_category']).length === 0) {
        spent_by_category_title = spent_by_category_title + ' (מידע לא זמין)';
        spent_by_category_font_color = '#C6C6C6';
        spent_by_category_font_size = 18;
    }

    const spent_by_category_config = {
        type: 'outlabeledPie',
        data: spent_by_category_data,
        options: {
            title: {
                display: true,
                text: spent_by_category_title,
                fontSize: spent_by_category_font_size,
                fontColor: spent_by_category_font_color,
                fontFamily: "'Gan', sans-serif",
            },
            responsive: false,
            zoomOutPercentage: pieChartSize, // makes chart 40% smaller (50% by default, if the property is undefined)

            plugins: {
                legend: false,
                outlabels: {
                    text: '%l %p',
                    color: 'white',
                    stretch: 45,
                    font: {
                        resizable: true,
                        minSize: 18,
                        maxSize: 25
                    }
                },
            }
        }
    };


    const spent_by_card_data = {
        labels: spent_by_card_labels,
        datasets: [{
            data: spent_by_card_items,
            backgroundColor: getRandomColors(spent_by_card_items.length),
        }]
    };

    // Configuration options for the doughnut chart
    let spent_by_card_title = 'הוצאות לפי כרטיס';
    let spent_by_card_font_color = '#4C495A';
    let spent_by_card_font_size = 22;
    if (Object.keys(spent_by_category['transaction_category']).length === 0) {
        spent_by_card_title = spent_by_card_title + ' (מידע לא זמין)';
        spent_by_card_font_color = '#C6C6C6';
        spent_by_card_font_size = 18;
    }

    const spent_by_card_config = {
        type: 'outlabeledPie',
        data: spent_by_card_data,
        options: {
            title: {
                display: true,
                text: spent_by_card_title,
                fontSize: spent_by_card_font_size,
                fontColor: spent_by_card_font_color,
                fontFamily: "'Gan', sans-serif",
            },
            responsive: false,
            zoomOutPercentage: pieChartSize, // makes chart 40% smaller (50% by default, if the property is undefined)

            plugins: {
                legend: false,
                outlabels: {
                    text: '%l %p',
                    color: 'white',
                    stretch: 45,
                    font: {
                        resizable: true,
                        minSize: 18,
                        maxSize: 25
                    }
                },
            }
        }
    };


    const bank_transaction_by_category_data = {
        labels: bank_transaction_by_category_labels,
        datasets: [{
            data: bank_transaction_by_category_items,
            backgroundColor: getRandomColors(bank_transaction_by_category_items.length),
        }]
    };

    let bank_transaction_by_category_title = 'תנועות בנק לפי קטגוריה';
    let bank_transaction_by_category_font_color = '#4C495A';
    let bank_transaction_by_category_font_size = 22;
    if (Object.keys(spent_by_category['transaction_category']).length === 0) {
        bank_transaction_by_category_title = bank_transaction_by_category_title + ' (מידע לא זמין)';
        bank_transaction_by_category_font_color = '#C6C6C6';
        bank_transaction_by_category_font_size = 18;
    }

    const bank_transaction_by_category_config = {
        type: 'outlabeledPie',
        data: bank_transaction_by_category_data,
        options: {
            title: {
                display: true,
                text: bank_transaction_by_category_title,
                fontSize: bank_transaction_by_category_font_size,
                fontColor: bank_transaction_by_category_font_color,
                fontFamily: "'Gan', sans-serif",
            },
            responsive: false,
            zoomOutPercentage: pieChartSize, // makes chart 40% smaller (50% by default, if the property is undefined)

            plugins: {
                legend: false,
                outlabels: {
                    text: '%l %p',
                    color: 'white',
                    stretch: 45,
                    font: {
                        resizable: true,
                        minSize: 18,
                        maxSize: 25
                    }
                },
            }
        }
    };

    const spent_by_category_canvas = document.getElementById('quick-overview-spent-by-category');
    // Create the doughnut chart with the provided configuration
    new Chart(spent_by_category_canvas, spent_by_category_config);

    const spent_by_card_canvas = document.getElementById('quick-overview-spent-by-card');
    // Create the doughnut chart with the provided configuration
    new Chart(spent_by_card_canvas, spent_by_card_config);

    const bank_transaction_by_category_canvas = document.getElementById('quick-overview-earned-by-category');
    // Create the doughnut chart with the provided configuration
    new Chart(bank_transaction_by_category_canvas, bank_transaction_by_category_config);
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

    let arrow_color, arrow_position_in_circle;
    let income_outcome_precent = document.querySelector('.income-outcome-half-doughnut-percent');
    if (income_against_outcome >= 0 && income_against_outcome <= 33.3) {
        arrow_color = 'rgba(46, 204, 113, 1)';
        arrow_position_in_circle = [250, 10];
        document.querySelector('.income-outcome-half-doughnut-percent').textContent = intcomma((income_against_outcome).toFixed(2).toLocaleString()) + '%';
    }
    if (income_against_outcome >= 33.3 && income_against_outcome <= 66.6) {
        arrow_color = 'rgba(255, 164, 46, 1)';
        arrow_position_in_circle = [11, 0.5];
        document.querySelector('.income-outcome-half-doughnut-percent').textContent = intcomma((income_against_outcome).toFixed(2).toLocaleString()) + '%';
    }

    if (income_against_outcome >= 66.6 && income_against_outcome <= 99.9) {
        arrow_color = 'rgba(231, 76, 60, 1)';
        arrow_position_in_circle = [1, 0.5];
        document.querySelector('.income-outcome-half-doughnut-percent').textContent = intcomma((income_against_outcome).toFixed(2).toLocaleString()) + '%';
    }

    if (income_against_outcome >= 99.9 && income_against_outcome <= 9999) {
        arrow_color = 'rgba(231, 76, 60, 1)';
        arrow_position_in_circle = [1, 1.0]
        income_outcome_precent.style.color = '#E74C3C';
        document.querySelector('.income-outcome-half-doughnut-percent').textContent = intcomma((income_against_outcome).toFixed(2).toLocaleString()) + '%';
    }

    if (income_against_outcome === -1) {
        arrow_color = 'rgba(46, 204, 113, 1)';
        arrow_position_in_circle = [250, 10];
        document.querySelector('.income-outcome-half-doughnut-title-2').style.display = 'none';
        document.querySelector('.income-outcome-half-doughnut-no-data-title').textContent = 'לא קיימים נתונים לחודש הנוכחי';
        document.querySelector('.income-outcome-half-doughnut-percent').textContent = '0.0%';
    }


    let ior_options_2 = {
        type: 'doughnut',
        data: {
            labels: ["", "Purple", ""],
            datasets: [
                {
                    data: [arrow_position_in_circle[0], arrow_position_in_circle[1], 10.5],
                    backgroundColor: [
                        "rgba(0,0,0,0)",
                        "rgba(255,255,255,1)",
                        "rgba(0,0,0,0)",
                    ],
                    borderColor: [
                        "rgba(0,0,0,0)",
                        arrow_color,
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
    // check if [user_subscriptions] was empty
    const empty_subscriptions_title = document.querySelector('#empty-subscriptions-description');
    if (Object.keys(user_direct_debit_subscriptions).length === 0) {
        empty_subscriptions_title.textContent = 'לא נמצאו תשלומים פעילים';
        return;
    }

    // Get the table body
    const tableBody = document.querySelector('#subscriptions-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_direct_debit_subscriptions)[0]
    let numberOfDuplicates = user_direct_debit_subscriptions[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_direct_debit_subscriptions.payment_type[i] !== 'עסקת תשלומים')
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
        subscription_price_div.textContent = '₪' + intcomma(user_direct_debit_subscriptions.amount[i].toFixed(2).toLocaleString());
        subscription_price_div.classList.add('subscription-price-div'); // Add the class for styling

        subscription_name_div.textContent = user_direct_debit_subscriptions.provider_name[i];
        subscription_name_div.classList.add('subscription-name-div'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        subscription_name_col.appendChild(subscription_name_div);
        subscription_price_col.appendChild(subscription_price_div);

        // Append the cell to the row
        subscription_row.appendChild(subscription_name_col);
        subscription_row.appendChild(subscription_price_col);

        // Append the row to the table body
        tableBody.appendChild(subscription_row);
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // check if [user_subscriptions] was empty
    const empty_direct_debit_title = document.querySelector('#empty-direct-debit-description');
    if (Object.keys(user_direct_debit_subscriptions).length === 0) {
        empty_direct_debit_title.textContent = 'לא נמצאו הוראות קבע פעילות';
        return;
    }

    // Get the table body
    const tableBody = document.querySelector('#direct-debit-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_direct_debit_subscriptions)[0]
    let numberOfDuplicates = user_direct_debit_subscriptions[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {
        if (user_direct_debit_subscriptions.payment_type[i] !== 'הוראת קבע')
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
        direct_debit_price_div.textContent = '₪' + intcomma(user_direct_debit_subscriptions.amount[i].toFixed(2).toLocaleString());
        direct_debit_price_div.classList.add('direct-debit-price-div'); // Add the class for styling

        direct_debit_name_div.textContent = user_direct_debit_subscriptions.provider_name[i];
        direct_debit_name_div.classList.add('direct-debit-name-div'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        direct_debit_name_col.appendChild(direct_debit_name_div);
        direct_debit_price_col.appendChild(direct_debit_price_div);

        // Append the cell to the row
        direct_debit_row.appendChild(direct_debit_name_col);
        direct_debit_row.appendChild(direct_debit_price_col);

        // Append the row to the table body
        tableBody.appendChild(direct_debit_row);
    }
});


/* ----------------------- Credit Cards List ----------------------- */

document.addEventListener('DOMContentLoaded', function () {

    // Get the container element
    const container = document.querySelector('.cards-group');

    // check if no cards has been found.
    if (Object.keys(user_cards).length === 0) {
        document.querySelector('.dashboard-container').style.marginTop = '-100px';
        const no_cards_description = document.querySelector('#no-cards-description');
        no_cards_description.textContent = ` לא נמצאו כרטיסים פעילים :(`;
        return;
    } else {
        document.querySelector('#no-cards-description').style.display = 'none';
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
        if (user_cards.card_type[i] === 'Visa')
            card_type_logo = '<img class="logo" src="static/images/visa_logo.svg" alt="Card Type Logo">';

        if (user_cards.card_type[i] === 'MasterCard')
            card_type_logo = '<img class="logo" src="static/images/mastercard_logo.svg" alt="Card Type Logo">';

        if (user_cards.card_type[i] === 'Unknown')
            card_type_logo = '<img class="logo" src="static/images/unknown_card_type_logo.svg" alt="Card Type Logo" width="15px" height="15px">';

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
                        <div class="card-number">${JSON.stringify(user_cards.last_4_digits[i]).replace(/^"(.*)"$/, '$1')} **** **** ****</div>
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

    // set scroll bar credit cards grid
    container.addEventListener('wheel', (e) => {
        container.scrollTo({
            top: container.scrollTop + e.deltaY,
            behavior: 'smooth'
        });
    });
});

/* ----------------------- Misc Functions ----------------------- */

function getRandomColors(numColors) {
    const interpolatedColors = [
        '#7BD92E',
        '#8FD931',
        '#A4DA35',
        '#B8DB39',
        '#FFD64D',
        '#FFCC53',
        '#FFC159',
        '#FFB75F',
        '#FFAC65',
        '#FFA26B',
        '#FF9871',
        '#FF8D77',
        '#FF837D',
        '#1A87D9',
        '#3380DC',
        '#4C89DF',
        '#6582E2',
        '#7E8BE5',
        '#9784E8',
        '#B07DEB',
        '#C977EE',
        '#E270F1'

    ];
    const randomColors = [];

    for (let i = 0; i < numColors; i++) {
        const randomIndex = Math.floor(Math.random() * interpolatedColors.length); // Generate a random index
        const randomColor = interpolatedColors.splice(randomIndex, 1)[0]; // Remove the color at the random index and add it to the result array
        randomColors.push(randomColor);
    }

    return randomColors;
}


function intcomma(number) {
    // Convert the number to a string
    number = number.toString();

    // Split the string into integer and decimal parts
    let parts = number.split(".");
    let integerPart = parts[0];
    let decimalPart = parts.length > 1 ? "." + parts[1] : "";

    // Add commas to the integer part
    let formattedInteger = "";
    for (let i = integerPart.length - 1, j = 1; i >= 0; i--, j++) {
        formattedInteger = integerPart.charAt(i) + formattedInteger;
        if (j % 3 === 0 && i > 0) {
            formattedInteger = "," + formattedInteger;
        }
    }

    // Concatenate the integer and decimal parts
    return formattedInteger + decimalPart;
}
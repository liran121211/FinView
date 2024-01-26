/* Outcome Table */
document.addEventListener('DOMContentLoaded', function () {
let business_name = 0, business_category = 1, business_price = 2, business_date = 3;

    // Sample data
    const outcome_records = [
        ['Emirates', 'Transport', '- ₪349.99', 'Today'],
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


/* Income Table */
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
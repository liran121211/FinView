document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.nav-span').forEach(function (span) {
        span.addEventListener('click', function () {

            let navDivClasses = ['personal-details-div', 'credit-cards-details-div', 'credit-cards-transactions-div']

            // Iterate over each class name
            navDivClasses.forEach(function (navDivClass) {
                // Select the div element with the current class name
                let divElement = document.querySelector('.' + navDivClass);

                // Hide the div if it exists
                if (span.getAttribute('data-div') === navDivClass)
                    divElement.style.display = 'block';
                else
                    divElement.style.display = 'none';
            });


        });
    });
});

/* ----------------------- Credit Cards Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // check if [user_outcome] was empty
    const empty_credit_cards_title = document.querySelector('#empty-transactions-description');
    if (Object.keys(user_cards).length === 0) {
        empty_credit_cards_title.textContent = 'לא נמצאו כרטיסים בחשבון';
        return;
    }

    // Get the table body
    const tableBody = document.querySelector('#credit-cards-table tbody');

    // Clear any existing content
    tableBody.innerHTML = '';

    // Populate the table with data
    let col_name = Object.keys(user_cards)[0]
    let numberOfDuplicates = user_cards[col_name].length;  // Change this value as needed
    for (let i = 0; i < numberOfDuplicates; i++) {

        const credit_card_row = document.createElement('tr');
        const credit_card_type_col = document.createElement('td');
        const credit_card_issuer_name_col = document.createElement('td');
        const credit_card_last_4_digits_col = document.createElement('td');

        // Add the class name "outcome_description/outcome_amount" to the new <td> element
        credit_card_type_col.classList.add('credit-card_type-col');
        credit_card_issuer_name_col.classList.add('credit-card_issuer-name-col');
        credit_card_last_4_digits_col.classList.add('credit-card-last-4-digits-col');

        // Create div elements for word1 and word2
        const credit_card_type = document.createElement('div');
        const credit_card_issuer_name = document.createElement('div');
        const credit_card_last_4_digits = document.createElement('div');


        // Set content and styling
        credit_card_type.textContent = user_cards.card_type[i];
        credit_card_type.id = user_cards.sha1_identifier[i];
        credit_card_type.classList.add('credit-card-type'); // Add the class for styling


        credit_card_issuer_name.textContent = user_cards.issuer_name[i];
        credit_card_issuer_name.classList.add('credit-card-issuer-name'); // Add the class for styling

        credit_card_last_4_digits.textContent = user_cards.last_4_digits[i];
        credit_card_last_4_digits.classList.add('credit-card-last-4-digits'); // Add the class for styling

        // Add word1 and word2 divs to the cell
        credit_card_type_col.appendChild(credit_card_type);
        credit_card_issuer_name_col.appendChild(credit_card_issuer_name);
        credit_card_last_4_digits_col.appendChild(credit_card_last_4_digits);


        // Append the cell to the row
        credit_card_row.appendChild(credit_card_last_4_digits_col);
        credit_card_row.appendChild(credit_card_issuer_name_col);
        credit_card_row.appendChild(credit_card_type_col);

        // Append the row to the table body
        tableBody.appendChild(credit_card_row);

    }


    // Define the options for the combo box
    const creditCardTypes = ['VISA', 'MasterCard', 'Dinners Club', 'American Express', 'Discover', 'Isracard'];

    // Select the table
    const creditCardsTable = document.getElementById('credit-cards-table');

    // Add event listener to the table
    creditCardsTable.addEventListener('dblclick', event => {
        const target = event.target; // Get the clicked element

        // Check if the clicked element is a table cell (td) with the class 'credit-card-type'
        if (target.classList.contains('credit-card-type')) {
            const originalContent = target.innerHTML; // Store the original content

            // Create a combo box (select element)
            const selectBox = document.createElement('select');

            // Populate the combo box with options
            creditCardTypes.forEach(cardType => {
                const optionElement = document.createElement('option');
                optionElement.textContent = cardType;
                selectBox.appendChild(optionElement);
            });

            // Set the initial selected option
            selectBox.value = originalContent.trim();

            // Add event listener to save changes when an option is selected
            selectBox.addEventListener('change', () => {
                target.innerHTML = selectBox.value;
            });

            // Add event listener to cancel editing on pressing Escape
            selectBox.addEventListener('keyup', e => {
                if (e.key === 'Escape') {
                    // Cancel editing and restore the original content
                    target.innerHTML = originalContent;
                }
            });

            // Replace the cell content with the combo box
            target.innerHTML = '';
            target.appendChild(selectBox);

            // Focus on the combo box
            selectBox.focus();


            // Add event listener to the combo box
            selectBox.addEventListener('change', () => {
                const selectedOption = selectBox.value;
                const url = '/settings/submit_user_cards';
                const data = new FormData();
                data.append('selected_card_type', selectedOption);
                data.append('sha1_identifier', target.id);

                // Make an AJAX POST request
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
                        'X-Requested-With': 'XMLHttpRequest' // Custom header to indicate AJAX request
                    },
                    body: data
                })
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            // Handle the case where the server indicates failure
                            showFailStatus("עדכון מידע נכשל");
                        } else {
                            // Handle the case where the server indicates success
                            showSuccessStatus("השינויים עודכנו בהצלחה");
                        }
                    })
                    .catch(_ => {
                        showFailStatus("עדכון מידע נכשל");
                    });
            });
        }
    });

});


/* ----------------------- Credit Cards Transactions Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Check if user_cards is empty
    const emptyCreditCardsTitle = document.querySelector('#empty-transactions-description');
    if (Object.keys(user_cards).length === 0) {
        emptyCreditCardsTitle.textContent = 'לא נמצאו עסקאות אשראי';
        return;
    }

    const tableBody = document.querySelector('#credit-cards-transactions-table tbody');
    const itemsPerPage = 10;
    let currentPage = 1;

    const colName = Object.keys(credit_cards_transactions)[0];
    const numberOfDuplicates = credit_cards_transactions[colName].length;
    const totalPages = Math.ceil(numberOfDuplicates / itemsPerPage);

    function createTableCell(content, className) {
        const cell = document.createElement('td');
        cell.classList.add(className);
        const div = document.createElement('div');
        div.textContent = content;
        div.classList.add(className.replace('-col', ''));
        cell.appendChild(div);
        return cell;
    }

    function renderTable(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, numberOfDuplicates);
        tableBody.innerHTML = '';

        for (let i = startIndex; i < endIndex; i++) {
            const row = document.createElement('tr');

            row.appendChild(createTableCell(credit_cards_transactions.last_4_digits[i], 'last-4-digits-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_category[i], 'transaction-category-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_type[i], 'transaction-type-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_provider[i], 'transaction-provider-col'));
            row.appendChild(createTableCell(credit_cards_transactions.total_amount[i], 'total-amount-col'));
            row.appendChild(createTableCell(credit_cards_transactions.charge_amount[i], 'charge-amount-col'));
            row.appendChild(createTableCell(credit_cards_transactions.business_name[i], 'business-name-col'));
            row.appendChild(createTableCell(credit_cards_transactions.date_of_transaction[i], 'date-of-transaction-col'));

            tableBody.appendChild(row);
        }
    }

    function renderPagination() {
        const pagination = document.getElementById("credit-cards-transactions-pagination");
        pagination.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const pageLink = document.createElement('a');
            pageLink.href = '#';
            pageLink.textContent = i;
            if (i === currentPage) {
                pageLink.classList.add('active');
            }
            pageLink.addEventListener('click', function (event) {
                event.preventDefault();
                currentPage = i;
                renderTable(currentPage);
                renderPagination();
            });
            pagination.appendChild(pageLink);
        }
    }

    renderTable(currentPage);
    renderPagination();
});


// Function to get CSRF cookie value
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the provided name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to show success status message
function showSuccessStatus(message) {
    const successStatusElement = document.querySelector('.settings-modification-block-success-status');
    successStatusElement.textContent = message;
    successStatusElement.style.display = 'block';
    setTimeout(() => {
        successStatusElement.style.display = 'none';
    }, 2000);


}

// Function to show fail status message
function showFailStatus(message) {
    const failStatusElement = document.querySelector('.settings-modification-block-fail-status');
    failStatusElement.textContent = message;
    failStatusElement.style.display = 'block';
    setTimeout(() => {
        failStatusElement.style.display = 'none';
    }, 2000);
}
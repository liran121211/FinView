/* ----------------------- Transaction Mode Selection ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Select the container div
    let container = document.querySelector('.transactions-mode-selection');

    // Define the number of credit card selection boxes to add
    const numberOfButtons = 2;
    const buttonName = ['תנועות אשראי', 'תנועות בנק']

    // Loop to create and append the required number of credit card selection boxes
    for (let i = 0; i < numberOfButtons; i++) {
        // Create a new div element for the credit card selection box
        const newButton = document.createElement('div');
        newButton.classList.add('mode-selection');
        newButton.setAttribute('button-idx', i);

        // Create a paragraph element for the text
        const paragraph = document.createElement('p');
        paragraph.textContent = `${buttonName[i]}`;

        // Append the paragraph element to the new box
        newButton.appendChild(paragraph);

        // Append the new box to the container
        container.appendChild(newButton);
    }


        // Select all divs with the class 'credit-card-selection-box'
    const divs = document.querySelectorAll('.mode-selection');

    // Add click event listener to each div
    divs.forEach(div => {
        div.addEventListener('click', () => {
            // Check if the div already has 'clicked' class
            const alreadyClicked = div.classList.contains('clicked');

            let creditCardsMode = document.querySelector(".credit-cards-transactions-div");
            let bankMode = document.querySelector(".bank-transactions-div");
            if (div.getAttribute("button-idx") === '0') {
                creditCardsMode.style.display = 'block';
                bankMode.style.display = 'none';
            }
            if (div.getAttribute("button-idx") === '1') {
                bankMode.style.display = 'block';
                creditCardsMode.style.display = 'none';
            }

            // Remove 'clicked' class from all divs
            divs.forEach(divElement => {
                divElement.classList.remove('clicked');
            });

            // If the div was already clicked, do nothing
            if (!alreadyClicked) {
                // Add 'clicked' class to the clicked div
                div.classList.add('clicked');
            } //end if|(alreadyClicked)
        }) //end addEventListener()
    }); //end forEach()

}); //end DOMContentLoaded()

/* ----------------------- Credit Cards Transactions Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Check if credit_cards_transactions is empty
    const emptyCreditCardsTitle = document.querySelector('#empty-credit-cards-transactions-description');
    if (Object.keys(credit_cards_transactions).length === 0) {
        emptyCreditCardsTitle.textContent = 'לא נמצאו עסקאות אשראי';
        return;
    }

    const tableBody = document.querySelector('#credit-cards-transactions-table tbody');

    function createTableCell(content, className) {
        const cell = document.createElement('td');
        cell.classList.add(className);
        const div = document.createElement('div');


        div.textContent = content;
        div.classList.add(className.replace('-col', ''));
        cell.appendChild(div);
        return cell;
    }

    function renderTable() {
        const colName = Object.keys(credit_cards_transactions)[0];
        const numberOfRows = credit_cards_transactions[colName].length;
        tableBody.innerHTML = '';

        for (let i = 0; i < numberOfRows; i++) {
            const row = document.createElement('tr');
            row.appendChild(createTableCell(credit_cards_transactions.last_4_digits[i], 'last-4-digits-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_category[i], 'credit-card-transaction-category-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_type[i], 'transaction-type-col'));
            row.appendChild(createTableCell(credit_cards_transactions.transaction_provider[i], 'credit-card-transaction-provider-col'));
            row.appendChild(createTableCell(credit_cards_transactions.total_amount[i], 'total-amount-col'));
            row.appendChild(createTableCell(credit_cards_transactions.charge_amount[i], 'charge-amount-col'));
            row.appendChild(createTableCell(credit_cards_transactions.business_name[i], 'business-name-col'));
            row.appendChild(createTableCell(credit_cards_transactions.date_of_transaction[i], 'date-of-transaction-col'));
            tableBody.appendChild(row);
        }
    }
    renderTable();


    document.getElementById("searchbox-transactions").addEventListener("input", function () {
        const last_4_digits =           0
        const transaction_category =    1
        const transaction_type =        2
        const transaction_provider =    3
        const transaction_total =       4
        const transaction_amount =      5
        const business_name =           6
        const transaction_date =        7

        let filterValue = this.value.toLowerCase();
        let table = document.getElementById("credit-cards-transactions-table");
        let rows = table.getElementsByTagName("tr");

        if (filterValue.length === 0)
            for (let i = 1; i < rows.length; i++)  // Start from index 1 to skip the header row
                rows[i].style.display = "";

        // Loop through all table rows, and hide those that don't match the search query
        for (let i = 1; i < rows.length; i++) { // Start from index 1 to skip the header row
            let r_last_4_digits         = rows[i].getElementsByTagName("td")[last_4_digits];
            let r_transaction_category  = rows[i].getElementsByTagName("td")[transaction_category];
            let r_transaction_type      = rows[i].getElementsByTagName("td")[transaction_type];
            let r_transaction_provider  = rows[i].getElementsByTagName("td")[transaction_provider];
            let r_transaction_total     = rows[i].getElementsByTagName("td")[transaction_total];
            let r_transaction_amount    = rows[i].getElementsByTagName("td")[transaction_amount];
            let r_business_name         = rows[i].getElementsByTagName("td")[business_name];
            let r_transaction_date      = rows[i].getElementsByTagName("td")[transaction_date];
            if (r_last_4_digits || r_transaction_category || r_transaction_type || r_transaction_provider || r_transaction_total || r_transaction_amount || r_business_name || r_transaction_date) {
                if (r_last_4_digits.textContent.toLowerCase().indexOf(filterValue) > -1         ||
                    r_transaction_category.textContent.toLowerCase().indexOf(filterValue) > -1  ||
                    r_transaction_type.textContent.toLowerCase().indexOf(filterValue) > -1      ||
                    r_transaction_provider.textContent.toLowerCase().indexOf(filterValue) > -1  ||
                    r_transaction_total.textContent.toLowerCase().indexOf(filterValue) > -1     ||
                    r_transaction_amount.textContent.toLowerCase().indexOf(filterValue) > -1    ||
                    r_business_name.textContent.toLowerCase().indexOf(filterValue) > -1         ||
                    r_transaction_date.textContent.toLowerCase().indexOf(filterValue) > -1)
                {
                    rows[i].style.display = "";
                }
                else
                {
                    rows[i].style.display = "none";
                }
            }
        }
    });
});

/* ----------------------- Bank Transactions Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Check if credit_cards_transactions is empty
    const emptyBankTitle = document.querySelector('#empty-bank-transactions-description');
    if (Object.keys(bank_transactions).length === 0) {
        emptyBankTitle.textContent = 'לא נמצאו תנועות בנק';
        return;
    }

    const tableBody = document.querySelector('#bank-transactions-table tbody');

    function createTableCell(content, className) {
        const cell = document.createElement('td');
        cell.classList.add(className);
        const div = document.createElement('div');


        div.textContent = content;
        div.classList.add(className.replace('-col', ''));
        cell.appendChild(div);
        return cell;
    }

    function renderTable() {
        const colName = Object.keys(bank_transactions)[0];
        const numberOfRows = bank_transactions[colName].length;
        tableBody.innerHTML = '';

        for (let i = 0; i < numberOfRows; i++) {
            const row = document.createElement('tr');
            row.appendChild(createTableCell(bank_transactions.account_number[i], 'account-number-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_category[i], 'bank-transaction-category-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_reference[i], 'transaction-reference-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_provider[i], 'bank-transaction-provider-col'));
            row.appendChild(createTableCell(bank_transactions.current_balance[i], 'current-balance-col'));
            row.appendChild(createTableCell(bank_transactions.outcome_balance[i], 'outcome-balance-col'));
            row.appendChild(createTableCell(bank_transactions.income_balance[i], 'income-balance-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_description[i], 'transaction-description-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_date[i], 'transaction-date-col'));
            tableBody.appendChild(row);
        }
    }
    renderTable();


    document.getElementById("searchbox-transactions").addEventListener("input", function () {
        const transaction_category =      0
        const transaction_reference =     1
        const account_number =            2
        const transaction_provider =      3
        const current_balance =           4
        const outcome_balance =           5
        const income_balance =            6
        const transaction_description =   7
        const transaction_date =          8

        let filterValue = this.value.toLowerCase();
        let table = document.getElementById("bank-transactions-table");
        let rows = table.getElementsByTagName("tr");

        if (filterValue.length === 0)
            for (let i = 1; i < rows.length; i++)  // Start from index 1 to skip the header row
                rows[i].style.display = "";

        // Loop through all table rows, and hide those that don't match the search query
        for (let i = 1; i < rows.length; i++) { // Start from index 1 to skip the header row
            let r_transaction_category          = rows[i].getElementsByTagName("td")[transaction_category];
            let r_transaction_reference         = rows[i].getElementsByTagName("td")[transaction_reference];
            let r_account_number                = rows[i].getElementsByTagName("td")[account_number];
            let r_transaction_provider          = rows[i].getElementsByTagName("td")[transaction_provider];
            let r_current_balance               = rows[i].getElementsByTagName("td")[current_balance];
            let r_outcome_balance               = rows[i].getElementsByTagName("td")[outcome_balance];
            let r_income_balance                = rows[i].getElementsByTagName("td")[income_balance];
            let r_transaction_description       = rows[i].getElementsByTagName("td")[transaction_description];
            let r_transaction_date              = rows[i].getElementsByTagName("td")[transaction_date];
            if (r_transaction_category || r_transaction_reference || r_account_number || r_transaction_provider || r_current_balance || r_outcome_balance || r_income_balance || r_transaction_description || r_transaction_date) {
                if (r_transaction_category.textContent.toLowerCase().indexOf(filterValue) > -1          ||
                    r_transaction_reference.textContent.toLowerCase().indexOf(filterValue) > -1         ||
                    r_account_number.textContent.toLowerCase().indexOf(filterValue) > -1                ||
                    r_transaction_provider.textContent.toLowerCase().indexOf(filterValue) > -1          ||
                    r_transaction_provider.textContent.toLowerCase().indexOf(filterValue) > -1          ||
                    r_current_balance.textContent.toLowerCase().indexOf(filterValue) > -1               ||
                    r_outcome_balance.textContent.toLowerCase().indexOf(filterValue) > -1               ||
                    r_income_balance.textContent.toLowerCase().indexOf(filterValue) > -1                ||
                    r_transaction_description.textContent.toLowerCase().indexOf(filterValue) > -1       ||
                    r_transaction_date.textContent.toLowerCase().indexOf(filterValue) > -1)
                {
                    rows[i].style.display = "";
                }
                else
                {
                    rows[i].style.display = "none";
                }
            }
        }
    });
});
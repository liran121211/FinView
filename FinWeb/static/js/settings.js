/* ----------------------- Settings Panel ----------------------- */
document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.nav-span').forEach(function (span) {
        span.addEventListener('click', function () {

            let navDivClasses = ['personal-details-div', 'credit-cards-details-div', 'credit-cards-transactions-div', 'bank-transactions-div', 'upload-files-div',]

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


/* ----------------------- Personal Details ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Function to handle portrait file selection and preview
    function handleFileSelect(event) {
        let p_file = event.target.files[0];
        let p_canvas = document.getElementById('profile-pic');
        let p_ctx = p_canvas.getContext('2d');

        let p_reader = new FileReader();
        p_reader.onload = function (e) {
            let p_img = new Image();
            p_img.onload = function () {
                // Clear the canvas
                p_ctx.clearRect(0, 0, p_canvas.width, p_canvas.height);
                p_ctx.save();
                p_ctx.beginPath();
                p_ctx.arc(p_canvas.width / 2, p_canvas.height / 2, p_canvas.width / 2, 0, Math.PI * 2, true);
                p_ctx.closePath();
                p_ctx.clip(); // Clip the canvas to the circular path
                p_ctx.drawImage(p_img, 0, 0, p_canvas.width, p_canvas.height); // Draw the image within the circular path
                p_ctx.restore(); // Restore the previous canvas state
            };
            p_img.src = e.target.result;

            // Update portrait via AJAX
            updateProfilePic(); // Pass the image data to the function
        };

        p_reader.readAsDataURL(p_file);
    }

    function updateProfilePic() {
        // Assume canvas is your canvas element
        let canvas = document.getElementById('profile-pic');

        // Convert canvas to data URL
        let imageData = canvas.toDataURL();

        // Send the data to Django backend using AJAX
        fetch('/settings/submit_personal_information', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token in the headers
            },
            body: JSON.stringify({image_data: imageData}),
        })
            .then(response => {
                if (response.ok) {
                    console.log('Image uploaded successfully');
                } else {
                    console.error('Image upload failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Add click event listener to the upload button
    document.getElementById('portrait-change-btn').addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default form submission behavior
        document.getElementById('portrait-change-input').click(); // Trigger file input click event
    });

    // Add onchange event listener to file input
    document.getElementById('portrait-change-input').addEventListener('change', handleFileSelect, false);

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
                            showFailStatus("עדכון מידע נכשל", '.settings-modification-block-fail-status');
                        } else {
                            // Handle the case where the server indicates success
                            showSuccessStatus('השינויים עודכנו בהצלחה', "'.settings-modification-block-success-status'");
                        }
                    })
                    .catch(_ => {
                        showFailStatus("עדכון מידע נכשל", "'.settings-modification-block-fail-status'");
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


    // Object to track sort state for each column
    const sortState = {
        date_of_transaction: 'asc',
        business_name: 'asc',
        charge_amount: 'asc',
        total_amount: 'asc',
        transaction_provider: 'asc',
        transaction_type: 'asc',
        transaction_category: 'asc',
        last_4_digits: 'asc'
    };

    const name_conversion = {
        '4 ספרות אחרונות': 'last_4_digits',
        'קטגוריה': 'transaction_category',
        'סוג העסקה': 'transaction_type',
        'ספק העסקה': 'transaction_provider',
        'סכום העסקה': 'total_amount',
        'סכום חיוב': 'charge_amount',
        'שם בית העסק': 'business_name',
        'תאריך עסקה': 'date_of_transaction'
    }

    // Function to sort transactions based on a column
    function sortByColumn(column) {
        const isAscending = sortState[column] === 'asc';
        const multiplier = isAscending ? 1 : -1;

        // Sort the data array based on the selected column
        credit_cards_transactions[column].sort((valueA, valueB) => {
            // Check if both values are numbers
            if (!isNaN(valueA) && !isNaN(valueB)) {
                return (valueA - valueB) * multiplier; // Numeric comparison
            } else {
                // Use localeCompare for string comparison
                return valueA.localeCompare(valueB) * multiplier;
            }
        });

        // Reverse the sort order for the column
        sortState[column] = isAscending ? 'desc' : 'asc';
    }

    // Function to handle click events on column headers
    function handleColumnHeaderClick(event) {
        const columnHeader = event.target;
        const column = name_conversion[columnHeader.textContent];
        sortByColumn(column);
        renderTable(currentPage);
    }

    // Add click event listeners to column headers
    const columnHeaderElements = document.querySelectorAll('#credit-cards-transactions-table th');
    columnHeaderElements.forEach(columnHeader => {
        columnHeader.addEventListener('click', handleColumnHeaderClick);
    });


});


/* ----------------------- Bank Transactions Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Check if user_cards is empty
    const emptyBankTitle = document.querySelector('#empty-transactions-description');
    if (Object.keys(user_cards).length === 0) {
        emptyBankTitle.textContent = 'לא נמצאו תנועות בנק';
        return;
    }

    const tableBody = document.querySelector('#bank-transactions-table tbody');
    const itemsPerPage = 10;
    let currentPage = 1;

    const colName = Object.keys(bank_transactions)[0];
    const numberOfDuplicates = bank_transactions[colName].length;
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

            row.appendChild(createTableCell(bank_transactions.account_number[i], 'account-number-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_category[i], 'transaction-category-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_reference[i], 'transaction-reference-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_provider[i], 'transaction-provider-col'));
            row.appendChild(createTableCell(bank_transactions.current_balance[i], 'current-balance-col'));
            row.appendChild(createTableCell(bank_transactions.outcome_balance[i], 'outcome-balance-col'));
            row.appendChild(createTableCell(bank_transactions.income_balance[i], 'income-balance-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_description[i], 'transaction-description-col'));
            row.appendChild(createTableCell(bank_transactions.transaction_date[i], 'transaction-date-col'));

            tableBody.appendChild(row);
        }
    }

    function renderPagination() {
        const pagination = document.getElementById("bank-transactions-pagination");
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


    // Object to track sort state for each column
    const sortState = {
        account_number: 'asc',
        transaction_category: 'asc',
        transaction_reference: 'asc',
        transaction_provider: 'asc',
        current_balance: 'asc',
        outcome_balance: 'asc',
        income_balance: 'asc',
        transaction_description: 'asc',
        transaction_date: 'asc'
    };

    const name_conversion = {
        'מספר חשבון': 'account_number',
        'קטגוריה': 'transaction_category',
        'אסמכתא': 'transaction_reference',
        'שם הבנק': 'transaction_provider',
        'יתרה נוכחית': 'current_balance',
        'סכום חיוב': 'outcome_balance',
        'סכום זיכוי': 'income_balance',
        'תיאור תנועה': 'transaction_description',
        'תאריך תנועה': 'transaction_date'
    }

    // Function to sort transactions based on a column
    function sortByColumn(column) {
        const isAscending = sortState[column] === 'asc';
        const multiplier = isAscending ? 1 : -1;

        // Sort the data array based on the selected column
        bank_transactions[column].sort((valueA, valueB) => {
            // Check if both values are numbers
            if (!isNaN(valueA) && !isNaN(valueB)) {
                return (valueA - valueB) * multiplier; // Numeric comparison
            } else {
                // Use localeCompare for string comparison
                return valueA.localeCompare(valueB) * multiplier;
            }
        });

        // Reverse the sort order for the column
        sortState[column] = isAscending ? 'desc' : 'asc';
    }

    // Function to handle click events on column headers
    function handleColumnHeaderClick(event) {
        const columnHeader = event.target;
        const column = name_conversion[columnHeader.textContent];
        sortByColumn(column);
        renderTable(currentPage);
    }

    // Add click event listeners to column headers
    const columnHeaderElements = document.querySelectorAll('#bank-transactions-table th');
    columnHeaderElements.forEach(columnHeader => {
        columnHeader.addEventListener('click', handleColumnHeaderClick);
    });
});

/* ----------------------- File Upload Table ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector("#upload-file-form");
    const fileInput = document.querySelector(".upload-file-input");
    const progressArea = document.querySelector(".upload-file-progress-area");
    const uploadedArea = document.querySelector(".uploaded-file-area");

    form.addEventListener("click", function () {
        fileInput.click();
    });

    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            let fileName = file.name;
            if (fileName.length >= 50) {
                const splitName = fileName.split('.');
                fileName = splitName[0].substring(0, 50) + "... ." + splitName[1];
            }
            uploadFile(fileName);
        }
    });

    function uploadFile(name) {
        let fileSize;
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/settings/upload', true);
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.upload.addEventListener("progress", function (event) {

            const loaded = event.loaded;
            const total = event.total;
            const fileLoaded = Math.floor((loaded / total) * 100);
            const fileTotal = Math.floor(total / 1000);

            (fileTotal < 1024) ? fileSize = fileTotal + ' ק"ב ' : fileSize = (loaded / (1024 * 1024)).toFixed(2) + ' מ"ב ';
            const progressHTML = `<li class="upload-file-row">
                          <i class="fas fa-file-alt"></i>
                          <div class="upload-file-content">
                            <div class="upload-file-details">
                              <span class="upload-file-name">${name} • מעלה</span>
                              <span class="upload-file-percent">${fileLoaded}%</span>
                            </div>
                            <div class="upload-file-progress-bar">
                              <div class="upload-file-progress" style="width: ${fileLoaded}%"></div>
                            </div>
                          </div>
                        </li>`;

            uploadedArea.classList.add("onprogress");
            progressArea.innerHTML = progressHTML;

            if (loaded === total) {
                progressArea.innerHTML = "";
                const uploadedHTML = `<li class="upload-file-row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="upload-file-details">
                                <span class="upload-file-name">${name} • טוען נתונים למערכת...</span>
                                <span class="upload-file-size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;

                uploadedArea.classList.remove("onprogress");
                uploadedArea.classList.add("completed-client-side");
                uploadedArea.innerHTML = uploadedHTML;
            }
        });
        xhr.onload = function () {
            if (xhr.status === 200) {
                let responseData = JSON.parse(xhr.responseText);
                progressArea.innerHTML = "";
                const uploadedServer = `<li class="upload-file-row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="upload-file-details">
                                <span class="upload-file-name">${name} • ${responseData.statusText}</span>
                                <span class="upload-file-size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;

                uploadedArea.classList.remove("completed-client-side");
                uploadedArea.classList.add("completed-server-side");
                uploadedArea.innerHTML = uploadedServer;
                showSuccessStatus("רשומות שנמצאו: " + responseData.Statistics[0] + " רשומות חדשות שנוספו: " + responseData.Statistics[1] + " רשומות שנכשלו: " + responseData.Statistics[2] + " רשומות קיימות: " + responseData.Statistics[3], ".upload-file-statistics");
            } else {
                let responseData = JSON.parse(xhr.responseText);
                progressArea.innerHTML = "";
                const uploadedServer = `<li class="upload-file-row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="upload-file-details">
                                <span class="upload-file-name">${name} • ${responseData.statusText}</span>
                                <span class="upload-file-size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;

                uploadedArea.classList.remove("completed-client-side");
                uploadedArea.classList.add("completed-server-side");
                uploadedArea.innerHTML = uploadedServer;
            }
        };
        const data = new FormData(form);
        xhr.send(data);
    }

});

/* ----------------------- Misc Functions ----------------------- */

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
function showSuccessStatus(message, element) {
    const successStatusElement = document.querySelector(element);
    successStatusElement.textContent = message;
    successStatusElement.style.display = 'block';
    setTimeout(() => {
        successStatusElement.style.display = 'none';
    }, 4000);
}

// Function to show fail status message
function showFailStatus(message, element) {
    const failStatusElement = document.querySelector(element);
    failStatusElement.textContent = message;
    failStatusElement.style.display = 'block';
    setTimeout(() => {
        failStatusElement.style.display = 'none';
    }, 2000);
}
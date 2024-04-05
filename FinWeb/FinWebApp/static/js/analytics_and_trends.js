// Spent Merchant per specific period
const ColorPalette = [
    'rgba(222, 48, 48, 0.5)',      // Red
    'rgba(224, 122, 52, 0.5)',      // Green
    'rgba(226, 195, 55, 0.5)',      // Blue
    'rgba(157, 189, 61, 0.5)',    // Yellow
    'rgba(64, 214, 207, 0.5)',    // Magenta
    'rgba(61, 157, 189, 0.5)',    // Cyan
    'rgba(171, 86, 126, 0.5)',    // Orange
    'rgba(219, 43, 125, 0.5)'     // Purple
];

document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.canvas-button').forEach(function (button) {
        button.addEventListener('click', function () {

            let dateNavCanvasClasses = ['spent_by_date_month', 'spent_by_date_quarter', 'spent_by_date_year']

            // Iterate over each class name
            dateNavCanvasClasses.forEach(function (navCanvasClass) {
                // Select the div element with the current class name
                let canvasElement = document.querySelector('#' + navCanvasClass);

                // Hide the div if it exists
                if (button.getAttribute('data-canvas') === navCanvasClass) {
                    canvasElement.style.display = 'block';
                    canvasElement.style.width = '500px';
                    canvasElement.style.height = '250px';
                } else {
                    if (button.getAttribute('data-canvas').includes('spent_by_date'))
                        canvasElement.style.display = 'none';
                }
            });


            let categoryNavCanvasClasses = ['spent_by_category_month', 'spent_by_category_quarter', 'spent_by_category_year']

            // Iterate over each class name
            categoryNavCanvasClasses.forEach(function (navCanvasClass) {
                // Select the div element with the current class name
                let canvasElement = document.querySelector('#' + navCanvasClass);

                // Hide the div if it exists
                if (button.getAttribute('data-canvas') === navCanvasClass) {
                    canvasElement.style.display = 'block';
                    canvasElement.style.width = '1000px';
                    canvasElement.style.height = '350px';
                } else {
                    if (button.getAttribute('data-canvas').includes('spent_by_category'))
                        canvasElement.style.display = 'none';
                }

            });


        });
    });
});

/* ----------------------- Credit Cards Analytics & Trends Section ----------------------- */
document.addEventListener('DOMContentLoaded', function () {
// Select the container div
    let container = document.querySelector('.credit-card-selection');

// Define the number of credit card selection boxes to add
    let numberOfBoxes = Object.keys(user_cards).length; // You can set this dynamically

// Loop to create and append the required number of credit card selection boxes
    for (let i = 0; i < numberOfBoxes; i++) {
        // Create a new div element for the credit card selection box
        let newBox = document.createElement('div');
        newBox.classList.add('credit-card-selection-box');

        // Create a paragraph element for the text
        let paragraph = document.createElement('p');
        paragraph.textContent = user_cards.issuer_name[i] + ' - ' + user_cards.last_4_digits[i]; // Set your dynamic content here

        // Append the paragraph element to the new box
        newBox.appendChild(paragraph);

        // Append the new box to the container
        container.appendChild(newBox);
    }
});


document.addEventListener('DOMContentLoaded', function () {

    // Spent By Month Chart
    const spent_by_date_monthly_data = {
        labels: Object.keys(spent_by_date_monthly),
        datasets: [{
            label: "הוצאות לפי חודש",
            data: Object.values(spent_by_date_monthly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

    const spent_by_date_month_ctx = document.getElementById('spent_by_date_month').getContext('2d');
    new Chart(spent_by_date_month_ctx, {
        type: 'bar',
        data: spent_by_date_monthly_data,
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

    // Spent By Quarter Chart
    const spent_by_date_quarter_ctx_data = {
        labels: Object.keys(spent_by_date_quarterly),
        datasets: [{
            label: "הוצאות לפי רבעון",
            data: Object.values(spent_by_date_quarterly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

    const spent_by_date_quarter_ctx = document.getElementById('spent_by_date_quarter').getContext('2d');
    new Chart(spent_by_date_quarter_ctx, {
        type: 'bar',
        data: spent_by_date_quarter_ctx_data,
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

    // Spent By Year Chart
    const spent_by_date_year_ctx_data = {
        labels: Object.keys(spent_by_date_yearly),
        datasets: [{
            label: "הוצאות לפי שנה",
            data: Object.values(spent_by_date_yearly),
            backgroundColor: 'rgba(222, 74, 74, 0.4)',
            borderColor: 'rgba(222, 74, 74, 1)',
            borderWidth: 1
        }]
    };

    const spent_by_date_year_ctx = document.getElementById('spent_by_date_year').getContext('2d');
    new Chart(spent_by_date_year_ctx, {
        type: 'bar',
        data: spent_by_date_year_ctx_data,
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


    // Function to create datasets for merchants from data
    function createDatasetsForCategories(data) {
        const categoryData = {};
        for (const currentDateData of Object.values(data)) {
            for (const [category, amount] of currentDateData) {
                if (categoryData.hasOwnProperty(category)) {
                    categoryData[category].push(amount);
                } else {
                    categoryData[category] = [amount];
                }
            }
        }
        return categoryData;
    }

    // Function to configure and create a bar chart
    function createBarChart(raw_data, ctx, data, colorPalette) {
        const chartData = {
            labels: Object.keys(raw_data),
            datasets: []
        };

        let idx = 0;
        for (const [name, values] of Object.entries(data)) {
            chartData.datasets.push({
                label: name,
                backgroundColor: colorPalette[idx],
                data: values
            });
            idx++;
        }

        const options = {
            scales: {
                x: {stacked: true},
                y: {stacked: true}
            },
            responsive: false
        };

        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: options
        });
    }

    const spent_by_category_month_ctx = document.getElementById('spent_by_category_month').getContext('2d');
    const spent_by_category_monthly_data = createDatasetsForCategories(spent_by_category_monthly);
    createBarChart(spent_by_category_monthly, spent_by_category_month_ctx, spent_by_category_monthly_data, ColorPalette);

    const spent_by_category_quarter_ctx = document.getElementById('spent_by_category_quarter').getContext('2d');
    const spent_by_category_quarter_data = createDatasetsForCategories(spent_by_category_quarterly);
    createBarChart(spent_by_category_quarterly, spent_by_category_quarter_ctx, spent_by_category_quarter_data, ColorPalette);

    const spent_by_category_year_ctx = document.getElementById('spent_by_category_year').getContext('2d');
    const spent_by_category_year_data = createDatasetsForCategories(spent_by_category_yearly);
    createBarChart(spent_by_category_yearly, spent_by_category_year_ctx, spent_by_category_year_data, ColorPalette);

    const words = [];
    for (const word of Object.values(spent_by_business)) {
        words.push([word.label, word.x])
    }

    const options = {
        list: words, // List of words with sizes
        fontFamily: "Gan", // Font family
        weightFactor: 18, // Set the weightFactor to 18 for consistent font size
        color: function (word, weight) { // Function to define color based on word index
            // Assign different colors based on the index
            return ColorPalette[weight % ColorPalette.length]; // Use modulo to loop through colors
        },
        // Other options: https://wordcloud2-js.timdream.org/
    };

    new WordCloud(document.getElementById('wordcloud-canvas'), options);


});
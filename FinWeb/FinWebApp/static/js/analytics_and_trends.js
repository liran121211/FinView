// Palette of colors in Analytics and Trends
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

// hold global usage of created chart instances.
let chartInstances = {
    'SpentByDateMonthly': null,
    'SpentByDateQuarterly': null,
    'SpentByDateYearly': null,
    'SpentByCategoryMonthly': null,
    'SpentByCategoryQuarterly': null,
    'SpentByCategoryYearly': null,
    'wordCloud': null,
}

// define the behaviour of graphs when clicking on the buttons above the graph.
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
        newBox.setAttribute('card-idx', i);
        newBox.style.height = (200 - (15 * numberOfBoxes)).toString() + 'px';

        // Create a paragraph element for the text
        let paragraph = document.createElement('p');
        paragraph.style.fontSize = (18 - (1.01 * numberOfBoxes)).toString() + 'px';
        paragraph.textContent = user_cards.issuer_name[i] + ' - ' + user_cards.last_4_digits[i]; // Set your dynamic content here

        // Append the paragraph element to the new box
        newBox.appendChild(paragraph);

        // Append the new box to the container
        container.appendChild(newBox);
    }

    // Select all divs with the class 'credit-card-selection-box'
    const divs = document.querySelectorAll('.credit-card-selection-box');

    // Add click event listener to each div
    divs.forEach(div => {
        div.addEventListener('click', () => {
            // Check if the div already has 'clicked' class
            const alreadyClicked = div.classList.contains('clicked');

            // Remove 'clicked' class from all divs
            divs.forEach(divElement => {
                divElement.classList.remove('clicked');
            });

            // If the div was already clicked, do nothing
            if (!alreadyClicked) {
                // Add 'clicked' class to the clicked div
                div.classList.add('clicked');

                // destroy latest graph before attaching a new one
                chartInstances['SpentByDateMonthly'].destroy();
                chartInstances['SpentByDateQuarterly'].destroy();
                chartInstances['SpentByDateYearly'].destroy();

                chartInstances['SpentByCategoryMonthly'].destroy();
                chartInstances['SpentByCategoryQuarterly'].destroy();
                chartInstances['SpentByCategoryYearly'].destroy();

                // add Spent By Month for specific card, Graph.
                const cardIdx = div.getAttribute('card-idx');
                spentByDateGraph('Monthly', spent_by_date_monthly_specific_card[cardIdx]);
                spentByDateGraph('Quarterly', spent_by_date_quarterly_specific_card[cardIdx]);
                spentByDateGraph('Yearly', spent_by_date_yearly_specific_card[cardIdx]);

                // add Spent By Category for specific card, Graph.
                spentByCategoryGraph('Monthly', spent_by_category_monthly_specific_card[cardIdx]);
                spentByCategoryGraph('Quarterly', spent_by_category_quarterly_specific_card[cardIdx]);
                spentByCategoryGraph('Yearly', spent_by_category_yearly_specific_card[cardIdx]);
            }
        });
    });

});


document.addEventListener('DOMContentLoaded', function () {
    spentByDateGraph('Monthly', spent_by_date_monthly);
    spentByDateGraph('Quarterly', spent_by_date_quarterly);
    spentByDateGraph('Yearly', spent_by_date_yearly);

    spentByCategoryGraph('Monthly', spent_by_category_monthly);
    spentByCategoryGraph('Quarterly', spent_by_category_quarterly);
    spentByCategoryGraph('Yearly', spent_by_category_yearly);


    // wordcloud of businesses names of transactions
    const wordcloud_words = [];
    for (const word of Object.values(spent_by_business)) {
        wordcloud_words.push([word.label, word.x])
    }

    const wordcloud_options = {
        list: wordcloud_words, // List of words with sizes
        fontFamily: "Gan", // Font family
        weightFactor: 18, // Set the weightFactor to 18 for consistent font size
        color: function (word, weight) { // Function to define color based on word index
            // Assign different colors based on the index
            return ColorPalette[weight % ColorPalette.length]; // Use modulo to loop through colors
        },
    };

    const wordcloud_ctx = document.getElementById('wordcloud-canvas');
    chartInstances['wordCloud'] = new WordCloud(wordcloud_ctx, wordcloud_options);


});


function spentByDateGraph(period, data) {
    if (period === 'Monthly') {
        // Spent By Month Chart
        const spent_by_date_monthly_data = {
            labels: Object.keys(data),
            datasets: [{
                label: "הוצאות לפי חודש",
                data: Object.values(data),
                backgroundColor: 'rgba(222, 74, 74, 0.4)',
                borderColor: 'rgba(222, 74, 74, 1)',
                borderWidth: 1
            }]
        };

        const spent_by_date_month_ctx = document.getElementById('spent_by_date_month').getContext('2d');
        chartInstances['SpentByDateMonthly'] = new Chart(spent_by_date_month_ctx, {
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
    }

    if (period === 'Quarterly') {
        // Spent By Quarter Chart
        const spent_by_date_quarter_ctx_data = {
            labels: Object.keys(data),
            datasets: [{
                label: "הוצאות לפי רבעון",
                data: Object.values(data),
                backgroundColor: 'rgba(222, 74, 74, 0.4)',
                borderColor: 'rgba(222, 74, 74, 1)',
                borderWidth: 1
            }]
        };

        const spent_by_date_quarter_ctx = document.getElementById('spent_by_date_quarter').getContext('2d');
        chartInstances['SpentByDateQuarterly'] = new Chart(spent_by_date_quarter_ctx, {
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
    }

    if (period === 'Yearly') {
        // Spent By Year Chart
        const spent_by_date_year_ctx_data = {
            labels: Object.keys(data),
            datasets: [{
                label: "הוצאות לפי שנה",
                data: Object.values(data),
                backgroundColor: 'rgba(222, 74, 74, 0.4)',
                borderColor: 'rgba(222, 74, 74, 1)',
                borderWidth: 1
            }]
        };

        const spent_by_date_year_ctx = document.getElementById('spent_by_date_year').getContext('2d');
        chartInstances['SpentByDateYearly'] = new Chart(spent_by_date_year_ctx, {
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
    }
}

function spentByCategoryGraph(period, data) {
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
    function createBarChart(barChartRaw, barChart_ctx, barChart_data, colorPalette) {
        const chartData = {
            labels: Object.keys(barChartRaw),
            datasets: []
        };

        let idx = 0;
        for (const [name, values] of Object.entries(barChart_data)) {
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


        if (period === 'Monthly') {
            chartInstances['SpentByCategoryMonthly'] = new Chart(barChart_ctx, {
                type: 'bar',
                data: chartData,
                options: options
            });
        }

        if (period === 'Quarterly') {
            chartInstances['SpentByCategoryQuarterly'] = new Chart(barChart_ctx, {
                type: 'bar',
                data: chartData,
                options: options
            });
        }

        if (period === 'Yearly') {
            chartInstances['SpentByCategoryYearly'] = new Chart(barChart_ctx, {
                type: 'bar',
                data: chartData,
                options: options
            });
        }
    }

    if (period === 'Monthly') {
        // spent by category graph, monthly.
        const spent_by_category_month_ctx = document.getElementById('spent_by_category_month').getContext('2d');
        const spent_by_category_monthly_data = createDatasetsForCategories(data);
        createBarChart(data, spent_by_category_month_ctx, spent_by_category_monthly_data, ColorPalette);
    }
    if (period === 'Quarterly') {
        // spent by category graph, quarterly.
        const spent_by_category_quarter_ctx = document.getElementById('spent_by_category_quarter').getContext('2d');
        const spent_by_category_quarter_data = createDatasetsForCategories(data);
        createBarChart(data, spent_by_category_quarter_ctx, spent_by_category_quarter_data, ColorPalette);
    }
    if (period === 'Yearly') {
        // spent by category graph, yearly.
        const spent_by_category_year_ctx = document.getElementById('spent_by_category_year').getContext('2d');
        const spent_by_category_year_data = createDatasetsForCategories(data);
        createBarChart(data, spent_by_category_year_ctx, spent_by_category_year_data, ColorPalette);
    }
}
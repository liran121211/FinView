// script.js

var data = {
    datasets: [{
        data: pieChartData.data,
        backgroundColor: [
            '#3498db', // Dodger Blue
            '#e74c3c', // Alizarin Crimson
            '#2ecc71', // Emerald Green
            '#f39c12', // Orange
            '#9b59b6'  // Amethyst Purple
        ],
        label: 'My dataset' // for legend
    }],
    labels: pieChartData.labels
};

var pieOptions = {
    events: false,
    title: {
        display: true,
        text: pieChartData.title,
        fontSize: 16
    },
    animation: {
        duration: 500,
        easing: "easeOutQuart",
        onComplete: function () {
            var ctx = this.chart.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontFamily, 'normal', Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';

            this.data.datasets.forEach(function (dataset) {

                for (var i = 0; i < dataset.data.length; i++) {
                    var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model,
                        total = dataset._meta[Object.keys(dataset._meta)[0]].total,
                        mid_radius = model.innerRadius + (model.outerRadius - model.innerRadius) / 2,
                        start_angle = model.startAngle,
                        end_angle = model.endAngle,
                        mid_angle = start_angle + (end_angle - start_angle) / 2;

                    var x = mid_radius * Math.cos(mid_angle);
                    var y = mid_radius * Math.sin(mid_angle);

                    ctx.fillStyle = '#fff';
                    if (i == 3) { // Darker text color for lighter background
                        ctx.fillStyle = '#444';
                    }

                    var val = dataset.data[i];
                    var percent = String(Math.round(val / total * 100)) + "%";

                    if (val != 0) {
                        ctx.fillText(dataset.data[i], model.x + x, model.y + y);
                        // Display percent in another line, line break doesn't work for fillText
                        ctx.fillText(percent, model.x + x, model.y + y + 15);
                    }
                }
            });
        }
    }
};

var pieChartCanvas = document.getElementById('pie-chart').getContext('2d');
var pieChart = new Chart(pieChartCanvas, {
    type: 'pie', // or doughnut
    data: data,
    options: pieOptions
});


let paymentMethod;

if (paymentMethodChart){
    let method_labels = Object.keys(paymentMethodChart);
    let payment_method_values = Object.values(paymentMethodChart);
    var ctx1 = document.getElementById('paymentMethodPieChart').getContext('2d')
    paymentMethod = new Chart(ctx1, {
        type: 'pie',
        data: {
            datasets: [{
                data: payment_method_values,
                backgroundColor: ['#6AF9B8', '#F9B86A']
            }],
            labels: method_labels
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    }
    );   
}

if (revenuesPerDayChart){

    const keys = Object.keys(revenuesPerDayChart);
    const values = Object.values(revenuesPerDayChart);

    var ctx2 = document.getElementById('revenuesPerDayBarChart').getContext('2d')

    let chart = new Chart(ctx2, {
        type: 'bar',
        data: {
            datasets: [{
                label: "Ingresos",
                data: values,
                backgroundColor: ['#99b378']
            }],
            labels: keys
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    }
    );
}

if (productsChart){

    const keys = Object.keys(productsChart);
    const values = Object.values(productsChart);

    var ctx3 = document.getElementById('productPieChart').getContext('2d')

    let chart = new Chart(ctx3, {
        type: 'pie',
        data: {
            datasets: [{
                data: values,
                backgroundColor: ['#6AECF9', '#6AF993', '#DB6AF9', '#F9F56A', '#F9886A']
            }],
            labels: keys
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    }
    );
}
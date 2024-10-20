// Manage the logic when check-icon is clicked

$(document).ready(function() {

    let orderId = null;
    
    $('.check-icon').on('click', function() {
        orderId = $(this).data('id'); 

        $('#confirmModal').modal('show');

        $('#confirmDeliverBtn').on('click', function() {

            if (orderId) {
                // Send AJAX request if the user confirms
                $.ajax({
                    url: `/order-deliver/${orderId}`,  
                    method: 'POST',
                
                success: function(response) {
                    $('#confirmModal').modal('hide');
                    location.reload(true);  
                },
                error: function(error) {
                    alert('There was an error marking the product as delivered.');
                }
                });

            }
        });
    });
});

// Manage the logic when cancel-icon is clicked


$(document).ready(function() {

    let orderId = null;
    
    $('.cancel-icon').on('click', function() {
        orderId = $(this).data('id'); 

        $('#cancelModal').modal('show');

        $('#confirmCancelBtn').on('click', function() {

            if (orderId) {
                // Send AJAX request if the user confirms
                $.ajax({
                    url: `/order-cancel/${orderId}`,  
                    method: 'POST',
                
                success: function(response) {
                    $('#cancelModal').modal('hide');
                    location.reload(true);  
                },
                error: function(error) {
                    alert('There was an error marking the product as delivered.');
                }
                });

            }
        });
    });
});
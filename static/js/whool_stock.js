// Handle the added new whool within the popup modal

$(document).ready(function() {
    $('#addWhoolBtn').click(function() {
        $('#addWhoolModal').modal('show');
    });

    $('#addBtn').click(function() {
        var whoolColor = $('#whoolColor').val();
        var whoolQuantity = $('#whoolQuantity').val();
        $('#addWhoolForm').submit();
    });
});


// Handle the updated stock within the popup modal

$(document).ready(function() {

    $('.update-icon').on('click', function() {
        
        const whoolId = $(this).data('id');
        const whoolColor = $(this).data('color');
        const whoolQuantity = $(this).data('quantity');
        
        // Set the modal input values with the stock's current data
        $('#stockId').val(whoolId);
        $('#updateWhoolColor').val(whoolColor);
        $('#updateWhoolQuantity').val(whoolQuantity);

        $('#updateStockModal').modal('show');
    });
});

// Handle the delete button interaction on product

$(document).ready(function() {
    
    $('.delete-icon').on('click', function() {

        const stockId = $(this).data('id');
        window.location.href = `/whool-stock-delete/${stockId}`;
    });
});
// Handle the visibility of the delete and update icons

function toggleIcons(item) {
    // Get the icons inside the same parent container as the clicked <li>
    const icons = item.parentElement.querySelectorAll('.update-icon, .delete-icon');
    icons.forEach(icon => {
        if (icon.style.display === "none" || icon.style.display === "") {
            icon.style.display = "inline-block"; // Show the icons
        } else {
            icon.style.display = "none"; // Hide the icons
        }
    });
}

//Handle the added new product within the popup modal

$(document).ready(function() {
    $('#addProductBtn').click(function() {
        $('#addProductModal').modal('show');
    });

    $('#addBtn').click(function() {
        var productName = $('#productName').val();
        $('#addProductForm').submit();
    });
});

//Handle the updated product within the popup modal

$(document).ready(function() {
    // Event listener for update-icon clicks
    $('.update-icon').on('click', function() {
        // Get the product ID and name from the data attributes
        const productId = $(this).data('id');
        const productName = $(this).data('name');
        
        // Set the modal input values with the product's current data
        $('#updateProductId').val(productId);
        $('#updateProductName').val(productName);

        // Show the update modal
        $('#updateProductModal').modal('show');
    });
});

//Handle the delete button interaction

$(document).ready(function() {
    
    $('.delete-icon').on('click', function() {
        // Get the product ID from the data-id attribute
        const productId = $(this).data('id');

        window.location.href = `/product-delete/${productId}`;
    });
});
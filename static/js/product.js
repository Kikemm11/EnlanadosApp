// Handle the visibility of the delete and update icons

function toggleIcons(item) {
    // Get the icons inside the same parent container as the clicked <li>
    const icons = item.parentElement.querySelectorAll('.update-icon, .delete-icon, .options-icon');
    icons.forEach(icon => {
        if (icon.style.display === "none" || icon.style.display === "") {
            icon.style.display = "inline-block"; // Show the icons
        } else {
            icon.style.display = "none"; // Hide the icons
        }
    });
}

// Handle the added new product within the popup modal

$(document).ready(function() {
    $('#addProductBtn').click(function() {
        $('#addProductModal').modal('show');
    });

    $('#addBtn').click(function() {
        var productName = $('#productName').val();
        $('#addProductForm').submit();
    });
});

// Handle the added new product type within the popup modal

$(document).ready(function() {
    $('#addProductTypeBtn').click(function() {
        $('#addProductTypeModal').modal('show');
    });

    $('#addBtn').click(function() {
        var productTypeName = $('#productTypeName').val();
        var productTypeParent = $('#productTypeParent').val();
        var productTypePrice = $('#productTypePrice').val();
        $('#addProductTypeForm').submit();
    });
});

// Handle the updated product within the popup modal

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

// Handle the delete button interaction on product

$(document).ready(function() {
    
    $('.delete-icon').on('click', function() {
        // Get the product ID from the data-id attribute
        const productId = $(this).data('id');

        window.location.href = `/product-delete/${productId}`;
    });
});


$(document).ready(function() {
    $('.options-icon').on('click', function() {
        // Get the product ID from the data attribute
        const productId = $(this).data('id');

        // Make an AJAX request to fetch product details
        $.ajax({
            url: `/product-type/${productId}`, // Adjust the URL as needed
            method: 'GET',
            success: function(data) {
                
                $('#optionsTable tbody').empty(); // Clear existing rows

                data.forEach(function(product) {
                    
                    const row = `<tr>
                                    <td>${product.name}</td>
                                    <td>${product.price}</td>
                                    <td>
                                        <img src="static/assets/img/update.png" alt="Update Table" class="update-icon-table" data-id="${product.id}" data-name="${product.name}" data-parent="${product.parent}" data-price="${product.price}">
                                        <img src="static/assets/img/delete.png" alt="Delete Table" class="delete-icon-table" data-id="${product.id}">
                                    </td> 
                                </tr>`;
                    $('#optionsTable tbody').append(row);
                });

                // Show the options table
                $('#optionsTable').toggle();
            },
            error: function() {
                alert('Error al obtener tipos de productos!'); 
            }
        });

    });

    // Optional: Close the table when clicking outside of it
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.options-icon').length && !$(event.target).closest('#optionsTable').length) {
            $('#optionsTable').hide();
        }
    });


    // Handle the delete button interaction on product type

    $('#optionsTable').on('click', '.delete-icon-table', function() {
        const productTypeId = $(this).data('id');

        window.location.href = `/product-type-delete/${productTypeId}`;   
    });


    $('#optionsTable').on('click', '.update-icon-table', function() {    
        
        const productTypeId = $(this).data('id');
        const productTypeName = $(this).data('name');
        const productTypeParent = $(this).data('parent');
        const productTypePrice = $(this).data('price');

        console.log(productTypeParent)
        
        // Set the modal input values with the product's current data
        $('#updateProductTypeId').val(productTypeId);
        $('#updateProductTypeName').val(productTypeName);
        $('#updateProductTypeParent').val(productTypeParent);
        $('#updateProductTypePrice').val(productTypePrice);

        // Show the update modal
        $('#updateProductTypeModal').modal('show');
    });

});
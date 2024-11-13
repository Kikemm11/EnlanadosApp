// Manage the search bar inside the select inputs

$(document).ready(function() {
    $('.city-select').select2({
      placeholder: "Selecciona un destino",
      allowClear: true
    });
  });

$(document).ready(function() {
  $('.product-select').select2({
    placeholder: "Selecciona un producto",
    allowClear: true
  });
});

$(document).ready(function() {
    $('.product-type-select').select2({
      placeholder: "Selecciona un tipo de producto",
      allowClear: true
    });
  });

$(document).ready(function() {
  $('.payment-method-select').select2({
    placeholder: "Selecciona un método de pago",
    allowClear: true
  });
});

$(document).ready(function() {
    $('.status-select').select2({
      placeholder: "Selecciona un estatus",
      allowClear: true
    });
  });

document.querySelector('.dropdown-btn').addEventListener('click', function(event) {
  // Prevent form submission or any other action if needed
  event.stopPropagation();
  event.preventDefault();
  
  // Toggle the 'show' class for the dropdown content
  document.querySelector('.dropdown-content').classList.toggle('show');
});

// Close dropdown if clicked outside
window.onclick = function(event) {
  if (!event.target.matches('.dropdown-btn') && !event.target.matches('.dropdown-content input')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
              openDropdown.classList.remove('show');
          }
      }
  }
}
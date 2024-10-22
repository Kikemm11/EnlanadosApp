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
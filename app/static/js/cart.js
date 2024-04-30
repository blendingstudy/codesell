document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="selected_items"]');
    const totalPriceElement = document.getElementById('total-price');
  
    function updateTotalPrice() {
      let totalPrice = 0;
      checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
          totalPrice += parseFloat(checkbox.dataset.price);
        }
      });
      totalPriceElement.textContent = totalPrice.toFixed(2);
    }
  
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', updateTotalPrice);
    });
  
    updateTotalPrice();
  });
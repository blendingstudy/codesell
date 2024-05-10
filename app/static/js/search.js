document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const searchResults = document.querySelector('.search-results');
  
    searchForm.addEventListener('submit', function(e) {
      e.preventDefault();
  
      const keyword = searchForm.querySelector('input[name="keyword"]').value;
      const minPrice = searchForm.querySelector('input[name="min_price"]').value;
      const maxPrice = searchForm.querySelector('input[name="max_price"]').value;
      const language = searchForm.querySelector('select[name="language"]').value;
      const usage = searchForm.querySelector('select[name="usage"]').value;
  
      const url = `/products/search?keyword=${encodeURIComponent(keyword)}&min_price=${encodeURIComponent(minPrice)}&max_price=${encodeURIComponent(maxPrice)}&language=${encodeURIComponent(language)}&usage=${encodeURIComponent(usage)}`;
  
      fetch(url)
        .then(response => response.text())
        .then(data => {
          searchResults.innerHTML = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
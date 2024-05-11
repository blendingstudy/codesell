document.addEventListener('DOMContentLoaded', () => {
    // 리뷰 삭제 버튼 클릭 이벤트 처리
    const deleteReviewButtons = document.querySelectorAll('.delete-review');
    deleteReviewButtons.forEach(button => {
      button.addEventListener('click', (event) => {
        const confirmDelete = confirm('Are you sure you want to delete this review?');
        if (!confirmDelete) {
          event.preventDefault();
        }
      });
    });
  
    // 리뷰 작성 폼 제출 이벤트 처리
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      reviewForm.addEventListener('submit', (event) => {
        event.preventDefault();
  
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;
  
        if (rating === '') {
          alert('Please select a rating.');
          return;
        }
  
        // AJAX 요청을 사용하여 리뷰 작성 처리
        fetch(reviewForm.action, {
          method: 'POST',
          body: new FormData(reviewForm)
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              alert('Review submitted successfully.');
              window.location.reload();
            } else {
              alert('Failed to submit the review. Please try again.');
            }
          })
          .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting the review.');
          });
      });
    }
  
    // 리뷰 수정 폼 제출 이벤트 처리
    const editReviewForm = document.getElementById('edit-review-form');
    if (editReviewForm) {
      editReviewForm.addEventListener('submit', (event) => {
        event.preventDefault();
  
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;
  
        if (rating === '') {
          alert('Please select a rating.');
          return;
        }
  
        // AJAX 요청을 사용하여 리뷰 수정 처리
        fetch(editReviewForm.action, {
          method: 'POST',
          body: new FormData(editReviewForm)
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              alert('Review updated successfully.');
              window.location.href = data.redirect;
            } else {
              alert('Failed to update the review. Please try again.');
            }
          })
          .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the review.');
          });
      });
    }
  });
document.addEventListener('DOMContentLoaded', function() {
  // 펀딩 참여 폼 제출 시 처리
  const participateForm = document.querySelector('.participate-form');
  if (participateForm) {
    participateForm.addEventListener('submit', function(event) {
      const amountInput = participateForm.querySelector('input[name="amount"]');
      const amount = parseInt(amountInput.value);

      if (isNaN(amount) || amount <= 0) {
        event.preventDefault();
        alert('유효한 참여 금액을 입력해주세요.');
        return;
      }

      // 서버로 펀딩 참여 요청 전송
      fetch(participateForm.action, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('펀딩에 참여해주셔서 감사합니다!');
            window.location.reload();
          } else {
            alert('펀딩 참여에 실패했습니다. 다시 시도해주세요.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('펀딩 참여 중 오류가 발생했습니다. 다시 시도해주세요.');
        });
    });
  }

  // 펀딩 삭제 버튼 클릭 시 확인 대화상자 표시
  const deleteForm = document.querySelector('.delete-form');
  if (deleteForm) {
    deleteForm.addEventListener('submit', function(event) {
      if (!confirm('정말로 이 펀딩을 삭제하시겠습니까?')) {
        event.preventDefault();
      }
    });
  }
});
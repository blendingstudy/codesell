document.addEventListener('DOMContentLoaded', function () {
    // 선물하기 폼 제출 이벤트 처리
    const giftForm = document.getElementById('gift-form');
    giftForm.addEventListener('submit', function (event) {
      event.preventDefault();
  
      const formData = new FormData(giftForm);
      const receiverEmail = formData.get('receiver_email');
      const message = formData.get('message');
  
      // 서버로 선물하기 요청 보내기
      fetch(giftForm.action, {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('선물이 성공적으로 전송되었습니다.');
          window.location.href = data.redirect_url;
        } else {
          alert('선물 전송에 실패했습니다. 다시 시도해주세요.');
        }
      })
      .catch(error => {
        console.error('선물하기 요청 실패:', error);
        alert('선물하기 요청에 실패했습니다. 다시 시도해주세요.');
      });
    });
  });
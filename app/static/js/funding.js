document.addEventListener('DOMContentLoaded', function() {
  const participateForm = document.getElementById('participate-form');
  const payButton = document.getElementById('pay-button');
  const amountInput = document.getElementById('amount');
  const fundingId = participateForm.dataset.fundingId;

  if (payButton) {
    payButton.addEventListener('click', function() {
      const amount = parseInt(amountInput.value);

      if (isNaN(amount) || amount <= 0) {
        alert('유효한 참여 금액을 입력해주세요.');
        return;
      }

      // 결제 정보 설정
      const paymentData = {
        pg: 'html5_inicis',
        pay_method: 'card',
        merchant_uid: 'merchant_' + new Date().getTime(),
        name: '펀딩 참여',
        amount: amount,
        buyer_email: '',
        buyer_name: '',
        buyer_tel: '',
        buyer_addr: '',
        buyer_postcode: '',
        funding_id: fundingId
      };

      // 결제 진행
      const IMP = window.IMP;
      IMP.init('imp38825147');
      IMP.request_pay(paymentData, function(rsp) {
        if (rsp.success) {
          // 결제 성공 시 서버로 펀딩 참여 요청 전송
          const data = {
            imp_uid: rsp.imp_uid,
            merchant_uid: rsp.merchant_uid,
            amount: amount
          };

          fetch(`/fundings/${fundingId}/participate`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
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
        } else {
          alert('결제에 실패하였습니다. 에러내용: ' + rsp.error_msg);
        }
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
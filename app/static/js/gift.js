document.addEventListener('DOMContentLoaded', function () {
  const giftForm = document.getElementById('gift-form');
  const giftSubmitBtn = document.getElementById('gift-submit-btn');

  giftSubmitBtn.addEventListener('click', function () {
    const receiverEmail = document.querySelector('input[name="receiver_email"]').value;
    const message = document.querySelector('textarea[name="message"]').value;

    // 아임포트 결제창 호출
    IMP.init('imp38825147'); // 아임포트 사용자 코드로 대체해야 합니다.
    IMP.request_pay({
      pg: 'html5_inicis', // PG사 선택
      pay_method: 'card', // 결제 수단
      merchant_uid: 'merchant_' + new Date().getTime(), // 주문번호
      name: '선물 결제', // 주문명
      amount: productPrice,
      buyer_email: userEmail,
      buyer_name: userName,
      buyer_tel: '', // 구매자 전화번호
      buyer_addr: '', // 구매자 주소
      buyer_postcode: '', // 구매자 우편번호
    }, function (rsp) {
      if (rsp.success) {
        // 결제 성공 시 선물하기 요청 보내기
        const formData = new FormData(giftForm);
        formData.append('receiver_email', receiverEmail);
        formData.append('message', message);

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
      } else {
        alert('결제에 실패하였습니다. 에러 내용: ' + rsp.error_msg);
      }
    });
  });
});
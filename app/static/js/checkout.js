console.log('checkout.js loaded');
$(document).ready(function() {
    $('#pay-button').click(function() {
      var IMP = window.IMP;
      IMP.init('imp38825147');
  
      IMP.request_pay({
        pg: 'html5_inicis',
        pay_method: 'card',
        merchant_uid: 'merchant_' + new Date().getTime(),
        name: '주문명:결제테스트',
        amount: totalPrice,
        buyer_email: userEmail,
        buyer_name: userName,
        buyer_tel: '010-1234-5678',
        buyer_addr: '서울특별시 강남구 삼성동',
        buyer_postcode: '123-456'
      }, function(rsp) {
        if (rsp.success) {
          // 결제 성공 시 로직
          alert('결제가 완료되었습니다.');
          
          // 서버로 결제 정보와 배송 정보 전송
          var shippingAddress = $('#shipping_address').val();
          var selected_items=[];
          $('.item-checkbox').each(function() {
            selected_items.push($(this).val());
          });
          $.ajax({
            url: '/orders/create',
            method: 'POST',
            data: {
              imp_uid: rsp.imp_uid,
              merchant_uid: rsp.merchant_uid,
              shipping_address: shippingAddress,
              selected_items: JSON.stringify(selected_items),
              total_amount: totalPrice
            },
            success: function(data) {
              // 주문 완료 처리
              window.location.href = '/orders/' + data.order_id;
            },
            error: function(xhr, status, error) {
              console.error(error);
              alert('주문 처리 중 오류가 발생했습니다.');
            }
          });
        } else {
          // 결제 실패 시 로직
          alert('결제에 실패하였습니다. 에러내용: ' + rsp.error_msg);
        }
      });
    });
  });

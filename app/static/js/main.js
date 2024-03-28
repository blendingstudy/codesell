// 문서 로딩 완료 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // 폼 제출 이벤트 처리
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            // 폼 데이터 처리 로직 작성
            // 예: 유효성 검사, 비동기 요청 등
        });
    }

    // 버튼 클릭 이벤트 처리
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            // 버튼 클릭 시 수행할 동작 작성
            // 예: 페이지 이동, 데이터 로딩 등
        });
    });

    // 비동기 요청 예시 (상품 목록 로딩)
    const productList = document.querySelector('.product-list');
    if (productList) {
        fetch('/products')
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                // 상품 목록 렌더링 로직 작성
                // 예: 상품 데이터를 기반으로 HTML 생성 및 삽입
            })
            .catch(function(error) {
                console.log('Error:', error);
            });
    }

    // 장바구니 수량 변경 이벤트 처리
    const cartItemQuantity = document.querySelectorAll('.cart-item-quantity');
    cartItemQuantity.forEach(function(input) {
        input.addEventListener('change', function(event) {
            const itemId = event.target.dataset.itemId;
            const quantity = event.target.value;
            // 장바구니 수량 변경 로직 작성
            // 예: 서버에 업데이트 요청 전송
        });
    });

    // 기타 JavaScript 코드 작성
    // ...
});
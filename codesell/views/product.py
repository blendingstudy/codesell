from flask import Blueprint, render_template
from codesell.controllers.product_controller import product_bp

product_view = Blueprint('product_view', __name__)

# '/products' URL로 접속 시, product_bp의 product_list 함수를 호출
product_view.add_url_rule('/products', view_func=product_bp.product_list)
# '/products/<int:product_id>' URL로 접속 시, product_bp의 product_detail 함수를 호출
product_view.add_url_rule('/products/<int:product_id>', view_func=product_bp.product_detail)
import os
import random
import shutil
import subprocess
import uuid
import zipfile
import docker
from flask import Blueprint, current_app, jsonify, render_template, request, redirect, send_file, url_for, flash
from flask_login import current_user, login_required
from app.models.order import Order
from app.models.product import Product
from app.models.category import Category
from app import db
from app.forms import ProductForm, SearchForm
from app.models.review import Review
from build_and_deploy import build_and_deploy_code

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()

    search_form.language.choices = [(0, 'All Languages')] + [(category.id, category.name) for category in language_categories]
    search_form.usage.choices = [(0, 'All Usages')] + [(category.id, category.name) for category in usage_categories]

    products = Product.query.filter_by(is_active=True)

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        min_price = search_form.min_price.data
        max_price = search_form.max_price.data
        language_id = search_form.language.data
        usage_id = search_form.usage.data

        if keyword:
            products = products.filter(Product.name.ilike(f'%{keyword}%'))
        if min_price:
            products = products.filter(Product.price >= min_price)
        if max_price:
            products = products.filter(Product.price <= max_price)
        if language_id:
            products = products.filter_by(language_id=language_id)
        if usage_id:
            products = products.filter_by(category_id=usage_id)

    products = products.all()

    return render_template('product_list.html', products=products, search_form=search_form)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    form.language.choices = [(category.id, category.name) for category in language_categories]
    form.usage.choices = [(category.id, category.name) for category in usage_categories]
    
    if form.validate_on_submit():
        language_id = request.form['language']
        usage_id = request.form['usage']
        code_file = request.files['code_file']

        if code_file:
            filename = code_file.filename
            _, extension = os.path.splitext(filename)

            if extension == '.zip':
                unique_directory = str(uuid.uuid4())
                zip_directory = os.path.join(current_app.root_path, '..', 'uploads', unique_directory)
                os.makedirs(zip_directory, exist_ok=True)
                zip_file_path = os.path.join(zip_directory, filename)
                code_file.save(zip_file_path)

                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_directory)

                code_file_path = os.path.join(zip_directory, 'app.py')  # 압축 해제된 app.py 파일 경로
            else:
                unique_filename = str(uuid.uuid4()) + '_' + filename
                code_file_path = os.path.join(current_app.root_path, '..', 'uploads', unique_filename)
                code_file.save(code_file_path)

            # 데모 링크 생성
            demo_link = generate_demo_link(code_file_path)
        
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            code_file=code_file_path,
            category_id=usage_id,
            language_id=language_id,
            seller_id=current_user.id,
            demo_link=demo_link
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product created successfully.', 'success')
        return redirect(url_for('product.index'))
    
    return render_template('product_create.html', form=form, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>')
def get_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    reviews = Review.query.filter_by(product_id=product_id).all()  # 상품의 리뷰 목록 조회
    average_rating = product.get_average_rating()  # 상품의 평균 평점 계산
    return render_template('product_detail.html', product=product, reviews=reviews, average_rating=average_rating, demo_link=product.demo_link)

@product_bp.route('/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if product.seller_id != current_user.id:
        flash('You are not authorized to update this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        code_file = request.files['code_file']
        
        if code_file:
            filename = code_file.filename
            _, extension = os.path.splitext(filename)

            if extension == '.zip':
                unique_directory = str(uuid.uuid4())
                zip_directory = os.path.join(current_app.root_path, '..', 'uploads', unique_directory)
                os.makedirs(zip_directory, exist_ok=True)
                zip_file_path = os.path.join(zip_directory, filename)
                code_file.save(zip_file_path)

                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_directory)

                code_file_path = os.path.join(zip_directory, 'app.py')  # 압축 해제된 app.py 파일 경로
            else:
                unique_filename = str(uuid.uuid4()) + '_' + filename
                code_file_path = os.path.join(current_app.root_path, '..', 'uploads', unique_filename)
                code_file.save(code_file_path)

            product.code_file = code_file_path

            # 데모 링크 생성
            demo_link = generate_demo_link(code_file_path)
            product.demo_link = demo_link  # 데모 링크 업데이트
        
        product.category_id = request.form['usage']
        
        db.session.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    return render_template('product_update.html', product=product, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if product.seller_id != current_user.id:
        flash('You are not authorized to delete this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    product.is_active = False
    db.session.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('product.index'))

@product_bp.route('/<int:product_id>/download')
@login_required
def download_code(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if not Order.has_purchased(current_user.id, product):
        flash('You have not purchased this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    try:
        code_file_path = os.path.join(current_app.root_path, '..', product.code_file)
        return send_file(code_file_path, as_attachment=True)
    except FileNotFoundError:
        flash('Code file not found.', 'error')
        return redirect(url_for('product.get_product', product_id=product.id))

@product_bp.route('/search')
def search():
    search_form = SearchForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()

    search_form.language.choices = [(0, 'All Languages')] + [(category.id, category.name) for category in language_categories]
    search_form.usage.choices = [(0, 'All Usages')] + [(category.id, category.name) for category in usage_categories]

    keyword = request.args.get('keyword')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    language_id = request.args.get('language')
    usage_id = request.args.get('usage')

    products = Product.query.filter_by(is_active=True)

    if keyword:
        products = products.filter(Product.name.ilike(f'%{keyword}%'))
        print(keyword)
    if min_price:
        products = products.filter(Product.price >= min_price)
        print(min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)
        print(max_price)
    if language_id != '0':
        products = products.filter_by(language_id=language_id)
        print(language_id)
    if usage_id != '0':
        products = products.filter_by(category_id=usage_id)
        print(usage_id)

    products = products.all()

    return render_template('search_results.html', products=products, search_form=search_form)
    
def generate_demo_link(code_file_path):
    # 고유한 디렉토리 이름 생성
    unique_directory = str(uuid.uuid4())

    # 코드 파일이 위치할 디렉토리 경로 생성
    code_directory = os.path.join(os.path.dirname(code_file_path), 'sandbox', unique_directory)

    # 코드 디렉토리 생성
    os.makedirs(code_directory, exist_ok=True)

    # 코드 파일을 샌드박스 디렉토리로 복사
    code_filename = os.path.basename(code_file_path)
    sandbox_code_path = os.path.join(code_directory, code_filename)
    shutil.copy2(code_file_path, sandbox_code_path)

    # 코드 빌드 및 배포
    image_id = build_and_deploy_code(code_file_path)
    
    try:
        # Docker 클라이언트 생성
        client = docker.from_env()

        # 호스트의 임의의 포트 선택
        host_port = random.randint(8000, 9000)

        # Docker 컨테이너 실행
        container = client.containers.run(
            image=image_id,
            name=f"code-sandbox-container-{unique_directory}",
            detach=True,
            ports={'8000/tcp': host_port},  # 호스트의 특정 포트에 매핑
            auto_remove=True
        )

        # 데모 링크 생성
        demo_link = f"http://localhost:{host_port}"
        return demo_link
    except docker.errors.APIError as e:
        print(f"Docker API Error: {str(e)}")
        return None
    except docker.errors.ImageNotFound as e:
        print(f"Docker Image Not Found: {str(e)}")
        return None
    finally:
        # Docker 클라이언트 종료
        client.close()
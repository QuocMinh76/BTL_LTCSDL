import json, os
from websale import app, db
from websale.models import Category, Product, User, Receipt, ReceiptDetail, UserRole
from flask_login import current_user
from sqlalchemy import func
import hashlib

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()

def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price.__ge__(from_price))

    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def count_product():
    return Product.query.filter(Product.active.__eq__(True)).count()

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    with app.app_context():
        db.session.add(user)
        db.session.commit()

# Khi luu xuong bam bang thuat toan gi thi khi kiem tra phai bam bang thuat toan do
def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(cart):
    if cart:
        with app.app_context():
            receipt = Receipt(user=current_user)
            db.session.add(receipt)

            for c in cart.values():
                d = ReceiptDetail(receipt=receipt,
                                  product_id=c['id'],
                                  quantity=c['quantity'],
                                  unit_price=c['price'])
                db.session.add(d)

            db.session.commit()

def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def category_stats():
    '''
    SELECT c.id, c.name, count(p.id)
    FROM category c left outer join product p on c.id = p.category_id
    GROUP BY c.id, c.name
    '''
    # Viet cau truy van cach 1
    # return (Category.query.join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
    #                     .add_column(func.count(Product.id)))\
    #                     .group_by(Category.id, Category.name).all()
    # Viet cau truy van cach 2
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Category.id.__eq__(Product.category_id), isouter=True)\
        .group_by(Category.id, Category.name).all()
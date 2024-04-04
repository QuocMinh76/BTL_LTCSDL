from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from websale import app, db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True  # Khong tao bang

    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name

# lazy: khi nao dung den cai products moi lam, con khong thi chi lam may cai thuoc tinh kia
# Neu de la false hay subquery thi khi truy van cate no se xuat luon cai product co quan he
# Khi lam relationship many-to-one thi nen de lazy la True
class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name

class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    #comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

# O cho foreign key, neu truyen khong trong dau nhay don (' ') thi dung ten lop cham (.) thuoc tinh
# Con neu dung dau nhay don (' ') thi dung cai ten bang (__tablename__) cham (.) thuoc tinh

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        c1 = Category(name="Mobile")
        c2 = Category(name="Tablet")

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        products = [{
            "id": 1,
            "name": "iPhone 7 Plus",
            "description": "Apple, 32GB, RAM: 3GB, iOS13",
            "price": 17000000,
            "image": "images/p1.png",
            "category_id": 1
        }, {
            "id": 2,
            "name": "iPad Pro 2020",
            "description": "Apple, 128GB, RAM: 6GB",
            "price": 37000000,
            "image": "images/p2.png",
            "category_id": 2
        }, {
            "id": 3,
            "name": "Galaxy Note 10 Plus",
            "description": "Samsung, 64GB, RAML: 6GB",
            "price": 24000000,
            "image": "images/p3.png",
            "category_id": 1
        }]

        for p in products:
            pro = Product(name=p['name'], price=p['price'], image=p['image'],
                          description=p['description'], category_id=p['category_id'])
            db.session.add(pro)

        db.session.commit()

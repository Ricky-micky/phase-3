from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


# Create a base class for the models
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # buyer, seller, admin

class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String, nullable=True)

    seller = relationship('User', backref='products')
    
class Review(Base):
    __tablename__ = 'review'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    review_date = Column(DateTime, nullable=False)

    product = relationship('Product', backref='reviews')
    user = relationship('User', backref='reviews')

class Order(Base):
    __tablename__ = 'order'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    order_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user = relationship('User', backref='orders')

class OrderDetail(Base):
    __tablename__ = 'order_detail'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship('Order', backref='order_details')
    product = relationship('Product', backref='order_details')



from sqlalchemy import Column, Integer, String, Float, Text, Date, TIMESTAMP, ForeignKey, CheckConstraint, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    
    # One Product can have many ProductTypes
    product_types = relationship("ProductType", backref="product", cascade="all, delete", passive_deletes=True)
    
    
class ProductType(Base):
    __tablename__ = 'product_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey('product.id', onupdate='CASCADE', ondelete='CASCADE'))
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    
    # Add Check constraint
    __table_args__ = (
        CheckConstraint('price > 0.0', name='product_type_price_check'),
    )
    
    # One ProductType belongs to many Orders
    orders = relationship("Order", backref="product_type", cascade="all, delete", passive_deletes=True)
    
    
class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, unique=True) 
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # One City belongs to many Orders
    orders = relationship("Order", backref="city", cascade="all, delete", passive_deletes=True)
    
    
class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # One PaymentMethod belongs to many Orders
    orders = relationship("Order", backref="payment_method", cascade="all, delete", passive_deletes=True) 
    
    
class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True) 
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # One Status belongs to many Orders
    orders = relationship("Order", backref="status", cascade="all, delete", passive_deletes=True)  
    

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    client = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    product_type_id = Column(Integer, ForeignKey('product_type.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    added_price = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    payment_method_id = Column(Integer, ForeignKey('payment_method.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    estimated_date = Column(Date, nullable=False)
    status_id = Column(Integer, ForeignKey('status.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Many-to-many relationship with WhoolStock via OrderWhool
    whool_stocks = relationship(
        'WhoolStock',
        secondary='order_whool',
        backref='orders'
    )
    

    # Add Check constraint
    __table_args__ = (
        CheckConstraint('added_price >= 0.0', name='order_added_price_check'),
        CheckConstraint('credit >= 0.0', name='order_credit_check'),
    )
    
    
class WhoolStock(Base):
    __tablename__ = 'whool_stock'

    id = Column(Integer, primary_key=True)
    color = Column(String, nullable=False, unique=True) 
    quantity = Column(Integer, nullable=False)
    last_update = Column(Date, nullable=False)  # Last update date
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Add Check constraint
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='whool_stock_quantity_check'),
    )

class OrderWhool(Base):
    __tablename__ = 'order_whool'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    whool_stock_id = Column(Integer, ForeignKey('whool_stock.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
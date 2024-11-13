from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from datetime import datetime
import os

from models.Models import Order, ProductType, Status

load_dotenv()
database = os.getenv("DATABASE")


class OrderController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_order(self):
        session = self.SessionLocal()
        result = session.query(Order).all()
        session.close()
        return result
    
    def read_one_order(self, order_id):
    
        session = self.SessionLocal()
        result = session.query(Order).filter(Order.id == order_id).options(
                              joinedload(Order.product_type).joinedload(ProductType.product), 
                              joinedload(Order.payment_method),
                              joinedload(Order.status),
                              joinedload(Order.city),
                              joinedload(Order.whool_stocks)
                              ).first()
        session.close()
        return result
        
    def read_current_month_order(self):
        session = self.SessionLocal()
        
        try:
            today = datetime.today()
            current_month = today.month
            current_year = today.year
    
            result = session.query(Order).filter(
                        extract('month', Order.estimated_date) == current_month,
                        extract('year', Order.estimated_date) == current_year,
                    ).options(joinedload(Order.product_type).joinedload(ProductType.product), 
                              joinedload(Order.payment_method),
                              joinedload(Order.status),
                              joinedload(Order.city),
                              ).all()
            
            return result
        
        finally:
            session.close()
            
    def read_filter_order(self, start_date, end_date, status):
        
        session = self.SessionLocal()
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        status = [1,2,3] if status == "" else [status]
        
        try:
                    
            result = session.query(Order).filter(
                        Order.estimated_date.between(start_date, end_date),
                        Order.status_id.in_(status)
                    ).options(joinedload(Order.product_type).joinedload(ProductType.product), 
                            joinedload(Order.payment_method),
                            joinedload(Order.status),
                            joinedload(Order.city),
                    ).all()
            
            return result
        
        finally:
            session.close()
            
    def statistics_data(self, start_date, end_date):
        
        session = self.SessionLocal()
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        try:
                    
            orders = session.query(Order).filter(
                        Order.estimated_date.between(start_date, end_date),
                        Order.status_id == 2
                    ).options(joinedload(Order.product_type).joinedload(ProductType.product), 
                            joinedload(Order.payment_method),
                            joinedload(Order.status),
                            joinedload(Order.city),
                    ).all()
                    
            payment_methods = {}
            revenues_per_day = {}
            products = {}
            
            revenue = 0
            
            for order in orders:
                
                # Get total revenue data
                
                order_revenue = order.product_type.price + order.added_price
                revenue += order_revenue 
                
                # Get payment methods data
                
                if not payment_methods.get(order.payment_method.name):
                    payment_methods[order.payment_method.name] = 1
                else:
                    payment_methods[order.payment_method.name] += 1
                    
                # Get revenues per day data
                
                date = order.estimated_date.strftime('%Y-%m-%d')
                
                if not revenues_per_day.get(date):
                    revenues_per_day[date] = order_revenue
                else:
                    revenues_per_day[date] += order_revenue
                
                # Get products data
                
                if not products.get(order.product_type.product.name):
                    products[order.product_type.product.name] = 1
                else:
                    products[order.product_type.product.name] += 1
                
            
            result = {'revenue': revenue,
                      'payment_methods_data': payment_methods,
                      'revenues_data': revenues_per_day,
                      'products_data': products
                      }
            
            return result
        
        finally:
            session.close()
        
        
        
      
    # Write Method
    
    def write_order(self, data):
        
        try:
            db_data = Order(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return db_data.id
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El pedido ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar pedido: {str(e)}'}
        finally:
            session.close()

    
    # Update Method


    def update_order(self, order_id, data):
        
        try:
            session = self.SessionLocal()
            order = session.query(Order).filter(Order.id == order_id).first()
            if order and order.status_id == 1:
                order.client = data.get('client')
                order.city_id = data.get('city_id')
                order.product_type_id = data.get('product_type_id')
                order.description = data.get('description')
                order.added_price = data.get('added_price')
                order.credit = data.get('credit')
                order.payment_method_id = data.get('payment_method_id')
                order.estimated_date = data.get('estimated_date')
                session.commit()
                return {'success': True, 'message': 'Pedido actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el pedido con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar pedido: {str(e)}'}
        finally:
            session.close()
            
    
    def deliver_order(self, order_id):
        
        try:
            session = self.SessionLocal()
            order = session.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status_id = 2
                session.commit()
                return {'success': True, 'message': 'Pedido actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el pedido con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar pedido: {str(e)}'}
        finally:
            session.close()
            
    def cancel_order(self, order_id):
        
        try:
            session = self.SessionLocal()
            order = session.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status_id = 3
                session.commit()
                return {'success': True, 'message': 'Pedido actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el pedido con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar pedido: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_order(self, order_id):
        try:
            session = self.SessionLocal()
            order = session.query(Order).filter(Order.id == order_id).first()
            if order:
                session.delete(order)
                session.commit()
                return {'success': True, 'message': 'Pedido eliminado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el pedido con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar el pedido: {str(e)}'}
        finally:
            session.close()
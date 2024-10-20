from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from datetime import datetime
import os

from models.Models import Order

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
    
    def read_current_month_order(self):
        session = self.SessionLocal()
        
        try:
            today = datetime.today()
            current_month = today.month
            current_year = today.year
    
            result = session.query(Order).filter(
                        extract('month', Order.estimated_date) == current_month,
                        extract('year', Order.estimated_date) == current_year,
                    ).options(joinedload(Order.product), 
                              joinedload(Order.product_type), 
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
                    ).options(
                        joinedload(Order.product), 
                        joinedload(Order.product_type), 
                        joinedload(Order.payment_method),
                        joinedload(Order.status),
                        joinedload(Order.city),
                    ).all()
            
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
            return {'success': True, 'message': 'Pedido registrado correctamente.'}
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
            if order:
                order.client = data.get('client')
                order.city = data.get('city')
                order.product = data.get('product')
                order.product_type = data.get('product_type')
                order.description = data.get('description')
                order.added_price = data.get('added_price')
                order.credit = data.get('credit')
                order.payment_method = data.get('payment_method')
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
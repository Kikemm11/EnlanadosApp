from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import OrderWhool

load_dotenv()
database = os.getenv("DATABASE")


class OrderWhoolController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_order_whool_stock(self):
        session = self.SessionLocal()
        result = session.query(OrderWhool).all()
        session.close()
        return result 
    
    
    # Write Method
    
    def write_order_whool_stock(self, data):
        
        try:
            db_data = OrderWhool(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Inventario registrado correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El inventario ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar inventario: {str(e)}'}
        finally:
            session.close()

    
    # Update Method


    def update_order_whool_stock(self, order_id, data):
        
        try:
            session = self.SessionLocal()
            order_whool_stock = session.query(OrderWhool).filter(OrderWhool.order_id == order_id).all()

            for record in order_whool_stock:
                self.delete_order_whool_stock(record.id)
            
            for whool_stock_id in data:
                data = {'order_id': order_id, 'whool_stock_id': whool_stock_id}
                self.write_order_whool_stock(data)
            
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar inventario: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_order_whool_stock(self, order_whool_stock_id):
        try:
            session = self.SessionLocal()
            order_whool_stock = session.query(OrderWhool).filter(OrderWhool.id == order_whool_stock_id).first()
            if order_whool_stock:
                session.delete(order_whool_stock)
                session.commit()
                return {'success': True, 'message': 'Inventario eliminada correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el inventario con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar el inventario: {str(e)}'}
        finally:
            session.close()
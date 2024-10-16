from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import WhoolStock

load_dotenv()
database = os.getenv("DATABASE")


class WhoolStockController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_whool_stock(self):
        session = self.SessionLocal()
        result = session.query(WhoolStock).all()
        session.close()
        return result
       
    def read_one_whool_stock(self, color):
        session = self.SessionLocal()
        result = session.query(WhoolStock).filter(WhoolStock.color == color).first()
        session.close()
        return result    
    
    
    # Write Method
    
    def write_whool_stock(self, data):
        
        try:
            db_data = WhoolStock(**data)
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


    def update_whool_stock(self, whool_stock_id, data):
        
        try:
            session = self.SessionLocal()
            whool_stock = session.query(WhoolStock).filter(WhoolStock.id == whool_stock_id).first()
            if whool_stock:
                whool_stock.color = data.get('color')
                whool_stock.quantity = data.get('quantity')
                session.commit()
                return {'success': True, 'message': 'Inventario actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el inventario con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar inventario: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_whool_stock(self, whool_stock_id):
        try:
            session = self.SessionLocal()
            whool_stock = session.query(WhoolStock).filter(WhoolStock.id == whool_stock_id).first()
            if whool_stock:
                session.delete(whool_stock)
                session.commit()
                return {'success': True, 'message': 'Inventario eliminada correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el inventario con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar el inventario: {str(e)}'}
        finally:
            session.close()
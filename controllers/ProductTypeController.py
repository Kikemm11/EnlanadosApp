from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import ProductType

load_dotenv()
database = os.getenv("DATABASE")


class ProductTypeController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_product_type(self):
        session = self.SessionLocal()
        result = session.query(ProductType).all()
        session.close()
        return result
       
    def read_one_product_type(self, name):
        session = self.SessionLocal()
        result = session.query(ProductType).filter(ProductType.name == name).first()
        session.close()
        return result    
    
    
    # Write Method
    
    def write_product_type(self, data):
        
        try:
            db_data = ProductType(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Tipo de producto registrado correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El tipo de producto ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar tipo de producto: {str(e)}'}
        finally:
            session.close()

    
    # Update Method


    def update_product_type(self, product_type_id, data):
        
        try:
            session = self.SessionLocal()
            product_type = session.query(ProductType).filter(ProductType.id == product_type_id).first()
            if product_type:
                product_type.name = data.get('name')
                product_type.name = data.get('product')
                product_type.name = data.get('price')
                session.commit()
                return {'success': True, 'message': 'Tipo de producto actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de producto con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar tipo de producto: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_product_type(self, product_type_id):
        try:
            session = self.SessionLocal()
            product_type = session.query(ProductType).filter(ProductType.id == product_type_id).first()
            if product_type:
                session.delete(product_type)
                session.commit()
                return {'success': True, 'message': 'Tipo de producto eliminado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de producto con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar el tipo de producto: {str(e)}'}
        finally:
            session.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import Product

load_dotenv()
database = os.getenv("DATABASE")


class ProductController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_product(self):
        session = self.SessionLocal()
        result = session.query(Product).all()
        session.close()
        return result
       
    def read_one_product(self, name):
        session = self.SessionLocal()
        result = session.query(Product).filter(Product.name == name).first()
        session.close()
        return result    
    
    
    # Write Method
    
    def write_product(self, data):
        
        try:
            print("TRY")
            db_data = Product(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            print("COMMIT")
            return {'success': True, 'message': 'Producto registrado correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El producto ya existe.'}
        except Exception as e:
            session.rollback()
            print("ERROR")
            print(e)
            return {'success': False, 'message': f'Error al insertar producto: {str(e)}'}
        finally:
            print("FINALLY")
            session.close()

    
    # Update Method


    def update_product(self, product_id, data):
        
        try:
            session = self.SessionLocal()
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                product.name = data.get('name')
                session.commit()
                return {'success': True, 'message': 'Producto actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el producto con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar producto: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_product(self, product_id):
        try:
            session = self.SessionLocal()
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                session.delete(product)
                session.commit()
                return {'success': True, 'message': 'Producto eliminado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el producto con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar el producto: {str(e)}'}
        finally:
            session.close()
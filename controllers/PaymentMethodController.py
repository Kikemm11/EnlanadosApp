from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import PaymentMethod

load_dotenv()
database = os.getenv("DATABASE")


class PaymentMethodController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_payment_method(self):
        session = self.SessionLocal()
        result = session.query(PaymentMethod).all()
        session.close()
        return result
       
    def read_one_payment_method(self, name):
        session = self.SessionLocal()
        result = session.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        session.close()
        return result    
    
    
    # Write Method
    
    def write_payment_method(self, data):
        
        try:
            db_data = PaymentMethod(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Método de pago registrada correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El método de pago ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar método de pago: {str(e)}'}
        finally:
            session.close()

    
    # Update Method


    def update_payment_method(self, payment_method_id, data):
        
        try:
            session = self.SessionLocal()
            payment_method = session.query(PaymentMethod).filter(PaymentMethod.id == payment_method).first()
            if payment_method:
                payment_method.name = data.get('name')
                session.commit()
                return {'success': True, 'message': 'Método de pago actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el método de pago con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar método de pago: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_payment_method(self, payment_method_id):
        try:
            session = self.SessionLocal()
            payment_method = session.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
            if payment_method:
                session.delete(payment_method)
                session.commit()
                return {'success': True, 'message': 'Método de pago eliminado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el método de pago con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar la método de pago: {str(e)}'}
        finally:
            session.close()
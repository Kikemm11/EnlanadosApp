from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import City

load_dotenv()
database = os.getenv("DATABASE")


class CityController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_city(self):
        session = self.SessionLocal()
        result = session.query(City).all()
        session.close()
        return result
       
    def read_one_city(self, name):
        session = self.SessionLocal()
        result = session.query(City).filter(City.name == name).first()
        session.close()
        return result    
    
    
    # Write Method
    
    def write_city(self, data):
        
        try:
            db_data = City(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Ciudad registrada correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'La ciudad ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar ciudad: {str(e)}'}
        finally:
            session.close()

    
    # Update Method


    def update_city(self, city_id, data):
        
        try:
            session = self.SessionLocal()
            city = session.query(City).filter(City.id == city_id).first()
            if city:
                city.name = data.get('name')
                session.commit()
                return {'success': True, 'message': 'Ciudad actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró la ciudad con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar ciudad: {str(e)}'}
        finally:
            session.close()
            
            
    # Delete Method


    def delete_city(self, city_id):
        try:
            session = self.SessionLocal()
            city = session.query(City).filter(City.id == city_id).first()
            if city:
                session.delete(city)
                session.commit()
                return {'success': True, 'message': 'Ciudad eliminada correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró la ciudad con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar la ciudad: {str(e)}'}
        finally:
            session.close()
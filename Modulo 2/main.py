from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mariadb+mariadbconnector://usuario:contraseña@localhost/recetas"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Receta(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ingredientes = Column(String)
    pasos = Column(String)

def agregar_receta(db, nombre, ingredientes, pasos):
    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    db.add(nueva_receta)
    db.commit()
    db.refresh(nueva_receta)
    print("Receta agregada con éxito.")

def actualizar_receta(db, id_receta, nombre, ingredientes, pasos):
    receta = db.query(Receta).filter(Receta.id == id_receta).first()
    receta.nombre = nombre
    receta.ingredientes = ingredientes
    receta.pasos = pasos
    db.commit()
    print("Receta actualizada con éxito.")

def eliminar_receta(db, id_receta):
    receta = db.query(Receta).filter(Receta.id == id_receta).first()
    db.delete(receta)
    db.commit()
    print("Receta eliminada con éxito.")

def ver_recetas(db):
    recetas = db.query(Receta).all()
    for receta in recetas:
        print(f"ID: {receta.id}, Nombre: {receta.nombre}, Ingredientes: {receta.ingredientes}, Pasos: {receta.pasos}")

def buscar_receta(db, nombre):
    recetas = db.query(Receta).filter(Receta.nombre.like(f"%{nombre}%")).all()
    for receta in recetas:
        print(f"ID: {receta.id}, Nombre: {receta.nombre}, Ingredientes: {receta.ingredientes}, Pasos: {receta.pasos}")

def menu():
    with SessionLocal() as db:
        while True:
            print("\nOpciones:")
            print(" a) Agregar nueva receta")
            print("b) Actualizar receta existente")
            print("c) Eliminar receta existente")
            print("d) Ver listado de recetas")
            print("e) Buscar ingredientes y pasos de receta")
            print("f) Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == 'a':
                nombre = input("Nombre de la receta: ")
                ingredientes = input("Ingredientes (separados por comas): ")
                pasos = input("Pasos: ")
                agregar_receta(db, nombre, ingredientes, pasos)
            elif opcion == 'b':
                id_receta = input("ID de la receta a actualizar: ")
                nombre = input("Nuevo nombre de la receta: ")
                ingredientes = input("Nuevos ingredientes (separados por comas): ")
                pasos = input("Nuevos pasos: ")
                actualizar_receta(db, id_receta, nombre, ingredientes, pasos)
            elif opcion == 'c':
                id_receta = input("ID de la receta a eliminar: ")
                eliminar_receta(db, id_receta)
            elif opcion == 'd':
                ver_recetas(db)
            elif opcion == 'e':
                nombre = input("Nombre de la receta a buscar: ")
                buscar_receta(db, nombre)
            elif opcion == 'f':
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

menu()

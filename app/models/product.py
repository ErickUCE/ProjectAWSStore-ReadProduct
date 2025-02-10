from sqlalchemy import Column, Integer, String, DECIMAL
from app.database import Base

class Product(Base):
    __tablename__ = "Products"  # 📌 Asegúrate de que el nombre coincide con MySQL

    id = Column(Integer, primary_key=True, index=True)
    nombreProducto = Column(String(255), nullable=False)
    descripcion = Column(String(500))
    marca = Column(String(100), nullable=False)
    precio = Column(DECIMAL(10,2), nullable=False)
    proveedor_id = Column(Integer, nullable=False)
    proveedor_nombre = Column(String(255), nullable=True)  # Se almacena el nombre del proveedor

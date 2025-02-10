from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.controllers.productController as product_controller  # ✅ Evita importaciones circulares

router = APIRouter()

# 📌 Obtener todos los productos
@router.get("/products")  # ✅ FastAPI ya entiende que es un GET
def read_products(db: Session = Depends(get_db)):
    return product_controller.get_all_products(db)

# 📌 Obtener un producto por ID
@router.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_controller.get_product_by_id(db, product_id)
    if not product:
        return {"error": "Producto no encontrado"}
    return product

# 📌 Sincronizar producto desde `CreateProduct`
@router.post("/sync-create")  # ✅ No necesitas 'methods=["POST"]'
def sync_product(product_data: dict, db: Session = Depends(get_db)):
    return product_controller.sync_create_product(product_data, db)

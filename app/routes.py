from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.controllers.productController as product_controller  # ✅ Evita importaciones circulares
from app.controllers.productController import sync_update_product
from app.models.product import Product


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


# 📌 Endpoint para recibir actualizaciones desde `UpdateProduct`
@router.post("/sync-update")
def sync_product_update(product_data: dict, db: Session = Depends(get_db)):
    return sync_update_product(product_data, db)

@router.post("/sync-delete")
def sync_delete_product(product_data: dict, db: Session = Depends(get_db)):
    """Elimina el producto en `CreateProduct` cuando `DeleteProduct` lo notifica."""
    
    print(f"🔍 Recibiendo solicitud de eliminación: {product_data}")  # Debugging

    product_id = product_data.get("id")  # ✅ Extraer ID del producto

    if not product_id:
        print("❌ Error: ID de producto no encontrado en la solicitud")
        return {"error": "ID de producto no encontrado en la solicitud"}

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        print(f"⚠️ Producto con ID {product_id} no encontrado en read.")
        return {"error": "Producto no encontrado en read"}

    db.delete(product)
    db.commit()

    print(f"✅ Producto eliminado en Read: {product_id}")

    return {"message": "Producto eliminado correctamente"}




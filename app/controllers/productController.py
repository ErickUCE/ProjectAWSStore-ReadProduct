from sqlalchemy.orm import Session
from app.models.product import Product



def get_all_products(db: Session):
    """ 📌 Obtener todos los productos """
    products = db.query(Product).all()
    
    # 🔥 Convertir Decimal a float en la respuesta
    return [
        {
            "id": product.id,
            "nombreProducto": product.nombreProducto,
            "descripcion": product.descripcion,
            "marca": product.marca,
            "precio": float(product.precio),  # ✅ Convertir Decimal a float
            "proveedor_id": product.proveedor_id,
            "proveedor_nombre": product.proveedor_nombre
        }
        for product in products
    ]

def get_product_by_id(db: Session, product_id: int):
    """ 📌 Obtener un producto por ID """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    # 🔥 Convertir Decimal a float antes de devolver
    return {
        "id": product.id,
        "nombreProducto": product.nombreProducto,
        "descripcion": product.descripcion,
        "marca": product.marca,
        "precio": float(product.precio),  # ✅ Convertir Decimal a float
        "proveedor_id": product.proveedor_id,
        "proveedor_nombre": product.proveedor_nombre
    }


def sync_create_product(product_data: dict, db: Session):
    """ 📌 Sincronizar un producto creado en CreateProduct """
    db_product = Product(
        id=product_data["id"],  # 🔹 Asegura que el ID coincide con el de CreateProduct
        nombreProducto=product_data["nombreProducto"],
        descripcion=product_data["descripcion"],
        marca=product_data["marca"],
        precio=product_data["precio"],
        proveedor_id=product_data["proveedor_id"],
        proveedor_nombre=product_data["proveedor_nombre"],
    )
    
    # 🔥 Verifica si el producto ya existe antes de insertarlo
    existing_product = db.query(Product).filter(Product.id == db_product.id).first()
    if existing_product:
        print(f"⚠️ Producto con ID {db_product.id} ya existe en ReadProduct.")
        return
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(f"✅ Producto sincronizado en ReadProduct: {db_product.nombreProducto}")
    return db_product


def sync_update_product(product_data: dict, db: Session):
    """ 📌 Sincronizar la actualización del producto desde `UpdateProduct` """
    
    db_product = db.query(Product).filter(Product.id == product_data["id"]).first()
    if not db_product:
        print(f"⚠️ Producto con ID {product_data['id']} no encontrado en ReadProduct.")
        return {"error": "Producto no encontrado en ReadProduct"}

    # 🔄 Actualizar los datos del producto
    for key, value in product_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    
    print(f"✅ Producto sincronizado en ReadProduct: {db_product.nombreProducto}")
    return db_product
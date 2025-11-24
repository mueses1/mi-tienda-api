from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from schemas.product import ProductInDB, ProductCreate, ProductUpdate
from crud.firebase_crud import FirebaseProductCRUD
from pathlib import Path
import os
import shutil

router = APIRouter()

product_crud = FirebaseProductCRUD()
UPLOAD_DIR = Path("static") / "products"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[ProductInDB])
def get_all_products():
    return product_crud.get_all()


@router.get("/{product_id}", response_model=ProductInDB)
def get_product(product_id: str):
    product = product_crud.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    new_product = product_crud.create(product.model_dump())
    return new_product


@router.post("/with-image", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product_with_image(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    category: str = Form(...),
    file: Optional[UploadFile] = File(None),
):
    data = {
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
    }

    new_product = product_crud.create(data)

    if file is None:
        return new_product

    # Validar extensión simple
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado")

    filename = f"{new_product['id']}{ext}"
    dest_path = UPLOAD_DIR / filename

    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/products/{filename}"
    updated = product_crud.update(new_product["id"], {"image_url": image_url})
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated


@router.put("/{product_id}", response_model=ProductInDB)
def update_product(product_id: str, product_update: ProductUpdate):
    update_data = product_update.model_dump(exclude_unset=True)
    updated = product_crud.update(product_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    deleted = product_crud.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None


@router.post("/{product_id}/image", response_model=ProductInDB)
def upload_product_image(product_id: str, file: UploadFile = File(...)):
    product = product_crud.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validar extensión simple
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado")

    filename = f"{product_id}{ext}"
    dest_path = UPLOAD_DIR / filename

    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/products/{filename}"
    updated = product_crud.update(product_id, {"image_url": image_url})
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated
from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.cart import Cart, CartItem
from crud.firebase_crud import FirebaseCartCRUD, FirebaseProductCRUD

router = APIRouter()

cart_crud = FirebaseCartCRUD()
product_crud = FirebaseProductCRUD()


@router.get("/{user_id}", response_model=Cart)
def get_cart(user_id: str):
    cart_data = cart_crud.get_cart(user_id)
    return Cart(user_id=cart_data["user_id"], items=cart_data.get("items", []))


@router.post("/{user_id}/items", response_model=Cart, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(user_id: str, item: CartItem):
    product = product_crud.get_by_id(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    stored_item = {
        "product_id": item.product_id,
        "name": item.name or product.get("name"),
        "price": float(item.price or product.get("price", 0)),
        "quantity": item.quantity,
        "image_url": item.image_url or product.get("image_url"),
    }
    cart_data = cart_crud.add_or_update_item(user_id, stored_item)
    return Cart(user_id=cart_data["user_id"], items=cart_data.get("items", []))


@router.delete("/{user_id}/items/{product_id}", response_model=Cart)
def remove_item_from_cart(user_id: str, product_id: str):
    cart_data = cart_crud.remove_item(user_id, product_id)
    return Cart(user_id=cart_data["user_id"], items=cart_data.get("items", []))


@router.delete("/{user_id}", response_model=Cart)
def clear_cart(user_id: str):
    cart_data = cart_crud.clear_cart(user_id)
    return Cart(user_id=cart_data["user_id"], items=cart_data.get("items", []))

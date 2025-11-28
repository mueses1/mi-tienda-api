import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.cart import Cart, CartItem, CheckoutRequest, CheckoutResponse, PaymentDetails
from crud.firebase_crud import FirebaseCartCRUD, FirebaseProductCRUD, FirebaseOrderCRUD

router = APIRouter()

cart_crud = FirebaseCartCRUD()
product_crud = FirebaseProductCRUD()
order_crud = FirebaseOrderCRUD()


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


@router.post("/{user_id}/checkout", response_model=CheckoutResponse)
def checkout_cart(user_id: str, checkout: CheckoutRequest):
    cart_data = cart_crud.get_cart(user_id)
    items = cart_data.get("items", [])
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El carrito está vacío",
        )

    total = sum(float(item.get("price", 0)) * int(item.get("quantity", 1)) for item in items)

    payment_details: Optional[dict] = None

    if checkout.payment_method == "tarjeta":
        data = checkout.payment_data
        if not data or not data.card_holder or not data.card_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos de tarjeta incompletos",
            )
        card_last4 = data.card_number[-4:]
        transaction_id = f"TX-{uuid.uuid4().hex[:10]}"
        payment_details = {
            "method": "tarjeta",
            "card_holder": data.card_holder,
            "card_last4": card_last4,
            "transaction_id": transaction_id,
        }
    elif checkout.payment_method == "transferencia":
        data = checkout.payment_data
        if not data or not data.transfer_holder or not data.transfer_bank or not data.transfer_account_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos de transferencia incompletos",
            )
        payment_details = {
            "method": "transferencia",
            "transfer_holder": data.transfer_holder,
            "transfer_bank": data.transfer_bank,
            "transfer_account_type": data.transfer_account_type,
            "transfer_account_number": data.transfer_account_number,
        }
    else:
        payment_details = {
            "method": checkout.payment_method,
        }

    order_data = {
        "user_id": user_id,
        "items": items,
        "total": total,
        "payment_method": checkout.payment_method,
        "status": "creada",
        "payment_details": payment_details,
    }

    created_order = order_crud.create(order_data)

    cart_crud.clear_cart(user_id)

    return CheckoutResponse(
        order_id=created_order["id"],
        user_id=user_id,
        items=[CartItem(**item) for item in items],
        total=total,
        payment_method=checkout.payment_method,
        status=order_data["status"],
        payment_details=PaymentDetails(**payment_details) if payment_details else None,
    )

from typing import List, Optional
from pydantic import BaseModel
from typing import Literal


class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image_url: Optional[str] = None


class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []


class PaymentData(BaseModel):
    card_holder: Optional[str] = None
    card_number: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    cvv: Optional[str] = None
    transfer_holder: Optional[str] = None
    transfer_bank: Optional[str] = None
    transfer_account_type: Optional[str] = None
    transfer_account_number: Optional[str] = None


class PaymentDetails(BaseModel):
    method: Literal["efectivo", "transferencia", "tarjeta"]
    card_holder: Optional[str] = None
    card_last4: Optional[str] = None
    transaction_id: Optional[str] = None
    transfer_holder: Optional[str] = None
    transfer_bank: Optional[str] = None
    transfer_account_type: Optional[str] = None
    transfer_account_number: Optional[str] = None


class CheckoutRequest(BaseModel):
    payment_method: Literal["efectivo", "transferencia", "tarjeta"]
    payment_data: Optional[PaymentData] = None


class CheckoutResponse(BaseModel):
    order_id: str
    user_id: str
    items: List[CartItem]
    total: float
    payment_method: Literal["efectivo", "transferencia", "tarjeta"]
    status: str
    payment_details: Optional[PaymentDetails] = None

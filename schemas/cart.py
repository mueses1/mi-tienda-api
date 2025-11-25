from typing import List, Optional
from pydantic import BaseModel


class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image_url: Optional[str] = None


class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []

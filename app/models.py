from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = Field(None, description="Auto-assigned by server")
    name: str = Field(..., description="Name of the item", json_schema_extra={"example": "Laptop"})
    description: Optional[str] = Field(None, description="Item description", json_schema_extra={"example": "Dell Inspiron 15"})
    price: float = Field(..., description="Price in USD, must be greater than 0", gt=0, json_schema_extra={"example": 999.99})
    in_stock: bool = Field(True, description="Whether item is in stock", json_schema_extra={"example": True})
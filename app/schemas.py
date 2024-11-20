from pydantic import BaseModel
from typing import Dict, List, Optional

class ProductSpecifications(BaseModel):
    color: Optional[str]
    dimensions: Optional[str]
    wattage: Optional[str]
    type: Optional[str]
    material: Optional[str]

class ProductMetadata(BaseModel):
    name: str
    description: Optional[str]
    specifications: Optional[ProductSpecifications]
    category: Optional[str]
    price: Optional[float]
    sku: Optional[str]

class ProductSchema(BaseModel):
    id: str
    metadata: ProductMetadata
    image_url: Optional[str] 
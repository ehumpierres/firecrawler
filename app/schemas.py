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

class ExtractedData(BaseModel):
    name: Optional[str]
    description: Optional[str]
    color: Optional[str]
    width_diameter: Optional[str]
    height: Optional[str]
    wattage: Optional[str]
    type: Optional[str]
    material: Optional[str]
    price: Optional[str]
    sku: Optional[str]
    image_url: Optional[str]

class ScrapedData(BaseModel):
    url: str
    raw_html: str
    markdown: str
    extracted_data: Optional[ExtractedData]
    status: str 
from pydantic import BaseModel, Field


class HealthOut(BaseModel):
    status: str


class ReadinessOut(BaseModel):
    status: str
    checks: dict[str, str]


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class ProductListOut(BaseModel):
    items: list[ProductOut]
    count: int


class OrderCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)


class OrderOut(BaseModel):
    order_id: str
    product_id: int
    quantity: int
    unit_price: float
    total: float
    status: str

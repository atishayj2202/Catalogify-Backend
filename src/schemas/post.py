from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.utils.enums import PostCategory


class PostCreateRequest(BaseModel):
    title: str
    category: PostCategory
    images: list[str]
    description: str
    cost: float
    brand: str = "unbranded"
    warranty_months: int = 0
    return_days: int = 0
    seller_location: str | None = None
    in_box: str | None = None


class PostLongResponse(BaseModel):
    id: UUID
    created_at: datetime
    user_id: UUID
    title: str
    category: PostCategory
    images: list[str]
    description: str
    cost: float
    brand: str = "unbranded"
    warranty_yrs: int = 0
    warranty_months: int = 0
    return_days: int = 0
    seller_location: str | None = None
    in_box: str | None = None


class PostResponse(BaseModel):
    id: UUID
    created_at: datetime
    data: PostLongResponse | None = None
    score: int
    likes: int = 0


class PostEditRequest(BaseModel):
    title: str | None = None
    images: list[str] | None = None
    description: str | None = None
    cost: float | None = None
    brand: str | None = None
    seller_location: str | None = None
    in_box: str | None = None


class AssessmentResponse(BaseModel):
    post_id: UUID
    assessment1: bool
    assessment2: list[str]
    assessment3: bool
    assessment4: bool
    assessment5: bool
    recommendation: str
    total: int

from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase
from src.utils.enums import PostCategory


class Post(DBSchemaBase):
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
    is_deleted: datetime | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Post


_Post = Base.from_schema_base(Post, "posts")

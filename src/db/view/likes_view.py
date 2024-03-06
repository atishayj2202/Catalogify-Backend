from typing import Type

from src.db.base import Base, DBSchemaBase
from src.utils.enums import PostCategory


class LikesView(DBSchemaBase):
    post_category: PostCategory
    positive_reactions: int

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _LikesView


_LikesView = Base.from_schema_base(LikesView, "post_likes")

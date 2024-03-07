from typing import Type

from src.db.base import Base, DBSchemaBase
from src.utils.enums import PostCategory


class AssessmentView(DBSchemaBase):
    post_category: PostCategory
    post_score: int

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _AssessmentView


_AssessmentView = Base.from_schema_base(AssessmentView, "post_assessments")

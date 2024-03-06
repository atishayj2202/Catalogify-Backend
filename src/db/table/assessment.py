from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Assessment(DBSchemaBase):
    post_id: UUID
    assessment1: bool = True
    assessment2: list[str] = []
    assessment3: bool = True
    assessment4: bool = True
    assessment5: bool = True
    assessment6: str | None = None
    total: int = 100

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Assessment


_Assessment = Base.from_schema_base(Assessment, "assessments")

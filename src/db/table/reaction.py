from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Reaction(DBSchemaBase):
    post_id: UUID
    user_id: UUID
    assessment1: bool = True

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Reaction


_Reaction = Base.from_schema_base(Reaction, "reactions")

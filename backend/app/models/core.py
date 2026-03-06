from pydantic import BaseModel, Field
from typing import Optional
import datetime


class CoreModel(BaseModel):
    pass


class IdModelMixin(BaseModel):
    id: int


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

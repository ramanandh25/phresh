from pydantic import BaseModel


class CoreModel(BaseModel):
    pass


class IdModelMixin(BaseModel):
    id: int

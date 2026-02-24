from typing import Optional 
from enum import Enum 
from backend.app.models.core import CoreModel, IdModelMixin


class CleaningType(str, Enum):
    dust_up = "dust_up"
    full_clean = "full_clean"
    spot_clean = "spot_clean"


class CleaningBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    cleaning_type: Optional[CleaningType]="spot_clean"
    price: Optional[float]


class CleaningCreate(CleaningBase):
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType]


class CleaninginDb(IdModelMixin, CleaningBase):
    name: str
    price: float


class CleaningPublic(IdModelMixin, CleaningBase):
    pass 

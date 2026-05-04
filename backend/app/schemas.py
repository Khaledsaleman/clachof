from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    telegram_id: str
    username: Optional[str] = None

class UserCreate(UserBase):
    pass

class BuildingBase(BaseModel):
    type: str
    x: int
    y: int

class BuildingCreate(BuildingBase):
    pass

class BuildingSchema(BuildingBase):
    id: int
    level: int
    upgrade_end_time: Optional[datetime] = None
    class Config:
        from_attributes = True

class UnitSchema(BaseModel):
    type: str
    level: int
    count: int
    class Config:
        from_attributes = True

class UserSchema(UserBase):
    id: int
    gold: float
    energy: float
    max_energy: float
    rank: int
    clan_id: Optional[int] = None
    buildings: List[BuildingSchema] = []
    units: List[UnitSchema] = []
    class Config:
        from_attributes = True

class ClanBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClanCreate(ClanBase):
    pass

class ClanSchema(ClanBase):
    id: int
    leader_id: int
    class Config:
        from_attributes = True

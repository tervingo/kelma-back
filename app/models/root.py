from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal
from bson import ObjectId


class ModeFields(BaseModel):
    """Sub-fields for each mode type."""
    act_agt: str = ""
    act_pat: str = ""
    pas_agt: str = ""
    pas_pat: str = ""


class ModeData(BaseModel):
    """Mode data structure containing base and optional modes."""
    base: ModeFields  # Mandatory
    long: Optional[ModeFields] = None
    strong: Optional[ModeFields] = None
    redup: Optional[ModeFields] = None


class RootBase(BaseModel):
    """Base model for Root without ID."""
    root: str = Field(..., description="Root text")
    prim: str | None = None
    mode: ModeData = Field(..., description="Mode data with base and optional modes")


class RootCreate(RootBase):
    """Model for creating a new root."""
    pass


class RootUpdate(BaseModel):
    """Model for updating a root (all fields optional)."""
    root: Optional[str] = None
    prim: Optional[str] = None
    mode: Optional[ModeData] = None


class Root(RootBase):
    """Model for Root with ID."""
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

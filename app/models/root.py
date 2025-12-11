from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId


class ModeFields(BaseModel):
    """Sub-fields for each mode type - all optional but at least one must be filled."""
    prim: str | None = None
    act_agt: str | None = None
    act_pat: str | None = None
    pas_agt: str | None = None
    pas_pat: str | None = None

    @field_validator('*', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None."""
        if v == "":
            return None
        return v

    def has_any_value(self) -> bool:
        """Check if at least one field has a value."""
        return any([self.prim, self.act_agt, self.act_pat, self.pas_agt, self.pas_pat])


class ModeData(BaseModel):
    """Mode data structure containing base and optional modes."""
    base: ModeFields  # Mandatory
    long: Optional[ModeFields] = None
    strong: Optional[ModeFields] = None

    @field_validator('base')
    @classmethod
    def validate_base_has_value(cls, v):
        """Ensure base mode has at least one field filled."""
        if not v.has_any_value():
            raise ValueError('Base mode must have at least one field filled')
        return v

    @field_validator('long', 'strong')
    @classmethod
    def validate_optional_mode_has_value(cls, v):
        """Ensure optional modes have at least one field filled if present."""
        if v is not None and not v.has_any_value():
            raise ValueError('Mode must have at least one field filled')
        return v


class RootBase(BaseModel):
    """Base model for Root without ID."""
    root: str = Field(..., description="Root text")
    mode: ModeData = Field(..., description="Mode data with base and optional modes")


class RootCreate(RootBase):
    """Model for creating a new root."""
    pass


class RootUpdate(BaseModel):
    """Model for updating a root (all fields optional)."""
    root: Optional[str] = None
    mode: Optional[ModeData] = None


class Root(RootBase):
    """Model for Root with ID."""
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

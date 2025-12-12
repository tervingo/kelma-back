from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal
from bson import ObjectId


class NounFields(BaseModel):
    """Fields specific to nouns."""
    abs_plural: str = Field(..., description="Absolutive plural")
    abs_plural2: str | None = Field(None, description="Absolutive plural 2 (optional)")
    erg_plural: str = Field(..., description="Ergative plural")
    gen_plural: str = Field(..., description="Genitive plural")
    dat_plural: str = Field(..., description="Dative plural")
    par: str = Field(..., description="Partitive")


class VerbFields(BaseModel):
    """Fields specific to verbs."""
    inf_i: str = Field(..., description="Infinitive I")
    prog_stem: str = Field(..., description="Progressive stem")
    perf_stem: str = Field(..., description="Perfect stem")
    n_part: str = Field(..., description="N-participle")
    t_part: str = Field(..., description="T-participle")
    s_part: str = Field(..., description="S-participle")
    v_part: str = Field(..., description="V-participle")


class TranslationBase(BaseModel):
    """Base model for Translation without ID."""
    kelma: str = Field(..., description="Word in conlang")
    english: str = Field(..., description="English translation")
    root: str = Field(..., description="Root reference")
    swadesh: bool = Field(default=False, description="Part of Swadesh list")
    cat: Literal[
        "adjective", "adverb", "conjunction", "interjection",
        "noun", "prefix", "pronoun", "quantifier", "suffix", "verb"
    ] = Field(..., description="Category")

    # Conditional fields
    noun_type: Optional[Literal["primary", "radical", "deverbal"]] = None
    noun_fields: Optional[NounFields] = None
    verb_fields: Optional[VerbFields] = None

    @model_validator(mode='after')
    def validate_category_fields(self):
        """Ensure category-specific fields are present when needed."""
        if self.cat == "noun":
            if self.noun_type is None:
                raise ValueError("noun_type is required when category is 'noun'")
            if self.noun_fields is None:
                raise ValueError("noun_fields are required when category is 'noun'")
        else:
            # If not noun, these fields should not be present
            if self.noun_type is not None:
                raise ValueError("noun_type should only be set when category is 'noun'")
            if self.noun_fields is not None:
                raise ValueError("noun_fields should only be set when category is 'noun'")

        if self.cat == "verb":
            if self.verb_fields is None:
                raise ValueError("verb_fields are required when category is 'verb'")
        else:
            # If not verb, these fields should not be present
            if self.verb_fields is not None:
                raise ValueError("verb_fields should only be set when category is 'verb'")

        return self


class TranslationCreate(TranslationBase):
    """Model for creating a new translation."""
    pass


class TranslationUpdate(BaseModel):
    """Model for updating a translation (all fields optional)."""
    kelma: Optional[str] = None
    english: Optional[str] = None
    root: Optional[str] = None
    swadesh: Optional[bool] = None
    cat: Optional[Literal[
        "adjective", "adverb", "conjunction", "interjection",
        "noun", "prefix", "pronoun", "quantifier", "suffix", "verb"
    ]] = None
    noun_type: Optional[Literal["primary", "radical", "deverbal"]] = None
    noun_fields: Optional[NounFields] = None
    verb_fields: Optional[VerbFields] = None


class Translation(TranslationBase):
    """Model for Translation with ID."""
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

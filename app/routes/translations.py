from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models.translation import Translation, TranslationCreate, TranslationUpdate
from ..services.translation_service import TranslationService
from ..config.database import get_db

router = APIRouter(prefix="/translations", tags=["translations"])


def get_translation_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> TranslationService:
    """Dependency to get TranslationService instance."""
    return TranslationService(db)


@router.get("/search", response_model=List[Translation])
async def search_translations(
    q: str = Query(..., min_length=1, description="Search query"),
    service: TranslationService = Depends(get_translation_service)
):
    """Search translations by kelma, english, or root."""
    return await service.search(q)


@router.get("/by-root/{root}", response_model=List[Translation])
async def get_translations_by_root(
    root: str,
    service: TranslationService = Depends(get_translation_service)
):
    """Get all translations for a specific root."""
    return await service.get_by_root(root)


@router.get("/{translation_id}", response_model=Translation)
async def get_translation(
    translation_id: str,
    service: TranslationService = Depends(get_translation_service)
):
    """Get a translation by ID."""
    translation = await service.get_by_id(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


@router.get("", response_model=List[Translation])
async def get_all_translations(service: TranslationService = Depends(get_translation_service)):
    """Get all translations."""
    return await service.get_all()


@router.post("", response_model=Translation, status_code=201)
async def create_translation(
    translation_data: TranslationCreate,
    service: TranslationService = Depends(get_translation_service)
):
    """Create a new translation."""
    return await service.create(translation_data)


@router.put("/{translation_id}", response_model=Translation)
async def update_translation(
    translation_id: str,
    translation_data: TranslationUpdate,
    service: TranslationService = Depends(get_translation_service)
):
    """Update a translation by ID."""
    translation = await service.update(translation_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


@router.delete("/{translation_id}", status_code=204)
async def delete_translation(
    translation_id: str,
    service: TranslationService = Depends(get_translation_service)
):
    """Delete a translation by ID."""
    success = await service.delete(translation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Translation not found")
    return None

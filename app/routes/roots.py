from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models.root import Root, RootCreate, RootUpdate
from ..services.root_service import RootService
from ..config.database import get_db

router = APIRouter(prefix="/roots", tags=["roots"])


def get_root_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> RootService:
    """Dependency to get RootService instance."""
    return RootService(db)


@router.get("", response_model=List[Root])
async def get_all_roots(service: RootService = Depends(get_root_service)):
    """Get all roots."""
    return await service.get_all()


@router.get("/search", response_model=List[Root])
async def search_roots(
    q: str = Query(..., min_length=1, description="Search query"),
    service: RootService = Depends(get_root_service)
):
    """Search roots by root text or primary meaning."""
    return await service.search(q)


@router.get("/{root_id}", response_model=Root)
async def get_root(
    root_id: str,
    service: RootService = Depends(get_root_service)
):
    """Get a root by ID."""
    root = await service.get_by_id(root_id)
    if not root:
        raise HTTPException(status_code=404, detail="Root not found")
    return root


@router.post("", response_model=Root, status_code=201)
async def create_root(
    root_data: RootCreate,
    service: RootService = Depends(get_root_service)
):
    """Create a new root."""
    return await service.create(root_data)


@router.put("/{root_id}", response_model=Root)
async def update_root(
    root_id: str,
    root_data: RootUpdate,
    service: RootService = Depends(get_root_service)
):
    """Update a root by ID."""
    root = await service.update(root_id, root_data)
    if not root:
        raise HTTPException(status_code=404, detail="Root not found")
    return root


@router.delete("/{root_id}", status_code=204)
async def delete_root(
    root_id: str,
    service: RootService = Depends(get_root_service)
):
    """Delete a root by ID."""
    success = await service.delete(root_id)
    if not success:
        raise HTTPException(status_code=404, detail="Root not found")
    return None

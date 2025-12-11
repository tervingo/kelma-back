from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.root import Root, RootCreate, RootUpdate


class RootService:
    """Service for Root CRUD operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.roots
    
    async def get_all(self) -> List[Root]:
        """Get all roots."""
        cursor = self.collection.find({})
        roots = await cursor.to_list(length=None)
        return [Root(**{**root, "_id": str(root["_id"])}) for root in roots]
    
    async def get_by_id(self, root_id: str) -> Optional[Root]:
        """Get a root by ID."""
        try:
            root = await self.collection.find_one({"_id": ObjectId(root_id)})
            if root:
                return Root(**{**root, "_id": str(root["_id"])})
            return None
        except Exception:
            return None
    
    async def create(self, root_data: RootCreate) -> Root:
        """Create a new root."""
        root_dict = root_data.model_dump()
        result = await self.collection.insert_one(root_dict)
        created_root = await self.collection.find_one({"_id": result.inserted_id})
        return Root(**{**created_root, "_id": str(created_root["_id"])})
    
    async def update(self, root_id: str, root_data: RootUpdate) -> Optional[Root]:
        """Update a root by ID."""
        try:
            update_data = {k: v for k, v in root_data.model_dump(exclude_unset=True).items() if v is not None}
            if not update_data:
                return await self.get_by_id(root_id)
            
            result = await self.collection.update_one(
                {"_id": ObjectId(root_id)},
                {"$set": update_data}
            )
            
            if result.matched_count:
                return await self.get_by_id(root_id)
            return None
        except Exception:
            return None
    
    async def delete(self, root_id: str) -> bool:
        """Delete a root by ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(root_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def search(self, query: str) -> List[Root]:
        """Search roots by root text or primary meaning."""
        cursor = self.collection.find({
            "$or": [
                {"root": {"$regex": query, "$options": "i"}},
                {"prim": {"$regex": query, "$options": "i"}}
            ]
        })
        roots = await cursor.to_list(length=None)
        return [Root(**{**root, "_id": str(root["_id"])}) for root in roots]

from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.translation import Translation, TranslationCreate, TranslationUpdate


class TranslationService:
    """Service for Translation CRUD operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.translations

    async def get_all(self) -> List[Translation]:
        """Get all translations."""
        cursor = self.collection.find({})
        translations = await cursor.to_list(length=None)
        return [Translation(**{**trans, "_id": str(trans["_id"])}) for trans in translations]

    async def get_by_id(self, translation_id: str) -> Optional[Translation]:
        """Get a translation by ID."""
        try:
            translation = await self.collection.find_one({"_id": ObjectId(translation_id)})
            if translation:
                return Translation(**{**translation, "_id": str(translation["_id"])})
            return None
        except Exception:
            return None

    async def create(self, translation_data: TranslationCreate) -> Translation:
        """Create a new translation."""
        translation_dict = translation_data.model_dump(exclude_none=True)
        result = await self.collection.insert_one(translation_dict)
        created_translation = await self.collection.find_one({"_id": result.inserted_id})
        return Translation(**{**created_translation, "_id": str(created_translation["_id"])})

    async def update(self, translation_id: str, translation_data: TranslationUpdate) -> Optional[Translation]:
        """Update a translation by ID."""
        try:
            update_data = {k: v for k, v in translation_data.model_dump(exclude_unset=True).items() if v is not None}
            if not update_data:
                return await self.get_by_id(translation_id)

            result = await self.collection.update_one(
                {"_id": ObjectId(translation_id)},
                {"$set": update_data}
            )

            if result.matched_count:
                return await self.get_by_id(translation_id)
            return None
        except Exception:
            return None

    async def delete(self, translation_id: str) -> bool:
        """Delete a translation by ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(translation_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def search(self, query: str) -> List[Translation]:
        """Search translations by kelma, english, or root."""
        cursor = self.collection.find({
            "$or": [
                {"kelma": {"$regex": query, "$options": "i"}},
                {"english": {"$regex": query, "$options": "i"}},
                {"root": {"$regex": query, "$options": "i"}}
            ]
        })
        translations = await cursor.to_list(length=None)
        return [Translation(**{**trans, "_id": str(trans["_id"])}) for trans in translations]

    async def get_by_root(self, root: str) -> List[Translation]:
        """Get all translations for a specific root."""
        cursor = self.collection.find({"root": root})
        translations = await cursor.to_list(length=None)
        return [Translation(**{**trans, "_id": str(trans["_id"])}) for trans in translations]

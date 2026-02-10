import hashlib
import time
from fastapi import HTTPException

from app.configs.firebase import get_firestore, create_document
from app.configs.supabase import get_supabase
from app.utils import db_utils as db


def generate_uid(user_data: dict) -> str:
    """Generate a hashed 32-character alphanumeric UID for Firestore document."""
    unique_string = f"{user_data.get('email', '')}{user_data.get('username', '')}{time.time()}"
    hash_obj = hashlib.sha256(unique_string.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex[:32]


async def sync_user_to_firestore(user_data: dict, supabase_id: int):
    """Sync user to Firestore with hashed 32-digit document ID."""
    try:
        firestore_db = get_firestore()
        if firestore_db:
            doc_id = generate_uid(user_data)
            firestore_data = {
                "supabase_id": supabase_id,
                "email": user_data.get("email"),
                "username": user_data.get("username"),
                "full_name": user_data.get("full_name"),
                "phone_number": user_data.get("phone_number"),
                "uid": doc_id
            }
            firestore_data = {k: v for k, v in firestore_data.items() if v is not None}
            await create_document("users", firestore_data, doc_id)
            return doc_id
    except Exception as e:
        print(f"Firestore sync error: {e}")
    return None


async def get_all_users():
    try:
        users = await db.get_all("users")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}") from e


async def get_user(user_id: int):
    try:
        user = await db.get_by_id("users", user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}") from e


async def get_user_by_email(email: str):
    try:
        user = await db.get_by_field("users", "email", email)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}") from e


async def create_user(user_data: dict):
    try:
        # Check if user with email already exists
        existing = await db.get_by_field("users", "email", user_data.get("email"))
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create in Supabase (primary database)
        new_user = await db.create("users", user_data)
        
        # Sync to Firestore
        firestore_doc_id = await sync_user_to_firestore(user_data, new_user.get("id"))
        
        if firestore_doc_id:
            print(f"User created in Firestore with doc ID: {firestore_doc_id}")
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}") from e


async def update_user(user_id: int, user_data: dict):
    try:
        update_data = {k: v for k, v in user_data.items() if v is not None}
        updated_user = await db.update("users", user_id, update_data)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}") from e


async def delete_user(user_id: int):
    try:
        await db.delete("users", user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}") from e

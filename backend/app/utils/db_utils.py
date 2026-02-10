"""
Supabase database utilities.
All CRUD operations now use Supabase instead of SQLAlchemy/SQLite.
"""
from fastapi import HTTPException
from app.configs.supabase import get_supabase


async def get_all(table_name: str):
    """Get all records from a table."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    result = client.table(table_name).select("*").execute()
    return result.data


async def get_all_by_field(table_name: str, field_name: str, field_value):
    """Get all records where field matches value."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    result = client.table(table_name).select("*").eq(field_name, field_value).execute()
    return result.data


async def create(table_name: str, data: dict):
    """Create a new record."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        result = client.table(table_name).insert(data).execute()
        if result.data:
            return result.data[0]
        raise HTTPException(status_code=500, detail="Failed to create record")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def get_by_id(table_name: str, obj_id: int):
    """Get a record by ID."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    result = client.table(table_name).select("*").eq("id", obj_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return result.data[0]


async def update(table_name: str, obj_id: int, data: dict):
    """Update a record by ID."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        result = client.table(table_name).update(data).eq("id", obj_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def delete(table_name: str, obj_id: int):
    """Delete a record by ID."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        result = client.table(table_name).delete().eq("id", obj_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def get_by_fields(table_name: str, fields: dict):
    """Get first record matching all fields."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    query = client.table(table_name).select("*")
    for key, value in fields.items():
        query = query.eq(key, value)
    result = query.limit(1).execute()
    
    if not result.data:
        return None
    return result.data[0]


async def get_by_field(table_name: str, field_name: str, field_value):
    """Get first record where field matches value."""
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    result = client.table(table_name).select("*").eq(field_name, field_value).limit(1).execute()
    if not result.data:
        return None
    return result.data[0]

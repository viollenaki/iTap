from fastapi import HTTPException
from sqlalchemy.future import select
import uuid

from app.configs.db import async_session


async def get_all(model):
    async with async_session() as db:
        result = await db.execute(select(model))
        objs = result.scalars().all()
        return objs
    
async def get_all_by_field(model, field_name: str, field_value):
    """
    Récupère tous les objets du modèle où field_name == field_value.
    """
    async with async_session() as db:
        stmt = select(model).where(getattr(model, field_name) == field_value)
        result = await db.execute(stmt)
        objs = result.scalars().all()
        return objs
    
async def get_all_with_relations(model, options=None):
    """
    Récupère tous les objets du modèle en chargeant explicitement les relations passées dans options.
    :param model: Le modèle SQLAlchemy
    :param options: Liste d'options de chargement (ex: [selectinload(Model.relation)])
    :return: Liste des objets du modèle avec les relations chargées
    """
    async with async_session() as db:
        stmt = select(model)
        if options:
            for opt in options:
                stmt = stmt.options(opt)
        result = await db.execute(stmt)
        objs = result.scalars().all()
        return objs

async def create(model, data: dict):
    async with async_session() as db:
        try:
            obj = model(**data)
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return obj
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e)) from e

async def get_by_id(model, obj_id):
    async with async_session() as db:
        obj = await db.get(model, obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

async def update(model, obj_id, data: dict):
    async with async_session() as db:
        obj = await db.get(model, obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in data.items():
            setattr(obj, key, value)
        try:
            await db.commit()
            await db.refresh(obj)
            return obj
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e)) from e

async def delete(model, obj_id):
    async with async_session() as db:
        obj = await db.get(model, obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        try:
            await db.delete(obj)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e)) from e

async def get_by_fields(model, fields: dict):
    async with async_session() as db:
        stmt = select(model)
        for key, value in fields.items():
            stmt = stmt.where(getattr(model, key) == value)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if not obj:
            return None
        return obj

async def get_by_field(model, field_name: str, field_value):
    async with async_session() as db:
        stmt = select(model).where(getattr(model, field_name) == field_value)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if not obj:
            return None
        return obj

async def update_links(
    link_model,  # ex: RolePermissions
    left_key: str,  # ex: "role_id"
    right_key: str,  # ex: "permission_id"
    left_id,
    right_ids: list
):
    """
    Met à jour les liens d'une table de liaison (many-to-many).
    Supprime les anciens liens et ajoute les nouveaux.
    """
    async with async_session() as db:
        # Supprimer les anciens liens
        await db.execute(
            link_model.__table__.delete().where(getattr(link_model, left_key) == left_id)
        )
        # Ajouter les nouveaux liens
        for right_id in right_ids:
            db.add(link_model(
                id=uuid.uuid4(),
                **{left_key: left_id, right_key: right_id}
            ))
        await db.commit()

async def assign_link(
    link_model,
    left_key: str,
    right_key: str,
    left_id,
    right_id
):
    """
    Assigne un lien dans une table de liaison (many-to-many).
    """
    async with async_session() as db:
        stmt = select(link_model).where(
            (getattr(link_model, left_key) == left_id) &
            (getattr(link_model, right_key) == right_id)
        )
        result = await db.execute(stmt)
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Lien déjà existant.")
        db.add(link_model(
            id=uuid.uuid4(),
            **{left_key: left_id, right_key: right_id}
        ))
        await db.commit()

async def unassign_link(
    link_model,
    left_key: str,
    right_key: str,
    left_id,
    right_id
):
    """
    Désassigne un lien dans une table de liaison (many-to-many).
    """
    async with async_session() as db:
        await db.execute(
            link_model.__table__.delete().where(
                (getattr(link_model, left_key) == left_id) &
                (getattr(link_model, right_key) == right_id)
            )
        )
        await db.commit()

async def delete_links(link_model, left_key: str, left_id):
    async with async_session() as db:
        await db.execute(
            link_model.__table__.delete().where(getattr(link_model, left_key) == left_id)
        )
        await db.commit()
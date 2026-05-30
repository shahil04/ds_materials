from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from . import models, schemas
from .auth import get_password_hash, verify_password

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        name=user.name,
        password_hash=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

async def list_packages(db: AsyncSession, destination: str = None, min_price: float = None, max_price: float = None, min_days: int = None, max_days: int = None):
    q = select(models.Package)
    if destination:
        q = q.where(models.Package.destination.ilike(f"%{destination}%"))
    if min_price is not None:
        q = q.where(models.Package.price >= min_price)
    if max_price is not None:
        q = q.where(models.Package.price <= max_price)
    if min_days is not None:
        q = q.where(models.Package.duration_days >= min_days)
    if max_days is not None:
        q = q.where(models.Package.duration_days <= max_days)
    result = await db.execute(q)
    return result.scalars().all()

async def create_package(db: AsyncSession, package: schemas.PackageCreate):
    db_pkg = models.Package(**package.dict())
    db.add(db_pkg)
    await db.commit()
    await db.refresh(db_pkg)
    return db_pkg

async def get_package(db: AsyncSession, package_id: int):
    result = await db.execute(select(models.Package).where(models.Package.id == package_id))
    return result.scalars().first()

async def update_package(db: AsyncSession, package_id: int, package: schemas.PackageCreate):
    await db.execute(
        update(models.Package)
        .where(models.Package.id == package_id)
        .values(**package.dict())
    )
    await db.commit()
    return await get_package(db, package_id)

async def delete_package(db: AsyncSession, package_id: int):
    await db.execute(delete(models.Package).where(models.Package.id == package_id))
    await db.commit()

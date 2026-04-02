from typing import Optional

from sqlalchemy import select, func, update, ColumnElement
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.domain.filters.product_filters import ProductSearchFilters
from app.infrastructure.db.models import ProductModel
from app.core.database import SessionLocal


class ProductRepositoryImpl(ProductRepository):
    async def get_products(self):
        async with SessionLocal() as session:
            result = await session.execute(select(ProductModel))
            product_models = result.scalars().all()

            count_result = await session.execute(
                select(func.count()).select_from(ProductModel)
            )
            count = count_result.scalar_one()

            products = [
                Product(
                    id=product_model.id,
                    name=product_model.name,
                    stock=product_model.stock,
                    price=product_model.price,
                )
                for product_model in product_models
            ]
            return products, count
            

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product_model = result.scalar_one_or_none()
            if not product_model:
                return None
            return Product(
                product_model.id,
                product_model.name,
                product_model.stock,
                product_model.price,
            )
        

    async def get_product_by_name(self, name: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.name == name)
            )
            product_model = result.scalar_one_or_none()
            if not product_model:
                return None
            return Product(
                product_model.id,
                product_model.name,
                product_model.stock,
                product_model.price,
            )
    
    async def search_products(self, filters: ProductSearchFilters) -> tuple[list[Product], int]:
        async with SessionLocal() as session:
            query = select(ProductModel)
            conditions: list[ColumnElement[bool]] = []
            if filters.name is not None:
                conditions.append(ProductModel.name.ilike(f"%{filters.name}%"))
            if filters.min_price is not None:
                conditions.append(ProductModel.price >= filters.min_price)
            if filters.max_price is not None:
                conditions.append(ProductModel.price <= filters.max_price)
            if conditions:
                query = query.where(*conditions)
            result = await session.execute(query)
            count_products = await session.execute(
                select(func.count()).select_from(query.subquery())
            )
            product_models = result.scalars().all()
            count = count_products.scalar_one()
            products = [
                Product(
                    id=product_model.id,
                    name=product_model.name,
                    stock=product_model.stock,
                    price=product_model.price,
                )
                for product_model in product_models
            ]
            return products, count
            


    async def create_product(self, product: Product) -> Product:
        async with SessionLocal() as session:
            product_model = ProductModel(
                name=product.name,
                stock=product.stock,
                price=product.price,
            )
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return Product(
                id=product_model.id,
                name=product_model.name,
                stock=product_model.stock,
                price=product_model.price,
            )
        
    async def delete_product(self, product_id: int) -> Optional[Product]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product_model = result.scalar_one_or_none()
            if not product_model:
                return None
            await session.delete(product_model)
            await session.commit()
            return Product(
                id=product_model.id,
                name=product_model.name,
                stock=product_model.stock,
                price=product_model.price,
            )
        
    async def purchase_product(self, product_id: int, quantity: int):
        async with SessionLocal() as session:
            stmt = (
                update(ProductModel)
                .where(ProductModel.id == product_id)
                .where(ProductModel.stock >= quantity)
                .values(stock=ProductModel.stock - quantity)
                .returning(ProductModel)
            )

            result = await session.execute(stmt)
            updated_product_model = result.scalar_one_or_none()
            if not updated_product_model:
                # This means either the product was not found or there was insufficient stock
                return None
            await session.commit()

            return Product(
                id=updated_product_model.id,
                name=updated_product_model.name,
                stock=updated_product_model.stock,
                price=updated_product_model.price,
            )
        
    async def increase_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        async with SessionLocal() as session:
            stmt = (
                update(ProductModel)
                .where(ProductModel.id == product_id)
                .values(stock=ProductModel.stock + quantity)
                .returning(ProductModel)
            )

            result = await session.execute(stmt)
            updated_product_model = result.scalar_one_or_none()
            if not updated_product_model:
                # This means the product was not found
                return None
            await session.commit()

            return Product(
                id=updated_product_model.id,
                name=updated_product_model.name,
                stock=updated_product_model.stock,
                price=updated_product_model.price,
            )

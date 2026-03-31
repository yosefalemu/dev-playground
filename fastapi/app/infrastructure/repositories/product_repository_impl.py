from sqlalchemy import select
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.models import ProductModel
from app.core.database import SessionLocal


class ProductRepositoryImpl(ProductRepository):
    async def get_products(self):
        async with SessionLocal() as session:
            result = await session.execute(select(ProductModel))
            product_models = result.scalars().all()
            return [
                Product(
                    id=product_model.id,
                    name=product_model.name,
                    stock=product_model.stock,
                    price=product_model.price,
                )
                for product_model in product_models
            ]
            

    async def get_product_by_id(self, product_id):
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
        

    async def get_product_by_name(self, name):
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
        

    async def create_product(self, product):
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
        
    async def delete_product(self, product_id):
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

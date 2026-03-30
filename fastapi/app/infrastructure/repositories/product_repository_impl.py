from sqlalchemy import select
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.models import ProductModel
from app.core.database import SessionLocal

class ProductRepositoryImpl(ProductRepository):
    async def get_product_by_id(self, product_id):
        async with SessionLocal() as session:
            result = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
            product_model = result.scalar_one_or_none()
            if not product_model:
                return None
            return Product(
                product_model.id,
                product_model.name,
                product_model.stock,
                product_model.price
            )
    async def save_product(self, product):
        async with SessionLocal() as session:
            product_model = ProductModel(
                id=product.id,
                name=product.name,
                stock=product.stock,
                price=product.price
            )
            session.add(product_model)
            await session.commit()
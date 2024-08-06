import uuid
from datetime import datetime

import asyncpg

from project.config import DATABASE_URL


async def get_db_connection():
    return await asyncpg.connect(dsn=DATABASE_URL)


async def insert_product(sku_item):
    conn = await get_db_connection()

    columns = [
        "uuid",
        "product_id",
        "title",
        "description",
        "brand",
        "first_image_url",
        "category_id",
        "category_lvl_1",
        "category_lvl_2",
        "category_lvl_3",
        "category_remaining",
        "price_before_discounts",
        "discount",
        "price_after_discounts",
        "inserted_at",
        "updated_at",
        "currency",
        "barcode",
        "similar_sku",
    ]

    sku_data = {col: sku_item.get(col, None) for col in columns}
    now = datetime.now()
    if not sku_data.get("uuid"):
        sku_data["uuid"] = str(uuid.uuid4())
    if not sku_data.get("inserted_at"):
        sku_data["inserted_at"] = now
    if not sku_data.get("updated_at"):
        sku_data["updated_at"] = now

    sku_data["product_id"] = int(sku_data.get("product_id", 0))
    sku_data["category_id"] = int(sku_data.get("category_id", 0))
    sku_data["price_before_discounts"] = float(sku_data.get("price_before_discounts", 0.0))
    sku_data["discount"] = float(sku_data.get("discount", 0.0))
    sku_data["price_after_discounts"] = float(sku_data.get("price_after_discounts", 0.0))
    sku_data["barcode"] = float(sku_data.get("barcode", 0))

    columns_str = ", ".join(columns)
    placeholders_str = ", ".join([f"${i + 1}" for i in range(len(columns))])
    insert_statement = f"""
        INSERT INTO sku ({columns_str})
        VALUES ({placeholders_str})
        RETURNING *;
    """

    values = [sku_data.get(col) for col in columns]
    try:
        inserted_product = dict(await conn.fetchrow(insert_statement, *values))
        inserted_product["uuid"] = str(inserted_product.get("uuid"))
        await conn.close()
        return inserted_product
    except Exception as e:
        print(str(e))
    finally:
        await conn.close()


async def update_similar_sku_column(sku_uuid, similar_sku_list: list):
    conn = await get_db_connection()

    update_statement = """
        UPDATE sku
        SET similar_sku = $1
        WHERE uuid = $2
    """

    try:
        await conn.execute(update_statement, similar_sku_list, uuid.UUID(sku_uuid))
    except Exception as e:
        print(str(e))
    finally:
        await conn.close()


async def get_products():
    conn = await get_db_connection()

    select_statement = """
        SELECT uuid, product_id, title, description FROM sku
    """

    try:
        products = await conn.fetch(select_statement)
        return [dict(product) for product in products]
    except Exception as e:
        print(str(e))
        return []
    finally:
        await conn.close()

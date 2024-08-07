import uuid
from datetime import datetime

import asyncpg

from project.config import DATABASE_URL


async def get_db_connection():
    return await asyncpg.connect(dsn=DATABASE_URL)


async def insert_products_batch(sku_items):
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

    now = datetime.now()
    values_list = []
    int64_limit = 2**63

    for sku_item in sku_items:
        sku_data = {col: sku_item.get(col, None) for col in columns}
        product_id = int(sku_data.get("product_id", 0))
        sku_data["uuid"] = str(uuid.uuid4())
        sku_data["inserted_at"] = sku_data.get("inserted_at", now)
        sku_data["updated_at"] = sku_data.get("updated_at", now)

        sku_data["product_id"] = product_id if -int64_limit < product_id < int64_limit - 1 else 0

        sku_data["category_id"] = int(sku_data.get("category_id", 0))
        sku_data["price_before_discounts"] = float(sku_data.get("price_before_discounts", 0.0))
        sku_data["discount"] = float(sku_data.get("discount", 0.0))
        sku_data["price_after_discounts"] = float(sku_data.get("price_after_discounts", 0.0))
        sku_data["barcode"] = float(sku_data.get("barcode", 0))

        values_list.append([sku_data.get(col) for col in columns])

    placeholders = ", ".join(
        [
            f"({', '.join(['$' + str(i + j * len(columns) + 1) for i in range(len(columns))])})"
            for j in range(len(values_list))
        ]
    )
    values_flat = [val for sublist in values_list for val in sublist]

    insert_statement = f"""
        INSERT INTO sku ({', '.join(columns)})
        VALUES {placeholders}
        RETURNING *;
    """

    try:
        inserted_products = await conn.fetch(insert_statement, *values_flat)
        results = [dict(product) for product in inserted_products]
        return results
    except Exception as e:
        print(str(e))
        return None
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

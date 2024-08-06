import psycopg2

from project.config import DB_PORT, DB_HOST, DB_PASS, DB_USER, DB_NAME

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS public.sku (
    uuid UUID PRIMARY KEY,
    marketplace_id INTEGER,
    product_id BIGINT,
    title TEXT,
    description TEXT,
    brand TEXT,
    seller_id INTEGER,
    seller_name TEXT,
    first_image_url TEXT,
    category_id INTEGER,
    category_lvl_1 TEXT,
    category_lvl_2 TEXT,
    category_lvl_3 TEXT,
    category_remaining TEXT,
    features JSON,
    rating_count INTEGER,
    rating_value DOUBLE PRECISION,
    price_before_discounts REAL,
    discount DOUBLE PRECISION,
    price_after_discounts REAL,
    bonuses INTEGER,
    sales INTEGER,
    inserted_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    currency TEXT,
    barcode BIGINT,
    similar_sku UUID[]
);
"""

cur.execute(create_table_query)

comments = [
    ("uuid", "id товара в нашей бд"),
    ("marketplace_id", "id маркетплейса"),
    ("product_id", "id товара в маркетплейсе"),
    ("title", "название товара"),
    ("description", "описание товара"),
    ("category_lvl_1", "Первая часть категории товара."),
    ("category_lvl_2", "Вторая часть категории товара."),
    ("category_lvl_3", "Третья часть категории товара."),
    ("category_remaining", "Остаток категории товара."),
    ("features", "Характеристики товара"),
    ("rating_count", "Кол-во отзывов о товаре"),
    ("rating_value", "Рейтинг товара (0-5)"),
    ("barcode", "Штрихкод")
]

for column, comment in comments:
    cur.execute(f"COMMENT ON COLUMN public.sku.{column} IS '{comment}';")

create_index_queries = [
    "CREATE INDEX IF NOT EXISTS sku_brand_index ON public.sku (brand);",
    "CREATE UNIQUE INDEX IF NOT EXISTS sku_marketplace_id_sku_id_uindex ON public.sku (marketplace_id, product_id);",
    "CREATE UNIQUE INDEX IF NOT EXISTS sku_uuid_uindex ON public.sku (uuid);"
]

for index_query in create_index_queries:
    cur.execute(index_query)

conn.commit()
cur.close()
conn.close()

print('Postgres migrations were carried out successfully!')

import typesense

from project.config import (
    TYPESENSE_API_KEY,
    TYPESENSE_CONNECTION_TIMEOUT_SECONDS,
    TYPESENSE_HOST,
    TYPESENSE_PORT,
    TYPESENSE_PROTOCOL,
)


def create_client():
    client = typesense.Client(
        {
            "nodes": [
                {
                    "host": TYPESENSE_HOST,
                    "port": TYPESENSE_PORT,
                    "protocol": TYPESENSE_PROTOCOL,
                }
            ],
            "api_key": TYPESENSE_API_KEY,
            "connection_timeout_seconds": TYPESENSE_CONNECTION_TIMEOUT_SECONDS,
        }
    )
    return client


async def insert_data_into_typesense(sku_data: dict):
    client = create_client()

    async def insert_document(document):
        try:
            client.collections["products"].documents.create(document)
        except Exception as ex:
            print(str(ex))

    try:
        sku_data = {
            "uuid": str(sku_data.get("uuid")),
            "product_id": str(sku_data.get("product_id")),
            "title": str(sku_data.get("title")),
            "description": str(sku_data.get("description")),
            "discount": float(sku_data.get("discount", 0.0)),
            "price_before_discounts": float(sku_data.get("price_before_discounts", 0.0)),
            "category_remaining": str(sku_data.get("category_remaining")),
            "barcode": str(sku_data.get("barcode")),
        }
    except Exception as e:
        print(str(e))
    await insert_document(sku_data)


async def search_in_typesense(title):
    client = create_client()

    search_parameters = {
        "q": title,
        "query_by": "title,description",
        "prefix": True,
        "fuzzy": True,
    }

    results = client.collections["products"].documents.search(search_parameters)
    return results["hits"]

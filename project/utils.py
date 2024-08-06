import io

from lxml import etree

from project.postgres_utils import get_products, insert_product, update_similar_sku_column
from project.typesense_utils import insert_data_into_typesense, search_in_typesense


async def is_xml(file):
    try:
        file_stream = io.BytesIO(await file.read())
        etree.iterparse(file_stream, events=("start", "end"))
        return True
    except Exception as e:
        print(str(e))
        return False


def get_full_path(category_id, categories_dict):
    path = []
    current_id = category_id
    while current_id is not None and current_id in categories_dict:
        category = categories_dict[current_id]
        path.insert(0, category["name"])
        current_id = category["parentId"]
    return path


async def parse_xml(file_path: str = None, file=None):
    categories_dict = {}

    if file_path:
        context = etree.iterparse(file_path, events=("start", "end"))
    elif file:
        file_content = await file.read()
        if not file_content:
            raise ValueError("The file has no content")
        file_stream = io.BytesIO(file_content)

        context = etree.iterparse(file_stream, events=("start", "end"))
    else:
        raise ValueError(
            "TypeError: parse_xml_insert_into_typesense() missing "
            '1 required positional argument: "file" or "file_path"'
        )

    for event, element in context:
        if event == "start":
            if element.tag == "category":
                cat_id = element.get("id")
                parent_id = element.get("parentId")
                name = element.text
                categories_dict[cat_id] = {"name": name, "parentId": parent_id}
        elif event == "end":
            if element.tag == "offer":
                offer_data = {
                    "product_id": element.get("id", default=""),
                    "available": element.get("available", default=True),
                    "barcode": element.findtext("barcode", default=0),
                    "category_id": element.findtext("categoryId", default=None),
                    "description": element.findtext("description", default="").strip(),
                    "title": element.findtext("name", default=""),
                    "brand": element.findtext("vendor", default=None),
                    "price_before_discounts": element.findtext("price", default=0),
                    "currency": element.findtext("currencyId", default="RUB"),
                    "marketplace_id": element.get("marketplace_id", None),
                    "first_image_url": element.findtext("picture", default=None),
                    "rating_count": element.findtext("rating_count", default=None),
                    "rating_value": element.findtext("rating_value", default=None),
                    "discount": element.findtext("discount", default=0),
                    "bonuses": element.findtext("bonuses", default=None),
                    "sales": element.findtext("sales", default=None),
                    "similar_sku": element.findtext("similar_sku", default=[]),
                }

                category_id = offer_data["category_id"]
                if category_id in categories_dict:
                    category_path = get_full_path(category_id, categories_dict)
                    category_lvl_1 = category_path[0] if len(category_path) > 0 else None
                    category_lvl_2 = category_path[1] if len(category_path) > 1 else None
                    category_lvl_3 = category_path[2] if len(category_path) > 2 else None
                    category_path_str = " / ".join(category_path)
                else:
                    category_lvl_1 = category_lvl_2 = category_lvl_3 = category_path_str = "N/A"

                offer_data.update(
                    {
                        "category_lvl_1": category_lvl_1,
                        "category_lvl_2": category_lvl_2,
                        "category_lvl_3": category_lvl_3,
                        "category_remaining": category_path_str,
                        "price_after_discounts": (1 - offer_data.get("discount"))
                        * element.findtext("price", default=0),
                    }
                )

                element.clear()

                inserted_product = await insert_product(offer_data)
                await insert_data_into_typesense(inserted_product)

    del context


async def conduct_matching():
    products = await get_products()

    for product in products:
        product_uuid = str(product.get("uuid"))
        similar_sku = [
            str(sku.get("document").get("uuid"))
            for sku in await search_in_typesense(product.get("title"))
            if product_uuid != str(sku.get("document").get("uuid"))
        ]
        if similar_sku:
            await update_similar_sku_column(str(product.get("uuid")), similar_sku_list=similar_sku)

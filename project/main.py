from lxml import etree


def parse_large_xml(file_path):
    context = etree.iterparse(file_path, events=("start", "end"))
    for event, element in context:
        if event == "start":
            if element.tag == "yml_catalog":
                print(f"Catalog Date: {element.get('date')}")
            elif element.tag == "shop":
                print("Shop found")
            elif element.tag == "name":
                print(f"Shop Name: {element.text}")
            elif element.tag == "company":
                print(f"Company: {element.text}")
            elif element.tag == "url":
                print(f"URL: {element.text}")
        elif event == "end":
            if element.tag == "offer":
                offer_id = element.get("id")
                available = element.get("available")

                barcode_elem = element.find("barcode")
                barcode = (
                    barcode_elem.text if barcode_elem is not None else "N/A"
                )

                category_id_elem = element.find("categoryId")
                category_id = (
                    category_id_elem.text
                    if category_id_elem is not None
                    else "N/A"
                )

                currency_id_elem = element.find("currencyId")
                currency_id = (
                    currency_id_elem.text
                    if currency_id_elem is not None
                    else "N/A"
                )

                description_elem = element.find("description")
                if (
                    description_elem is not None
                    and description_elem.text is not None
                ):
                    description = description_elem.text.strip()
                else:
                    description = "N/A"

                print(
                    f"Offer ID: {offer_id}, Available: {available}, Barcode: {barcode}"
                )
                print(
                    f"Category ID: {category_id}, Currency ID: {currency_id}"
                )
                print(f"Description: {description}")

                element.clear()

    del context


if __name__ == "__main__":
    parse_large_xml("elektronika_products_20240801_145140.xml")

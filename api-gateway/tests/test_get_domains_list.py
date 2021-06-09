import json
from typing import Optional, Any, List
from lxml import html
import requests
from requests import Response

URL = ""

if __name__ == "__main__":
    page: Response = requests.get(URL)
    tree: Optional[Any] = html.fromstring(page.content)
    els: List[Any] = tree.xpath(
        '//*[contains(concat( " ", @class, " " ), concat( " ", "table-hover", " " ))]//div//a/text()'
    )
    zones: List[str] = [zone.replace(" domains", "").strip() for zone in els]
    with open("../static/zones.json", "w", encoding="utf-8") as file:
        json.dump(zones, file, ensure_ascii=False, indent=4)

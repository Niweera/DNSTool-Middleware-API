import json
from typing import Optional, Any, List
from lxml import html
import requests
from requests import Response
from os.path import abspath, join, dirname, realpath

URL = ""

if __name__ == "__main__":
    page: Response = requests.get(URL)
    tree: Optional[Any] = html.fromstring(page.content)
    els: List[Any] = tree.xpath(
        '//*[contains(concat( " ", @class, " " ), concat( " ", "table-hover", " " ))]//div//a/text()'
    )
    zones: List[str] = [zone.replace(" domains", "").strip() for zone in els]
    zones_json_file: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "zones.json")
    )
    with open(zones_json_file, "w", encoding="utf-8") as file:
        json.dump(zones, file, ensure_ascii=False, indent=4)

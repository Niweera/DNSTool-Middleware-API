import json
import re
from os.path import abspath, join, dirname, realpath
from typing import List

if __name__ == "__main__":
    email_domains_txt: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "email-domains.txt")
    )
    black_list_json: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "blacklist-domains.json")
    )
    white_list_json: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "whitelist-domains.json")
    )
    with open(file=email_domains_txt, mode="r", encoding="utf-8") as email_domains_file:
        domains: List[str] = [
            domain.rstrip() for domain in email_domains_file.readlines()
        ]
        black_list: List[str] = [
            entry.lstrip("-").lower() for entry in domains if re.search("^-", entry)
        ]
        white_list: List[str] = [
            entry.lower() for entry in domains if not re.search("^-", entry)
        ]
        with open(black_list_json, "w", encoding="utf-8") as bl_file:
            json.dump(black_list, bl_file, ensure_ascii=False, indent=4)
        with open(white_list_json, "w", encoding="utf-8") as wl_file:
            json.dump(white_list, wl_file, ensure_ascii=False, indent=4)

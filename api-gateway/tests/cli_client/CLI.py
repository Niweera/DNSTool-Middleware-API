import json
from os.path import abspath, join, dirname, realpath


class CLI:
    def __init__(self):
        service_account_file: str = abspath(
            join(dirname(realpath(__file__)), "service_account_1625850846648708.json")
        )
        with open(
            file=service_account_file, mode="r", encoding="utf-8"
        ) as service_account_json:
            service_account = json.load(service_account_json)
            print(service_account)

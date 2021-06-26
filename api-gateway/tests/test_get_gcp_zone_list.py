import json
from os.path import abspath, join, dirname, realpath
from typing import List
import pandas
from pandas import DataFrame

if __name__ == "__main__":
    zone_file: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "gcp-regions-zones.txt")
    )
    df: DataFrame = pandas.read_csv(zone_file, sep=" ")
    zones: List[str] = df["NAME"].to_list()
    zones_json_file: str = abspath(
        join(dirname(dirname(realpath(__file__))), "static", "gcp-zones.json")
    )
    with open(zones_json_file, "w", encoding="utf-8") as file:
        json.dump(zones, file, ensure_ascii=False, indent=4)

from hashlib import sha256
from typing import List, Dict


def hash_data(*args) -> str:
    concatenated = "".join(args)
    return sha256(concatenated.encode("utf-8")).hexdigest()


def sort_data_by_names(data: List) -> List:
    return sorted(data, key=lambda x: (x["second_name"], x["first_name"]))


def append_hash(item: Dict) -> Dict:
    item["hash"] = hash_data(
        item["first_name"], item["second_name"], item["birth_date"]
    )
    return item


def process_data(data: List) -> List:
    """
    Sorts provided data by 'second_name' and 'first_name'
    and appends hash value to each item in 'data'.
    """
    sorted_data = sort_data_by_names(data)
    return [append_hash(item) for item in sorted_data]

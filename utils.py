import json


def read_json(json_file):
    with open(json_file, "r", encoding="utf-8") as fp:
        return json.load(fp)


def write_to_file(data: dict, file_path: str):
    with open(file_path, "w", encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False)

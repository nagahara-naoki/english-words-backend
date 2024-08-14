# app/utils.py
import json


def save_to_file(data, filename):
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

import json

def load_json(file_path, encoding='utf-8'):
    """Loads a JSON file and returns its content."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(file_path, data, encoding='utf-8'):
    """Saves data to a JSON file."""
    with open(file_path, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
import json

def load_json(file_path, encoding='utf-8-sig'):
    """Loads a JSON file and returns its content."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON in {file_path}:\n{e}")
        return None

def save_json(file_path, data, encoding='utf-8'):
    """Saves data to a JSON file."""
    with open(file_path, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
from utils.file_handler import load_json
from config import I18N_DIR
import os

class Localization:
    """Manages language strings for the application."""
    def __init__(self, language='en'):
        self.language = language
        self.strings = self._load_strings()

    def _load_strings(self):
        """Loads the language file corresponding to the selected language."""
        lang_file = os.path.join(I18N_DIR, f"{self.language}.json")
        strings = load_json(lang_file)
        if strings is None:
            print(f"Warning: Language file for '{self.language}' not found. Falling back to 'en'.")
            self.language = 'en'
            lang_file = os.path.join(I18N_DIR, "en.json")
            strings = load_json(lang_file)
        return strings

    def get(self, key, **kwargs):
        """Gets a string by key and formats it with provided arguments."""
        return self.strings.get(key, key).format(**kwargs)
import json
from pathlib import Path


class FavoritesManager:
    def __init__(self, filename):
        self.filename = Path(filename)
        self._favorites = self._load()

    def _load(self):
        try:
            with self.filename.open(encoding="utf-8") as favorites_file:
                favorites = json.load(favorites_file)
        except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
            return {}

        if not isinstance(favorites, dict) or not all(
            isinstance(name, str) and isinstance(location, str)
            for name, location in favorites.items()
        ):
            return {}
        return favorites

    def _save(self):
        with self.filename.open("w", encoding="utf-8") as favorites_file:
            json.dump(self._favorites, favorites_file, indent=2)

    def add(self, name, location):
        if any(saved_name.casefold() == name.casefold() for saved_name in self._favorites):
            return False

        self._favorites[name] = location
        self._save()
        return True

    def remove(self, name):
        matching_names = [
            saved_name
            for saved_name in self._favorites
            if saved_name.casefold() == name.casefold()
        ]
        if not matching_names:
            return False

        for saved_name in matching_names:
            del self._favorites[saved_name]
        self._save()
        return True

    def list_all(self):
        return self._favorites.copy()

    def get_location(self, name):
        for saved_name, location in self._favorites.items():
            if saved_name.casefold() == name.casefold():
                return location
        return None
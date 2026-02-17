import os
import json
from datetime import datetime
from core.helper.helper import join_path


class ArchiveManager:

    def __init__(self):
        self.file_path = join_path(
            ["default", "data", "saved_archives.json"],
            True
        )
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"loaded_archives": []}, f, indent=4)

    def load_archives(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_archives(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_archive(self, path, custom_name=None):
        data = self.load_archives()
        archives = data["loaded_archives"]

        # Evita duplicado
        for archive in archives:
            if archive["path"] == path:
                archive["last_open"] = datetime.now().strftime("%d/%m/%Y")
                if custom_name:
                    archive["custom_name"] = custom_name
                self.save_archives(data)
                return

        name = os.path.basename(path)
        ext = name.split(".")[-1]

        archives.append({
            "path": path,
            "name": name,
            "custom_name": custom_name or name,
            "pinned": False,
            "last_open": datetime.now().strftime("%d/%m/%Y"),
            "type": ext
        })

        self.save_archives(data)

    def remove_archive(self, path):
        data = self.load_archives()
        data["loaded_archives"] = [
            archive for archive in data["loaded_archives"]
            if archive["path"] != path
        ]
        self.save_archives(data)

    def toggle_pin(self, path):
        data = self.load_archives()
        for archive in data["loaded_archives"]:
            if archive["path"] == path:
                archive["pinned"] = not archive["pinned"]
        self.save_archives(data)

    def update_custom_name(self, path, custom_name):
        """Atualiza o nome personalizado de um arquivo já salvo."""
        data = self.load_archives()
        for archive in data["loaded_archives"]:
            if archive["path"] == path:
                archive["custom_name"] = custom_name
        self.save_archives(data)

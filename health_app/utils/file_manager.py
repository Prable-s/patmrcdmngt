import json
import os
from datetime import datetime


class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.write_data([])

    def read_data(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def write_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4, default=self.datetime_converter)

    def datetime_converter(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

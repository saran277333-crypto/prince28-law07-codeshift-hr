import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class RecordStore:
    def __init__(self, data_file: Path):
        self.data_file = data_file
        self.records = []

    def load_records(self):
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                self.records = json.load(file)

            logger.info("records loaded", extra={"records": len(self.records)})

        except FileNotFoundError:
            self.records = []
            logger.error("Records file not found: %s", self.data_file)

        except json.JSONDecodeError:
            self.records = []
            logger.error("Invalid JSON in records file: %s", self.data_file)

    def get_all(self):
        return self.records

    def get_by_id(self, record_id: str):
        for record in self.records:
            if record.get("id") == record_id:
                return record

        return None

"""One strict, working-directory-independent loader for the CSV knowledge base."""
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


class KnowledgeDataError(ValueError):
    """Malformed knowledge data; not a learner input error."""


def load_csv(relative_path):
    path = (DATA_DIR / relative_path).resolve()
    if DATA_DIR.resolve() not in path.parents:
        raise KnowledgeDataError("CSV path must remain inside the knowledge data directory.")
    if not path.is_file():
        raise FileNotFoundError(f"WiseLanka data file not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        if not fields or any(not field or not field.strip() for field in fields):
            raise KnowledgeDataError(f"Missing CSV header: {relative_path}")
        if len(fields) != len(set(fields)):
            raise KnowledgeDataError(f"Duplicate CSV columns: {relative_path}")
        rows = []
        for number, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise KnowledgeDataError(f"Invalid CSV row width: {relative_path}:{number}")
            rows.append(dict(row))
        return rows

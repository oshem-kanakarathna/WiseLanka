import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_csv(relative_path):
    """
    Load a CSV file from the WiseLanka data directory.

    Example:
        load_csv("reference/programmes.csv")
    """

    file_path = DATA_DIR / relative_path

    if not file_path.exists():
        raise FileNotFoundError(
            f"WiseLanka data file not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)
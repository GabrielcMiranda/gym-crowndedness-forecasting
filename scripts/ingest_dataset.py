import csv
import hashlib
import io
import os
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ARCHIVE_URL = "https://www.kaggle.com/api/v1/datasets/download/nsrose7224/crowdedness-at-the-campus-gym"
CSV_MEMBER_NAME = "data.csv"
EXPECTED_SHA256 = "490412204d0d90c58036788adaaba1a16968dfab525fad3fefe78a18bc998ff4"
EXPECTED_SIZE_BYTES = 3_447_605
EXPECTED_ROW_COUNT = 62_184
EXPECTED_COLUMNS = [
    "number_people",
    "date",
    "timestamp",
    "day_of_week",
    "is_weekend",
    "is_holiday",
    "temperature",
    "is_start_of_semester",
    "is_during_semester",
    "month",
    "hour",
]
DOWNLOAD_TIMEOUT_SECONDS = 120
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / CSV_MEMBER_NAME


class DatasetIntegrityError(Exception):
    pass


def validate_csv_content(content: bytes) -> None:
    rows = csv.reader(io.StringIO(content.decode("utf-8"), newline=""))
    columns = next(rows, [])
    if columns != EXPECTED_COLUMNS:
        raise DatasetIntegrityError(f"Colunas inesperadas: {columns}")
    row_count = sum(1 for _ in rows)
    if row_count != EXPECTED_ROW_COUNT:
        raise DatasetIntegrityError(f"Esperadas {EXPECTED_ROW_COUNT} linhas, encontradas {row_count}")
    content_hash = hashlib.sha256(content).hexdigest()
    if content_hash != EXPECTED_SHA256:
        raise DatasetIntegrityError(f"SHA-256 divergente: {content_hash}")


def is_valid_csv_file(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        validate_csv_content(path.read_bytes())
    except (DatasetIntegrityError, UnicodeDecodeError):
        return False
    return True


def download_archive(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "dataset-ingest"})
    with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
        return response.read()


def extract_csv_member(archive_content: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(archive_content)) as archive:
        try:
            member = archive.getinfo(CSV_MEMBER_NAME)
        except KeyError as error:
            raise DatasetIntegrityError(f"{CSV_MEMBER_NAME} ausente no arquivo baixado") from error
        if member.file_size != EXPECTED_SIZE_BYTES:
            raise DatasetIntegrityError(f"Tamanho inesperado de {CSV_MEMBER_NAME}: {member.file_size} bytes")
        return archive.read(member)


def write_atomically(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_bytes(content)
    os.replace(temporary_path, path)


def ingest_dataset(output_path: Path = OUTPUT_PATH) -> bool:
    if is_valid_csv_file(output_path):
        return False
    csv_content = extract_csv_member(download_archive(ARCHIVE_URL))
    validate_csv_content(csv_content)
    write_atomically(output_path, csv_content)
    return True


def main() -> int:
    try:
        was_downloaded = ingest_dataset()
    except (DatasetIntegrityError, UnicodeDecodeError, zipfile.BadZipFile) as error:
        print(f"Dataset rejeitado: {error}", file=sys.stderr)
        return 1
    except urllib.error.URLError as error:
        print(f"Falha no download: {error}", file=sys.stderr)
        return 1
    status = "baixado e validado" if was_downloaded else "já estava válido, download ignorado"
    print(f"{OUTPUT_PATH}: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

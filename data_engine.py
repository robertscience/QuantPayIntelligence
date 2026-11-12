from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile

import pandas as pd


MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 100
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}


def load_financial_file(file_obj, filename):
    """Carga y valida un archivo financiero CSV o Excel."""
    if not filename or Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato no admitido. Utiliza CSV o XLSX.")

    content = file_obj.read(MAX_FILE_BYTES + 1)
    if not content:
        raise ValueError("El archivo está vacío.")
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("El archivo supera el límite de 10 MB.")

    try:
        if Path(filename).suffix.lower() == ".csv":
            data = pd.read_csv(BytesIO(content), encoding="utf-8-sig")
        else:
            data = pd.read_excel(BytesIO(content), engine="openpyxl")
    except (ValueError, UnicodeError, OSError, BadZipFile) as exc:
        raise ValueError("No se pudo leer el archivo. Revisa su formato.") from exc

    if data.empty:
        raise ValueError("El archivo no contiene registros.")
    if len(data) > MAX_ROWS or len(data.columns) > MAX_COLUMNS:
        raise ValueError("El archivo supera los límites de filas o columnas.")

    data.columns = [str(column).strip() for column in data.columns]

    if any(not column for column in data.columns):
        raise ValueError("Todas las columnas deben tener un nombre.")
    if not data.columns.is_unique:
        raise ValueError("El archivo contiene nombres de columnas duplicados.")

    return data

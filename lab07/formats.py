import json


def csv_to_records(text: str) -> list[dict]:
    """Разбирает CSV с заголовком в список словарей."""
    if not text or not text.strip():
        return []

    lines = text.splitlines()
    if not lines:
        return []

    headers = [h.strip() for h in lines[0].split(",")]
    result = []

    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(",")]
        record = dict(zip(headers, values))
        result.append(record)

    return result


def parse_settings(lines: list[str]) -> dict:
    """Разбирает простой YAML-подобный текст в словарь."""
    result = {}
    current_list_key = None

    def convert_type(val: str):
        low_val = val.lower()
        if low_val in ("true", "yes"):
            return True
        if low_val in ("false", "no"):
            return False
        try:
            num_val = val.replace(",", ".")
            if "." in num_val:
                return float(num_val)
            return int(num_val)
        except ValueError:
            return val

    for line in lines:
        clean_line = line.split("#")[0].strip()
        if not clean_line:
            continue

        if clean_line.startswith("- "):
            if current_list_key is not None:
                item_value = clean_line[2:].strip()
                result[current_list_key].append(convert_type(item_value))
        elif ":" in clean_line:
            key, value = clean_line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if not value:
                current_list_key = key
                result[key] = []
            else:
                current_list_key = None
                result[key] = convert_type(value)

    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из extra по ключу. Поля самой записи важнее."""
    for row in rows:
        row_id = row.get(key)
        if row_id in extra:
            for k, v in extra[row_id].items():
                if k not in row:
                    row[k] = v
    return rows


def records_to_json(records: list[dict]) -> str:
    """Преобразует список словарей в красивый JSON-строку."""
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)
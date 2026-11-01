def parse_record(line: str) -> dict:
    if not isinstance(line, str):
        raise ValueError("Строка должна быть строкой")
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Неверный формат строки")
    city, temp_str, date = parts
    if not city.strip() or not date.strip():
        raise ValueError("Город или дата пусты")
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError(f"Температура не число: {temp_str}")
    return {"city": city.strip(), "temperature": temp, "date": date.strip()}

def read_valid(lines: list) -> list:
    records = []
    for line in lines:
        if not line or not line.strip():
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            continue
    return records

def average_by_city(records: list) -> dict:
    totals, counts = {}, {}
    for rec in records:
        c, t = rec["city"], rec["temperature"]
        totals[c] = totals.get(c, 0) + t
        counts[c] = counts.get(c, 0) + 1
    return {c: round(totals[c] / counts[c], 1) for c in totals}

def warmest_city(records: list) -> str:
    averages = average_by_city(records)
    if not averages:
        return ""
    sorted_cities = sorted(averages.items(), key=lambda item: (-item[1], item[0]))
    return sorted_cities[0][0]
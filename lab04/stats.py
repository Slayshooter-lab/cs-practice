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
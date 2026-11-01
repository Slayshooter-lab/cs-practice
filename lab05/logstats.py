def parse_event(line: str) -> dict:
    """Разбирает строку лога в словарь."""
    if not line or not line.strip():
        raise ValueError("Пустая строка")

    parts = line.split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError("Неверный формат строки: меньше трех частей")

    time, level, message = parts
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
        raise ValueError("Неизвестный уровень логирования")

    return {"time": time, "level": level, "message": message.strip()}


def count_levels(lines) -> dict:
    """Считает количество строк каждого уровня."""
    counts = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "BROKEN": 0}
    for line in lines:
        try:
            event = parse_event(line)
            counts[event["level"]] += 1
        except ValueError:
            counts["BROKEN"] += 1
    return counts


def top_errors(lines, n: int) -> list:
    """Возвращает топ-n частых сообщений уровня ERROR."""
    error_counts = {}
    for line in lines:
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            continue

    # Сортируем по количеству (убывание), при равенстве — по алфавиту
    sorted_errors = sorted(error_counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_errors[:n]


def format_report(counts: dict, errors: list) -> str:
    """Формирует текстовый отчет."""
    lines = ["Отчёт по журналу", ""]

    # Уровни по алфавиту
    for level in sorted(counts.keys()):
        lines.append(f"{level}: {counts[level]}")

    lines.append("")
    lines.append("Частые ошибки:")

    for msg, count in errors:
        lines.append(f"- {msg} — {count}")

    return "\n".join(lines) + "\n"
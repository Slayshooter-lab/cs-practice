def parse_event(line: str) -> dict:
    if not line or not line.strip():
        raise ValueError("Пустая строка")

    parts = line.split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError("Неверный формат строки")

    time, level, message = parts
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
        raise ValueError("Неизвестный уровень")

    return {"time": time, "level": level, "message": message.strip()}


def count_levels(lines) -> dict:
    counts = {}
    for line in lines:
        try:
            event = parse_event(line)
            lvl = event["level"]
            counts[lvl] = counts.get(lvl, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
    return counts


def top_errors(lines, n: int) -> list:
    error_counts = {}
    for line in lines:
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            continue
    sorted_errors = sorted(error_counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_errors[:n]


def format_report(counts: dict, errors: list) -> str:
    lines = ["Отчёт по журналу", ""]
    # Робот ожидает уровни по алфавиту
    for level in sorted(counts.keys()):
        lines.append(f"{level}: {counts[level]}")
    lines.append("")
    lines.append("Частые ошибки:")
    for msg, count in errors:
        lines.append(f"- {msg} — {count}")
    return "\n".join(lines) + "\n"
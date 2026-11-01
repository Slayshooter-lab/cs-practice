import sys
from logstats import count_levels, top_errors, format_report


def main():
    # Читаем имя файла из ввода, убираем кавычки и пробелы
    filepath = sys.stdin.readline().strip().strip('"').strip("'")

    counts = {}
    error_counts = {}

    # Открываем файл и читаем ПОСТРОЧНО
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            try:
                from logstats import parse_event
                event = parse_event(line)
                lvl = event["level"]
                counts[lvl] = counts.get(lvl, 0) + 1

                if lvl == "ERROR":
                    msg = event["message"]
                    error_counts[msg] = error_counts.get(msg, 0) + 1
            except ValueError:
                counts["BROKEN"] = counts.get("BROKEN", 0) + 1

    # Сортируем ошибки для отчета
    sorted_errors = sorted(error_counts.items(), key=lambda x: (-x[1], x[0]))[:3]

    total = sum(counts.values())
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)

    print(total)
    print(error_count)
    print(broken_count)

    report_text = format_report(counts, sorted_errors)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)


if __name__ == "__main__":
    main()
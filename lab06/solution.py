def count_by_extension(paths: list) -> dict:
    """Считает количество файлов для каждого расширения (в нижнем регистре, без точки)."""
    counts = {}
    for path in paths:
        # Берем имя файла (на случай, если в пути есть папки)
        filename = path.split("/")[-1]

        # Если в имени есть точка, берем то, что после последней
        if "." in filename:
            ext = filename.split(".")[-1].lower()
        else:
            ext = ""  # Если точки нет (например, Makefile)

        counts[ext] = counts.get(ext, 0) + 1
    return counts


def deepest_path(paths: list) -> str:
    """Возвращает путь с наибольшей вложенностью (по количеству '/')."""
    if not paths:
        return ""

    # Считаем вложенность: количество разделителей '/'
    # При равенстве сортируем по алфавиту
    best_path = sorted(paths, key=lambda p: (-p.count("/"), p))[0]
    return best_path


def human_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} Б"

    units = ["КБ", "МБ", "ГБ", "ТБ"]
    size = float(n_bytes)

    for unit in units:
        size /= 1024.0
        if size < 1024:
            return f"{size:.1f} {unit}"

    return f"{size:.1f} ПБ"
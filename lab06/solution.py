def count_by_extension(paths: list) -> dict:
    counts = {}
    for path in paths:
        filename = path.split("/")[-1]

        idx = filename.rfind(".")

        if idx > 0:
            ext = filename[idx + 1:].lower()
        else:
            ext = ""

        counts[ext] = counts.get(ext, 0) + 1
    return counts


def deepest_path(paths: list) -> str:
    """Возвращает путь с наибольшей вложенностью (по количеству '/')."""
    if not paths:
        return ""

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
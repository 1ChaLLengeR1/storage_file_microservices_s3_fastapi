def original_name_from_path(path: str) -> str:
    if path.endswith('/'):
        path = path[:-1]

    return path.split('/')[-1]


def path_lvl(path: str) -> int:
    parts = path.strip('/').split('/')
    if len(parts) > 0:
        return len(parts) - 1
    else:
        return 0

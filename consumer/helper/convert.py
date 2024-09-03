def original_name_from_path(path: str) -> str:
    if path.endswith('/'):
        path = path[:-1]

    return path.split('/')[-1]
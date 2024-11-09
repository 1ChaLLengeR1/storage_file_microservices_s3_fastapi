def original_name_from_path(path: str) -> str:
    if path.endswith('/'):
        path = path[:-1]

    return path.split('/')[-1]


def split_path(catalog_name: str) -> list:
    directories = catalog_name.strip("/").split("/")
    paths = ["/".join(directories[:i + 1]) + "/" for i in range(len(directories))]
    return paths


def path_lvl(path: str) -> int:
    parts = path.strip('/').split('/')
    if len(parts) > 0:
        return len(parts) - 1
    else:
        return 0

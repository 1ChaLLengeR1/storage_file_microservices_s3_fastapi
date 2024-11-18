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


import os


def get_first_and_last_folder(path: str) -> dict:
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split(os.sep)
    if 'download' in parts:
        download_index = parts.index('download')
        relevant_parts = parts[download_index + 1:]
    else:
        relevant_parts = parts

    if not relevant_parts:
        return {"error": "path is None"}

    first_folder = relevant_parts[0]
    last_folder = relevant_parts[-1]

    data = {
        "global_catalog": first_folder,
        "last_catalog": last_folder
    }
    return data

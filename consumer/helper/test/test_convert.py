import pytest
from consumer.helper.convert import original_name_from_path


def test_original_name_from_path():
    test_collection_paths = ["test1/", "test1", "test1/test2/", "test1/test2",
                             "test1/test2/test3", "test1/test2/test3/", "test1/test2/test3/test4",
                             "test1/test2/test3/test4/"]

    test_collection_paths_correct = ["test1", "test1", "test2", "test2", "test3", "test3", "test4", "test4"]

    for i, path in enumerate(test_collection_paths):
        result = original_name_from_path(path)
        assert result == test_collection_paths_correct[i], pytest.fail(
            f"Failed for path: {path}. Expected: {test_collection_paths_correct[i]}, Got: {result}")

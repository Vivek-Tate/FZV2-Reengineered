import pytest
import os
from FinderZV2 import Logging  # replace 'your_module' with the actual module name


# Define the fixture here
@pytest.fixture
def log_data():
    return {
        'loggingBool': True,
        'logList': ["Test log"],
        'announcement': "Test announcement",
        'dir1': "Test dir1",
        'dir2': "Test dir2",
        'dir1Action': "Test dir1Action",
        'dir2Action': "Test dir2Action",
        'logTag': 'NC',
        'log_non_critical': True
    }


def test_Log(log_data):
    result = Logging.Log(**log_data)
    assert len(result) == 2
    assert any("Test announcement" in entry for entry in result)


def test_writeLogsToFile(tmpdir):
    logging = Logging()
    creationPath = tmpdir.mkdir("subdir")
    fileLines = ["Test log"]
    mode = "Test mode"

    logging.writeLogsToFile(str(creationPath), fileLines, mode)
    assert len(os.listdir(str(creationPath))) == 1
    with open(os.path.join(str(creationPath), os.listdir(str(creationPath))[0]), 'r') as f:
        lines = f.readlines()
    assert "Test log" in lines[0]


def test_log_entries(log_data):
    logging = Logging()
    result = logging.Log(**log_data)
    assert any("Test announcement" in entry for entry in result)
    assert any("Test dir1Action Test dir1 Test dir2Action Test dir2" in entry for entry in result)

from pathlib import Path

from pytest import fixture

from src.config import Config
from src.process_enrollments import process_file


@fixture
def config(tmp_path) -> Config:
    config = Config()
    config.test_mode = True
    output_path = tmp_path / "output"
    output_path.mkdir()
    config.output_path = output_path
    return config


def test_not_properly_formatted_json(capsys, config):
    f = Path("test/input/not_properly_formatted.json")
    process_file(f, config)
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"{f} is not a properly formatted JSON: <Extra data: line 2 column 24 (char 24)>\n"
    )

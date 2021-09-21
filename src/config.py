import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    input_path: Path = Path(".")
    enrollments_per_request: int = 10
    concurrent_requests: int = 10
    endpoint: str = "http://localhost:9777/api/rest/"
    test_mode: bool = True
    archive_path: Path = field(default=Path("input/archive"), init=False)
    output_path: Path = field(default=Path("output"), init=False)
    sample_ip_path: Path = field(default=Path("sample_id"), init=False)

    def __post_init__(self):
        this_module_path = Path(os.path.realpath(__file__))
        src_path = this_module_path.parent
        project_path = src_path.parent
        self.archive_path = self.input_path / "archive"
        if not self.archive_path.is_dir():
            self.archive_path.mkdir()
        if self.test_mode:
            test_path = project_path / "test"
            self.output_path = test_path / "output"
            if not self.output_path.is_dir():
                self.output_path.mkdir()
            self.sample_ip_path = test_path / "sample_ip"
            assert self.sample_ip_path.is_dir(), f"{self.sample_ip_path}"

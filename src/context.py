from dataclasses import dataclass, field
from pathlib import Path

from src.config import Config
from src.models.identify_process_response import IpResponse


@dataclass
class Context:
    config: Config
    gbp: str
    input_file: Path
    employees: list[dict]
    lots_total: int = field(default=0, init=False)
    ip_response: IpResponse = field(init=False)

    def __post_init__(self):
        seq_size = len(self.employees)
        total, remaining = divmod(seq_size, self.config.enrollments_per_request)
        self.lots_total = total + 1 if remaining else total

    def employees_lot(self, index: int) -> list[dict]:
        i, n = index, self.config.enrollments_per_request
        return self.employees[i * n : (i + 1) * n]

    def lot_index(self, index: int, sep="/") -> str:
        return f"{index+1}{sep}{self.lots_total}"

    @property
    def file_name(self) -> str:
        return self.input_file.name

    def output_file_for_test_mode(self, index: int) -> Path:
        result = self.config.output_path
        result /= f"{self.lot_index(index, sep='-')}_{self.file_name}"
        return result

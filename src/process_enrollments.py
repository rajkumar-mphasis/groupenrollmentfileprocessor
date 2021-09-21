import json
import time
from collections.abc import Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, TypeVar

import click
import requests
from requests import RequestException

from src.config import Config
from src.context import Context
from src.mapping.census import multi_census
from src.mapping.util import find_corresponding_product
from src.wynsure_api.identify_process import get_it_response

T = TypeVar("T")


def load_json_from_file(f: Path) -> Optional[dict]:
    """
    Read file f and return:
     - a JSON string if it can be parse
     - None if the file is not a properly formatted JSON
    """
    with open(f, "r", encoding="utf-8") as jsf:
        try:
            return json.load(jsf)
        except JSONDecodeError as e:
            print(f"{f} is not a properly formatted JSON: <{e}>")
            return None


def chunks(
    sequence: Sequence[T], n: int
) -> Iterator[tuple[Sequence[T], tuple[int, int]]]:
    """Yield successive (n-sized chunk, (chunk number, total)) tuple from sequence."""
    seq_size = len(sequence)
    total, remaining = divmod(seq_size, n)
    total = total + 1 if remaining else total
    for i in range(0, seq_size, n):
        yield sequence[i : i + n], (i // n + 1, total)


def call_bulk_upload_api(payload: str, context: Context, index: int) -> str:
    body = json.dumps(payload, ensure_ascii=False)
    headers = {"Content-Type": "application/json;charset=ISO-8859-1"}
    endpoint = context.config.endpoint + "BulkUpload/BulkEnrollment"
    try:
        response = requests.post(endpoint, data=body, headers=headers)
        if response.status_code == 200:
            ret = f"Lot {context.lot_index(index)} has been Successfully processed"
        else:
            ret = f"Error while processing lot {context.lot_index(index)}, response code {response.status_code}"
    except RequestException as e:
        ret = f"Error while processing lot {context.lot_index(index)}: {e!s}"
    return ret


def process_employees(context: Context, index: int) -> str:
    employees = context.employees_lot(index)
    payload = multi_census(employees, context.gbp)
    return call_bulk_upload_api(payload, context, index)


def save_payload_in_test_mode(context: Context, index: int) -> str:
    """Only for testing purpose, writes payload files in the folder of the path"""
    employees = context.employees_lot(index)
    payload = multi_census(employees, context.gbp, context.ip_response)
    output_file = context.output_file_for_test_mode(index)
    with open(output_file, "w", encoding="utf-8") as of:
        json.dump(payload, of, ensure_ascii=False, indent=4)
    return f"File <{output_file}> created"


def create_context_from_file(f: Path, config: Config) -> Optional[Context]:
    data = load_json_from_file(f)
    if data:
        enroll = "Enrollment_Detail"
        try:
            enroll_node: dict = data[enroll]
            gbp = enroll_node["GroupNumber"]
            employees = enroll_node["Employee"]
            return Context(gbp=gbp, input_file=f, employees=employees, config=config)
        except KeyError as e:
            key = f"{enroll}/{e.args[0]}" if e.args[0] != enroll else enroll
            print(f"{f} does not contain <{key}> key")
    return None


def process_file(f: Path, config: Config) -> None:
    context = create_context_from_file(f, config)
    if context:
        context.ip_response = get_it_response(context)
        # FGE temporary testing code - start
        print("FGE temporary testing code")
        for code in ["ACCD", "CRIT"]:
            print(find_corresponding_product(code, context.ip_response))
            #with open( code + '_data.json', 'w', encoding='utf-8') as f:
            #    json.dump(find_corresponding_product(code, context.ip_response), f, ensure_ascii=False, indent=4)
        # FGE temporary testing code - end
        process_function = (
            save_payload_in_test_mode if config.test_mode else process_employees
        )
        with ThreadPoolExecutor(max_workers=config.concurrent_requests) as executor:
            calls = []
            for index in range(context.lots_total):
                calls.append(executor.submit(process_function, context, index))
                for task in as_completed(calls):
                    print(task.result())


def process_enrollments(config: Config) -> None:
    """
    Periodically checks for new files.
    For each file: call IP, split enrollments, transform them in a Wynsure API format, call Wynsure API
    """
    while 1:
        for f in config.input_path.glob("*.json"):
            process_file(f, config)
            if not config.test_mode:
                f.rename(config.archive_path / f.name)
        if config.test_mode:
            break
        else:
            time.sleep(10)


@click.command()
@click.option(
    "-p",
    "--input-path",
    default="input",
    type=click.Path(exists=True, file_okay=False),
    help="Path to the folder containing input informatica files",
)
@click.option(
    "-e",
    "--enrollments-per-request",
    default=10,
    type=int,
    help="Number of enrollments to be processed per request to Wynsure bulk upload API",
)
@click.option(
    "-c",
    "--concurrent-requests",
    default=10,
    type=int,
    help="Max number of concurrent request sent in parallel to Wynsure bulk upload API",
)
@click.option(
    "-ep",
    "--endpoint",
    default="http://dcwws01:9801/api/rest/",
    type=str,
    help="URL of Wynsure bulk upload",
)
@click.option(
    "-t",
    "--test-mode",
    is_flag=True,
    help="""\b
              In test mode:
               - Stops once all files in the input folder are treated
               - Input files are not moved to <archive> folder
               - Identify Process API is not called, instead use an example file from <sample_ip> folder
               - Bulk upload API is not called, payload files are created instead in an <output> folder
              """,
)
def main(input_path, enrollments_per_request, concurrent_requests, endpoint, test_mode):
    """
    Call Wynsure bulk upload API from informatica group enrollment files

    \b
    Periodically checks for new files in <input-path> and for each file:
     1. Call identify process API to get information about the GBP
     2. Split enrollments in chunks of maximum <enrollments_per_request> enrollments
     3. Transform each chunks in a Wynsure bulk upload API format
     4. Call bulk upload API in up to <concurrent_requests> parallel requests
    """
    config = Config(
        input_path=Path(input_path),
        enrollments_per_request=enrollments_per_request,
        concurrent_requests=concurrent_requests,
        endpoint=endpoint,
        test_mode=True,
    )
    process_enrollments(config)

import datetime
import json

import requests

from src.context import Context
from src.models.identify_process_response import IpResponse


def call_identify_process_api(context: Context):
    # we might need to get the 2 dates from the first product node found in input file
    # (ApplicationDate -> SignatureDate, EffectiveDate -> EffectiveDate)
    # Right now using current date instead
    signature_date = effective_date = str(datetime.date.today())
    payload = {
        "className": "aAFCI_IdentifyProcess_In",
        "WithDetails": True,
        "GBPNumber": context.gbp,
        "MemberId": "dummyMemberId",
        "SignatureDate": signature_date,
        "EffectiveDate": effective_date,
        "IsInTestMode": False,
    }
    body = json.dumps(payload, ensure_ascii=False)
    headers = {"Content-Type": "application/json;charset=ISO-8859-1"}
    endpoint = context.config.endpoint + "GBFP/IdentifyProcess"
    try:
        ret = requests.post(endpoint, data=body, headers=headers)
        return ret
    except requests.exceptions.RequestException as e:
        return e


def get_it_response(context: Context) -> IpResponse:
    config = context.config
    if config.test_mode:
        ip_file = config.sample_ip_path / "example_1_multiproduct_4.json"
        with open(ip_file, encoding="utf-8") as f:
            ip_payload = json.load(f)
    else:
        ip_response = call_identify_process_api(context)
        ip_payload = ip_response.json()
    model = IpResponse.from_node(ip_payload, gbp=context.gbp)
    model.display()  # for testing
    return model

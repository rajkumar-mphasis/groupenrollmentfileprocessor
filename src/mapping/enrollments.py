from src.mapping.enrollment.insured import enrollment_insured
from src.mapping.enrollment.subscribed_entities import enrollment_subscribed_entities
from src.mapping.util import convert_date_format


def census_enrollment(employee, gbp, ip_response):
    dependents = employee["Dependents"] if "Dependents" in employee else {}
    if "Dependent" in dependents:
        for dependent in dependents["Dependent"]:
            if "Enrollments" in dependent and "Products" in dependent["Enrollments"]:
                enrollments = dependent["Enrollments"]
                subscribed_entities = [
                    enrollment_subscribed_entities(dependent, product, ip_response)
                        for product in enrollments["Products"]
                ]
            else:
                subscribed_entities = {}
        insured = [
            enrollment_insured(dependent) for dependent in dependents["Dependent"]
        ]
    else:
        subscribed_entities = {}

    #Process the sigle product from dependent
    if "Dependent" in dependents and isinstance(dependents["Dependent"], list):
        dependent = dependents["Dependent"][0]
        enrollments = dependent["Enrollments"] if "Enrollments" in dependent else {}
        if "Products" in enrollments and isinstance(enrollments["Products"], list):
            product = enrollments["Products"][0]
        else:
            product = {}
    else:
        product = {}

    return {
        "className": "aAFCI_CreateOrUpdateEnrollment_In",
        "BrokerAssociations": [],
        "DistributionUnitCode": "IA",
        "Insured": insured,
        "EnrollmentNumber": enrollment_enrollment_number(product),
        "EnrollmentInformation": enrollment_enrollment_information(product),
        "UpdateDate": "",
        "SubscribedEntities": subscribed_entities,
        "IsInTestMode": False,
    }


def enrollment_enrollment_number(product):
    return {
        "InternalPolicyIdentifier": {"InternalPolicyId": "", "IssuingCompanyCode": ""},
        "ExternalPolicyIdentifier": {"ExternalPolicyId": "", "ThirdPartyID": ""},
        "Buid": "",
    }


def enrollment_enrollment_information(product):
    signatureDate = product["ApplicationDate"] if "ApplicationDate" in product else ""

    return {
        "className": "aSPLI_MemberContract",
        "GBPNumber": {
            "InternalPolicyIdentifier": {
                "InternalPolicyId": "",
                "IssuingCompanyCode": "",
            },
            "ExternalPolicyIdentifier": {"ExternalPolicyId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "CertificateInternalID": "",
        "ExternalManagement": False,
        "ClaimExternalManagement": False,
        "ResidenceStateCode": {
            "StateLabel": "",
            "StateName": "AL",
            "StateCode": "AL",
        },
        "AdditionalDatas": enrollment_information_additional_datas(product),
        "CreationDate": "",
        "EffectiveDate": "",
        "SubscriptionDate": "",
        "SignatureDate": convert_date_format(signatureDate),
        "TermOrRenewalDate": None,
        "LastRenewalDate": None,
        "ReinstatementDate": None,
        "TerminationDate": None,
        "TerminationReason": "",
        "TerminationNumber": 0,
        "BillingMode": "Next Period",
        "EndorsementKind": "",
        "Status": "Pending",
        "PatchUpdateOnly": False,
    }


def enrollment_information_additional_datas(product):
    return {
        "className": "aSPCB_ClassificationValue",
        "ValueCode": "",
        "FieldValue": "",
        "NameDescription": "",
        "GrandfatheredClass": False,
        "FieldCode": "",
        "FieldName": "",
        "CodeForPopulationClass": "",
        "PatchUpdateOnly": False,
    }

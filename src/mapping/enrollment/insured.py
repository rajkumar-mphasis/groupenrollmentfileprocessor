def enrollment_insured(products):
    return {
        "className": "aSPLI_Insured_Data",
        "InsuredInformation": insured_insured_information(products),
        "AdditionalData": insured_additional_data(products),
        "Insured": insured_insured(products),
        "RelationshipsToInsured": "",
        "EffectiveDate": None,
        "ExpiryDate": None,
        "RuleTerminationDate": None,
        "CICoverageDetails": insured_ci_coverage_details(products),
        "IsInTestMode": False,
    }


def insured_insured_information(products):
    return {
        "className": "aSPLI_InsuredWithRelation",
        "Dependence_Deprecated5200": "",
        "MainOwnerRelationshipToInsured": "",
        "AdditionalData": [],
        "PersonAdditionalData": insured_information_person_additional_data(products),
        "ClientId": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "LastName": "",
        "FirstName": "",
        "BirthDate": "",
        "SSN": "",
        "IsInTestMode": False,
    }


def insured_information_person_additional_data(products):
    return {
        "className": "aSPCB_AdditionalData_ValueDescription",
        "Value": {
            "className": "aSPCB_ClassificationValue",
            "ValueCode": "",
            "FieldValue": "",
            "NameDescription": "",
            "GrandfatheredClass": False,
            "FieldCode": "",
            "FieldName": "",
            "CodeForPopulationClass": "",
            "PatchUpdateOnly": False,
        },
        "Description": None,
        "Visibility": "",
        "MandatoryLevel": "",
        "PositionOrderX": 0,
        "PositionOrderY": 0,
        "VisibilityRule": "",
        "CoverageCode": "",
        "IsInTestMode": False,
    }


def insured_additional_data(products):
    return {
        "className": "aSPCB_AdditionalData_ValueDescription",
        "Value": {
            "className": "aAFCI_ClassificationValueField",
            "Classification": {"Code": "", "Name": ""},
            "FieldValueCode": "",
            "FieldValueName": "",
            "FieldCode": "",
            "FieldName": "",
            "CodeForPopulationClass": "",
            "PatchUpdateOnly": False,
        },
        "Description": None,
        "Visibility": "",
        "MandatoryLevel": "",
        "PositionOrderX": 0,
        "PositionOrderY": 0,
        "VisibilityRule": "",
        "CoverageCode": "",
        "IsInTestMode": False,
    }


def insured_insured(products):
    return {
        "className": "aSPLI_GetPerson",
        "SearchPerson": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "CreateOrUpdatePerson": None,
        "IsInTestMode": False,
    }


def insured_ci_coverage_details(products):
    return {
        "TotalCoverageamount": {"amount": 0, "currency": "USD"},
        "LatestCoverageEffectiveDate": None,
        "InsuredHasPendingCoverage": False,
    }

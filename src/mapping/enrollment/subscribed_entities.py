from src.mapping.util import convert_date_format
from src.mapping.util import find_corresponding_product
import os
import json

def enrollment_subscribed_entities(dependent, product, ip_response):
    productCode = product["ProductCode"] if "ProductCode" in product else ""
    productCode = find_corresponding_product(productCode, ip_response).code
    
    # used sample ip_response JSON file. Getting Error while iterating actula ip_response data and need to replace this code
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "sample_ip" , "example_1_multiproduct_4.JSON")
    file = open(file_path,)
    ip_response = json.load(file)
    file.close()

    #Get respective ProductChoices from ip_response and map the Coverages
    if "PossibleEnrollmentData" in ip_response and "ProductChoices" in ip_response["PossibleEnrollmentData"]:
        possibleEnrollmentData = ip_response["PossibleEnrollmentData"]
        productDetails = {}
        for ProductChoice in possibleEnrollmentData["ProductChoices"]:
            if ("Product" in ProductChoice and "Code" in ProductChoice["Product"] and ProductChoice["Product"]["Code"] == productCode):
                productDetails = ProductChoice
                break

    subscribedCoverages = {}
    if "Options" in productDetails:
        for insuredCoverages in productDetails["Options"]:
            subscribedCoverages = [subscribed_entities_coverages(dependent, productDetails, insuredCoverages, subscriptionCoverages) for subscriptionCoverages in insuredCoverages["Options"]]

    return {
        "className": "aSPLI_CreateOrUpdateSubscribedProduct_In",
        "ProductCode": subscribed_entities_product_code(productDetails),
        "ProductInfo": subscribed_entities_product_info(product, productDetails),
        #subscribed_entities_coverages(dependent, productDetails, ip_response) for employee in productDetails
        "Coverages": subscribedCoverages,
        "IsInTestMode": False,
    }


def subscribed_entities_product_code(productDetails):
    productCode = productDetails["Product"]["Code"] if "Product" in productDetails and "Code" in productDetails["Product"] else ""
    return {
        "ProductIdentifier": {
            "IssuingCompanyCode": "",
            "ProductCode": productCode,
        },
        "Buid": "",
    }


def subscribed_entities_product_info(product, productDetails):
    effectiveDate = product["EffectiveDate"] if "EffectiveDate" in product else ""
    terminationDate = product["TerminationDate"] if "TerminationDate" in product else ""

    return {
        "className": "aAFCI_SubscribedProduct",
        "AdditionalDatas": product_info_additional_data(product),
        "ProductSpecificAdditionalData": [],
        "ExternalContractID": "",
        "EndorsementIndicator": "",
        "DoesProductSupportRollOver": False,
        "ProductCode": product_info_product_code(productDetails),
        "CreationDate": "",
        "EffectiveDate": convert_date_format(effectiveDate),
        "SubscriptionDate": "",
        "SignatureDate": None,
        "TermOrRenewalDate": None,
        "LastRenewalDate": None,
        "ReinstatementDate": None,
        "TerminationDate": convert_date_format(terminationDate),
        "TerminationReason": "",
        "TerminationNumber": 0,
        "BillingMode": "",
        "EndorsementKind": "",
        "Status": "Pending",
        "PatchUpdateOnly": False,
    }


def product_info_additional_data(product):
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


def product_info_product_code(productDetails):
    productCode = productDetails["Product"]["Code"] if "Product" in productDetails and "Code" in productDetails["Product"] else ""
    return {
        "ProductIdentifier": {
            "IssuingCompanyCode": "",
            "ProductCode": productCode,
        },
        "Buid": "",
    }


def subscribed_entities_coverages(dependent, productDetails, insuredCoverages, subscriptionCoverages):
    return {
            "className": "aSPLI_CreateOrUpdateIndividualLifeCoverage_In",
            "CoverageGeneralInformation": coverages_coverage_general_information(productDetails, subscriptionCoverages),
            "InsuredPersons": coverages_insured_persons(dependent, productDetails, insuredCoverages, subscriptionCoverages),
            "Beneficiaries": [],
            "CoverageAmount": None,
            "UnderwrittingData": [],
            "IsInTestMode": False,
    }
    

def coverages_coverage_general_information(productDetails, subscriptionCoverages):
    #optionCode = productDetails["Riders"] if "Riders" in productDetails else ""
    optionCode = subscriptionCoverages["Option"]["Code"] if "Option" in subscriptionCoverages and "Code" in subscriptionCoverages["Option"] else ""
    return {
        "className": "aSPLI_IndividualLifeCoverage",
        "SignatureDate": None,
        "OriginalEffectiveDate": None,
        "AcquisitionKind": "",
        "GrandFathered": False,
        "AdditionalDatas": coverage_general_information_additional_datas(productDetails),
        "CreationDate": "",
        "PackageName": "",
        "OptionCode": optionCode,
        "OptionName": "",
        "EffectiveDate": "",
        "SubscriptionDate": "",
        "TerminationDate": None,
        "TerminationReason": "",
        "TerminationNumber": 0,
        "BillingServiceName": "",
        "Status": "Pending",
        "OptionVersion": 0,
        "IsBuyUp": False,
        "BuyUpIndex": 0,
        "CoverageType": "",
        "PatchUpdateOnly": False,
    }


def coverage_general_information_additional_datas(productDetails):
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
        "Description": {
            "className": "aSPCB_Classification",
            "PossibleValues": [],
            "DefaultValue": None,
            "UseDefaultValue": False,
            "IsCalculated": False,
            "ExternalDescCode": "",
            "FieldCode": "",
            "FieldName": "",
            "CodeForPopulationClass": "",
            "PatchUpdateOnly": False,
        },
        "Visibility": "",
        "MandatoryLevel": "",
        "PositionOrderX": 0,
        "PositionOrderY": 0,
        "VisibilityRule": "",
        "CoverageCode": "",
        "IsInTestMode": False,
    }


def coverages_insured_persons(dependent, productDetails, insuredCoverages, subscriptionCoverages):
    relation = (
        #dependent["RelationshipToOwner"] if "RelationshipToOwner" in dependent else ""
        insuredCoverages["Insured"]["MainOwnerRelationshipToInsured"] if "Insured" in insuredCoverages and "MainOwnerRelationshipToInsured" in insuredCoverages["Insured"] else ""
    )

    return [
        {
            "className": "aSPLI_CreateOrUpdateCoveredPerson_In",
            "CoveredPerson": insured_persons_covered_person(
                dependent, productDetails, insuredCoverages, subscriptionCoverages
            ),
            "Details": {
                "className": "aSPLI_CoveredPerson",
                "Relationship_Deprecated": "",
                "EndDate": None,
                "EffectiveDate": "",
                "AdditionalDatas": insured_persons_additional_datas(productDetails),
                "SignatureDate": None,
                "PatchUpdateOnly": False,
            },
            "RelationToOwners": [
                {
                    "className": "aSPLI_RelationToOwner",
                    "PolicyOwner": {
                        "InternalClientId": "",
                        "ExternalClientIdentifier": {
                            "ExternalClientId": "",
                            "ThirdPartyID": "",
                        },
                        "Buid": "",
                    },
                    "Relation": relation,
                    "IsInTestMode": False,
                }
            ],
            "IsInTestMode": False,
        }
    ]


def insured_persons_additional_datas(productDetails):
    return [
        {
            "className": "aSPCB_AdditionalDataValue_Text",
            "FieldValue": "",
            "FieldCode": "",
            "FieldName": "",
            "CodeForPopulationClass": "",
            "PatchUpdateOnly": False,
        },
        {
            "className": "aAFCI_ClassificationValueField",
            "Classification": {
                "Code": "",
                "Name": "",
            },
            "FieldValueCode": "",
            "FieldValueName": "",
            "FieldCode": "",
            "FieldName": "",
            "CodeForPopulationClass": "",
            "PatchUpdateOnly": False,
        },
    ]


def insured_persons_covered_person(dependent, productDetails, insuredCoverages, subscriptionCoverages):
    return {
        "className": "aSPLI_GetPerson",
        "SearchPerson": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "CreateOrUpdatePerson": covered_person_create_or_update_person(
            dependent, productDetails, insuredCoverages, subscriptionCoverages
        ),
        "IsInTestMode": False,
    }


def covered_person_create_or_update_person(dependent, productDetails, insuredCoverages, subscriptionCoverages):
    return {
        "className": "aAFCI_CreateOrUpdatePerson_Data",
        "ip_responseInformations": [],
        "PersonIdentity": create_or_update_person_person_identity(
            dependent, productDetails, insuredCoverages, subscriptionCoverages
        ),
        "LegalRepresentative": None,
        "ClaimDisbursementChannel": [],
        "ClientId": create_or_update_person_client_id(productDetails),
        "ThirdPartyID": "FO",
        "UpdateDate": None,
        "Correspondences": create_or_update_person_correspondences(productDetails),
        "PaymentMethods": [],
        "ContactInformations": [],
        "LoginInformation": None,
        "IsInTestMode": False,
    }


def create_or_update_person_person_identity(dependent, productDetails, insuredCoverages, subscriptionCoverages):
    # ssn = dependent["SSN"] if "SSN" in dependent else ""
    # name = dependent["LastName"] if "LastName" in dependent else ""
    # shortName = dependent["FirstName"] if "FirstName" in dependent else ""
    # middleName1 = dependent["MiddleName"] if "MiddleName" in dependent else ""
    # birthDate = dependent["BirthDate"] if "BirthDate" in dependent else ""
    # gender = dependent["Gender"] if "Gender" in dependent else ""

    ssn = ""
    name = ""
    shortName = ""
    middleName1 = ""
    birthDate = ""
    gender = ""

    if "Insured" in insuredCoverages:
        ssn = insuredCoverages["Insured"]["SSN"] if "SSN" in insuredCoverages["Insured"] else ""
        name = insuredCoverages["Insured"]["LastName"] if "LastName" in insuredCoverages["Insured"] else ""
        shortName = insuredCoverages["Insured"]["FirstName"] if "FirstName" in insuredCoverages["Insured"] else ""
        middleName1 = insuredCoverages["Insured"]["MiddleName"] if "MiddleName" in insuredCoverages["Insured"] else ""
        birthDate = insuredCoverages["Insured"]["BirthDate"] if "BirthDate" in insuredCoverages["Insured"] else ""
        gender = insuredCoverages["Insured"]["Gender"] if "Gender" in insuredCoverages["Insured"] else ""       

    return {
        "className": "aAFCI_US_Person",
        "Gender": gender,
        "OnCSLNList": None,
        "AdditionalDatas": person_identity_additional_datas(productDetails),
        "ChildSupportLienOnFile": False,
        "PersonInternalID": "",
        "SSN": ssn,
        "MaritalStatus": "",
        "PersonTitleEnum": "",
        "PriorName": "",
        "MiddleName1": middleName1,
        "MiddleName2": "",
        "NameSuffix": "",
        "AttachedToAnOtherSSN": False,
        "Nationality": "",
        "BirthRank": 0,
        "BirthCountry": "",
        "BirthPlaceCity": "",
        "BirthPlaceZipCode": "",
        "BirthPlaceState": "",
        "LegalRepresentativeId_Deprecated5200": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "Occupation": "",
        "BirthDate": birthDate,
        "VisibilityCode": 2,
        "Delinquent": False,
        "UnderSurveillance": False,
        "Name": name,
        "ShortName": shortName,
        "CreationDate": "",
        "PreferredLanguageCode": "",
        "TerminationDate": None,
        "IsAnonymous": False,
        "PreferredContactChoice": "",
        "PatchUpdateOnly": False,
    }


def person_identity_additional_datas(product):
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


def create_or_update_person_client_id(product):
    return {
        "InternalClientId": "",
        "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
        "Buid": "",
    }


def create_or_update_person_correspondences(productDetails):
    return {
        "className": "aSPCB_Correspondence",
        "EffectiveDate": "",
        "AddressUsage": "0",
        "Address": correspondences_address(productDetails),
        "IsDefaultCorrespondance": True,
        "PrivatePhone": "",
        "PrivatePhoneExtension": "",
        "OfficePhone": "",
        "OfficePhoneExtension": "",
        "CellPhone": "",
        "Fax": "",
        "eMail": "",
        "MediaType": "",
        "Invalid": False,
        "InvalidReason": "",
        "PatchUpdateOnly": False,
    }


def correspondences_address(productDetails):
    return {
        "className": "aAFCI_PostalAddressWithValidation",
        "IsValidationAttempted": False,
        "IsValidStatus": False,
        "State": "",
        "Line1": "",
        "Line2": "",
        "ZipCodeAndCity": {"ZipCode": "", "City": ""},
        "Country": "",
        "IsNotMandatory": False,
        "CorrespondenceID": {"Buid": ""},
        "PatchUpdateOnly": False,
    }

from src.mapping.util import convert_date_format


def census_employee(employee, gbp):
    return {
        "className": "aSPLI_CreateOrUpdateEmployee_In",
        "EmployeeId": employee_employee_id(employee),
        "Employee": employee_employee(employee, gbp),
        "Person": employee_person(employee),
        "LegalEntityId": {
            "InternalClientId": gbp,
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "IsInTestMode": False,
    }


def employee_employee_id(employee):
    return {
        "EmployeeId": employee["EmployeeID"],
        "PersonId": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": "FO"},
            "Buid": "",
        },
        "LegalEntityId": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": "FO"},
            "Buid": "",
        },
        "Buid": "",
    }


def employee_employee(employee, gbp):
    division_id = (
        gbp if employee["DivisionID"] == "" else employee["DivisionID"]
    )  # I am not sure about that
    result = {
        "className": "aAFCI_Employee",
        "DivisionId": {
            "InternalClientId": division_id,
            "ExternalClientIdentifier": {
                "ExternalClientId": "",
                "ThirdPartyID": "FO",
            },
            "Buid": "",
        },
        "DivisionName": employee["EmployerName"],  # not certain
        "DivisionShortName": employee["EmployerName"],  # probably wrong
        "WorksiteState": "Undefined",
        "EffectiveDate": convert_date_format(employee["HireDate"]),
        "TerminationReason": "",
        "TerminationDate": convert_date_format(employee["TerminationDate"]),
        "HireDate": convert_date_format(employee["HireDate"]),
        "SalaryDefinedAtDate": None,
        "EmploymentStatus": "Active",
        "WorkingHours": employee["HoursWorkedPerWeek"],
        "WorkingHoursDefinedForFrequency": "Weekly",
        "WorkingCategory": "Full time",
        "BaseSalaryAmount": {
            "amount": employee["AnnualSalary"],
            "currency": "cUSDollar",
        },
        "BaseSalaryFrequency": "Annually",
        "SalaryCommissionAmount": {"amount": 0, "currency": "cUSDollar"},
        "SalaryCommissionFrequency": "Undefined",
        "SalaryBonusAmount": {"amount": 0, "currency": "cUSDollar"},
        "SalaryBonusFrequency": "Undefined",
        "CanBeEnrolled": True,
        "AdditionalDynamicDatas": [],  # TO DO
        "PatchUpdateOnly": False,
    }
    return result


def employee_person(employee):
    result = {
        "className": "aSPLI_CreateOrUpdatePerson_Data",
        "PersonIdentity": person_person_identity(employee),
        "LegalRepresentative": None,
        "ClaimDisbursementChannel": [],
        "ClientId": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "ThirdPartyID": "",  # no idea what this field is used for
        "UpdateDate": "",  # should we set current date here ?
        "Correspondences": [person_correspondence(employee)],
        "PaymentMethods": [],
        "ContactInformations": [],
        "LoginInformation": None,
        "IsInTestMode": False,
    }
    return result


def person_person_identity(employee):
    result = {
        "className": "aAFCI_US_Person",
        "Gender": "Male" if employee["Gender"] == "M" else "Female",
        "OnCSLNList": None,
        "AdditionalDatas": [],  # TODO
        "ChildSupportLienOnFile": False,
        "PersonInternalID": "",
        "SSN": employee["SSN"],
        "MaritalStatus": "Undefined",
        "PersonTitleEnum": "",
        "PriorName": "",
        "MiddleName1": employee["MiddleName"],
        "MiddleName2": "",
        "NameSuffix": "",
        "AttachedToAnOtherSSN": False,
        "Nationality": "UNITED STATES",  # information missing in input
        "BirthRank": 0,
        "BirthCountry": "UNITED STATES",
        "BirthPlaceCity": "",
        "BirthPlaceZipCode": "",
        "BirthPlaceState": "",
        "LegalRepresentativeId_Deprecated5200": {
            "InternalClientId": "",
            "ExternalClientIdentifier": {"ExternalClientId": "", "ThirdPartyID": ""},
            "Buid": "",
        },
        "Occupation": "",
        "BirthDate": convert_date_format(employee["BirthDate"]),
        "VisibilityCode": 2,
        "Delinquent": False,
        "UnderSurveillance": False,
        "Name": employee["LastName"],
        "ShortName": employee["FirstName"],
        "CreationDate": "",  # current date or automatically filled by Wynsure ?
        "PreferredLanguageCode": "En",
        "TerminationDate": None,
        "IsAnonymous": False,
        "PreferredContactChoice": "#DynamicalActorText# with Default Correspondence",  # no idea how this field should be fill
        "PatchUpdateOnly": False,
    }
    return result


def person_correspondence(employee):
    result = {
        "className": "aSPCB_Correspondence",
        "EffectiveDate": "",
        "AddressUsage": "3",
        "Address": {
            "className": "aAFCI_PostalAddressWithValidation",
            "IsValidationAttempted": False,
            "IsValidStatus": False,
            "State": employee["AddressState"],
            "Line1": employee["AddressLine1"],
            "Line2": employee["AddressLine2"],
            "ZipCodeAndCity": {
                "ZipCode": employee["Zip"],
                "City": "",  # should we call a get city from zipcode wynsure business service for this ?
            },
            "Country": employee[
                "AddressCountry"
            ],  # some conversion should be done here eg USA => UNITED STATES
            "IsNotMandatory": False,
            "CorrespondenceID": {"Buid": ""},
            "PatchUpdateOnly": False,
        },
        "IsDefaultCorrespondance": True,
        "PrivatePhone": employee["HomePhoneNo"],
        "PrivatePhoneExtension": "",
        "OfficePhone": "",
        "OfficePhoneExtension": "",
        "CellPhone": "",
        "Fax": "",
        "eMail": employee["EmailAddress"],
        "MediaType": "",
        "Invalid": False,
        "InvalidReason": "",
        "PatchUpdateOnly": False,
    }
    return result

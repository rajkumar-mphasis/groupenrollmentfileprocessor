from src.mapping.employee import census_employee
from src.mapping.enrollments import census_enrollment


def multi_census(employees, gbp, ip_response):
    census_list = [census_item(employee, gbp, ip_response) for employee in employees]
    result = {
        "className": "aSPLI_MultiCensusLoading_In",
        "ListCensusLoading": census_list,
        "IsInTestMode": False,
    }
    return result


def census_item(employee, gbp, ip_response):
    result = {
        "className": "aSPLI_CensusLoading_In",
        "Employee": census_employee(employee, gbp),
        "Enrollment": census_enrollment(employee, gbp, ip_response),
        "IsInTestMode": False,
    }
    return result

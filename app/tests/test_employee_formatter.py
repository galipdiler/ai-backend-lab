from app.employee_formatter import format_employee
from app.employee_model import Employee

def test_employee_return():
    employee=Employee("Galip","AI Engineering",26)
    result= format_employee(employee)
    assert result=="Galip | Department: AI Engineering | Age: 26"
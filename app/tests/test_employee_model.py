import pytest
from app.validator import InvalidAgeError
from app.employee_model import Employee, Manager

def test_manager_store_value():
    manager=Manager("Simge","AI Engineering",32,team_size=5)
    assert manager.name== "Simge"
    assert manager.department== "AI Engineering"
    assert manager.age== 32
    assert manager.team_size== 5 

def test_manager_negetive_age():
    with pytest.raises(InvalidAgeError):
        Manager("Simge","AI Engineering",-5,team_size=5)

def test_employee_reject_negative_age():
    with pytest.raises(InvalidAgeError):
        Employee("Galip","AI Enginering",-5)

def test_employee_store_initial_value():
    employee=Employee("Galip","AI Engineer",26)

    assert employee.name== "Galip"
    assert employee.department=="AI Engineer"
    assert employee.age== 26

def test_employe_changes_department():
    employee=Employee("Galip","AI Engineering",26)
    employee.change_department("LLM Engineering")
    assert employee.department=="LLM Engineering"
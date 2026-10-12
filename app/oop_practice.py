from app.employee_model import Employee,Manager
from app.employee_formatter import (format_employee,format_employee_short)
from collections.abc import Callable

def display_employee(employee:Employee, formatter:Callable[[Employee],str], )-> None:
    text=formatter(employee)
    print(text)
def main() -> None:
    employee1 = Employee("Galip", "AI Engineering", 26)
    manager = Manager("Simge", "Data Engineering", 32, team_size=5)

    display_employee(manager, format_employee)
    manager.change_department("AI Engineering")
    display_employee(manager, format_employee)

    print(f"Ekip büyüklüğü: {manager.team_size}")
    print(format_employee(employee1))

    new_department = input("Yeni departmanı giriniz: ")
    employee1.change_department(new_department)

    display_employee(employee1,format_employee)
    display_employee(employee1,format_employee_short)


if __name__ == "__main__":
    main()
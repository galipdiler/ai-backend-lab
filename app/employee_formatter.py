from app.employee_model import Employee

def format_employee(employee: Employee) -> str:
    return(
           f" {employee.name} | Department: {employee.department} | Age: {employee.age}" 
    )
def format_employee_short (employee: Employee) -> str:
    return f"{employee.name} | {employee.department}"
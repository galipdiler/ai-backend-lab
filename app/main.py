from app.employee import create_employee

name=input("Çalışanın adını giriniz: ")
department=input("Departmanını giriniz: ")
age=int(input("yasını giriniz: "))

employee=create_employee(name,department,age)

print(employee)

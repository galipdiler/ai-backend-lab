from fastapi import FastAPI ,Query,HTTPException,Response
from app.schemeas import EmployeeCreate, normalize_employee_name,EmployeeDepartmentUpdate,EmployeeResponse
from threading import Lock
from uuid import uuid4

app=FastAPI()
employees:dict[str,EmployeeCreate]={}
employees_lock = Lock()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/employees/{employee_id}",response_model=EmployeeResponse)
def get_employee(employee_id: str): 
    employee=employees.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.",)
    return{
        "id":employee_id,
        **employee.model_dump(),
    }
@app.get("/employees",response_model=list[EmployeeResponse])
def list_employees(department: str | None=None, limit : int=Query(default=10,ge=1,le=100),):
    with employees_lock:
        records= list(employees.items())
    results=[]

    for employee_id, employee in records:
        if department is not None:
            if employee.department.casefold() !=department.casefold():
                continue
        results.append({
            "id":employee_id,
            **employee.model_dump(),
        })
        if len(results) >= limit:
            break
    return results
    
@app.post("/employees", status_code=201,response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):
    name_key = (
        normalize_employee_name(employee.name),
        normalize_employee_name(employee.last_name),
    )
    
    with employees_lock:
        for existing in employees.values():
            existing_key = (
                normalize_employee_name(existing.name),
                normalize_employee_name(existing.last_name),
            )
            if existing_key == name_key:
                raise HTTPException(
                    status_code=409,
                    detail="Bu ad ve soyadla bir çalışan zaten kayıtlı.",
                )

        employee_id = str(uuid4())
        employees[employee_id] = employee

    return {"id": employee_id, **employee.model_dump()}
@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id:str)-> Response:
    with employees_lock:
        employee= employees.pop(employee_id,None)

    if employee is None:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı",)
    return Response(status_code=204)
@app.patch("/employees/{employee_id}",response_model=EmployeeResponse)
def update_employee_department(employee_id:str,update:EmployeeDepartmentUpdate,):
    with employees_lock:
        employee=employees.get(employee_id)
        if employee is None:
            raise HTTPException(status_code=404,detail="Çalışan bulunamadı.",)
        updated_employee=employee.model_copy(update={"department":update.department})
        employees[employee_id]=updated_employee
    return{"id":employee_id,**updated_employee.model_dump(),}
    
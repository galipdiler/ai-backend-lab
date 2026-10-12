from unicodedata import normalize

from pydantic import BaseModel, Field, field_validator

class EmployeeDepartmentUpdate(BaseModel):
    department:str =Field (min_length=1)
    @field_validator("department", mode="before")
    @classmethod
    def clean_department(cls,value:object)->object:
        if isinstance(value,str):
            return " ".join(value.split())
        return value


def normalize_employee_name(value: str) -> str:
    # Treat Turkish I variants alike for duplicate matching.
    return normalize("NFC", value).casefold().replace("i\u0307", "i").replace("ı", "i")


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    age: int = Field(ge=0)

    @field_validator("name", "last_name","department", mode="before")
    @classmethod
    def clean_name(cls, value: object) -> object:
        if isinstance(value, str):
            return " ".join(normalize("NFC", value).split())
        return value


class EmployeeResponse(EmployeeCreate):
    id: str

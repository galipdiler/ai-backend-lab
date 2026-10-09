class Employee:
    def __init__(self, name: str, department: str, age: int) -> None:
        self.name = name
        self.department = department
        self.age = age

    def introduce(self) -> str:
        return (
            f"Ben {self.name}, {self.department} departmanında "
            f"çalışıyorum ve {self.age} yaşındayım."
        )
    def change_department(self, new_department: str) -> None:
        self.department = new_department
class Manager(Employee):
    def __init__(self, name:str, department:str, age:int, team_size:int) ->None :
        super().__init__(name, department, age)
        self.team_size= team_size
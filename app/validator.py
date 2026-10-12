

class InvalidAgeError(ValueError):
    pass
def validate_age(age:int)-> int:
    if age<0:
        raise InvalidAgeError("Yaş negatif olamaz. ")
    return age
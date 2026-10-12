class InvalidAgeError(ValueError):
    pass

def validate_age(age:int)-> int:
    if age <0:
        raise InvalidAgeError("Yaş negatif olamaz")
    return age

def read_age()-> int:
    while True:
        raw_age=input("Yaşınızı giriniz: ")
        try:
            age=int(raw_age)
        except ValueError:
            print("Geçersiz giriş tam sayı girmeniz gerekiyor")
            continue
        try:
            return validate_age(age)
        except InvalidAgeError as error:
            print(error)
        

def main ()-> None:
    age=read_age()
    print(f"yaşınız: {age}")

if __name__ == "__main__":
    main()
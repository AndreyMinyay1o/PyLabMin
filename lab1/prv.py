class Validator:
    @staticmethod
    def validate_surname(surname):
        if not surname.isalpha():
            raise ValueError("Фамилия должна состоять только из букв")
        return surname

    @staticmethod
    def validate_name(name):
        if not name.isalpha():
            raise ValueError("Имя должно состоять только из букв")
        return name

    @staticmethod
    def validate_phone(phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Номер телефона должен состоять из 10 цифр")
        return phone

class Client:
    def __init__(self, surname, name, patronymic, address, phone):
        self.surname = Validator.validate_surname(surname)
        self.name = Validator.validate_name(name)
        self.phone = Validator.validate_phone(phone)
        self.patronymic = patronymic
        self.address = address

    def validate(self):
        self.surname = self.validate_surname(self.surname)
        self.name = self.validate_name(self.name)
        self.phone = self.validate_phone(self.phone)

    def __str__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self.phone == other.phone

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def short_version(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

    def full_version(self):
        return f"{self.surname} {self.name} {self.patronymic}, Адрес: {self.address}, Телефон: {self.phone}"

class ShortClientInfo:
    def __init__(self, surname, name, phone):
        self.surname = surname
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.surname} {self.name[0]}. Телефон: {self.phone}"

class ClientInfo(ShortClientInfo, Client):
    def __init__(self, surname, name, patronymic, address, phone):
        Client.__init__(self, surname, name, patronymic, address, phone)
        ShortClientInfo.__init__(self, surname, name, phone)

  if __name__ == "__main__":
    client_data = {
        "surname": "Миняйло",
        "name": "Андрей",
        "patronymic": "Андреевич",
        "address": "Улица Ставропольская 149",
        "phone": "890005150"
    }

    client = Client.from_json(client_data)

    print("Краткая информация:", client.short_version())
    print("Полная информация:", client.full_version())

    client2_data = {
        "surname": "Миняйло",
        "name": "Андрей",
        "patronymic": "Андреевич",
        "address": "Улица Ставропольская 149",
        "phone": "890005150"
    }
    client2 = Client.from_json(client2_data)

    print("Сравнение клиентов по телефону:", client == client2)

    client_info = ClientInfo("Миняйло", "Андрей", "Андреевич", "Улица Ставропольская 149", "890005150")
    print("Информация через ClientInfo:", client_info.short_version())

import re
import json
import uuid
import yaml
import sqlite3

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
class MyEntity_rep_json:
    def __init__(self, filename):
        self.filename = filename
        self.entities = self._read_from_json()

    def _read_from_json(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file) or []
                return data
        except FileNotFoundError:
            return []

    def _write_to_json(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.entities, file, ensure_ascii=False, indent=4)

    def get_by_id(self, entity_id):
        return next((entity for entity in self.entities if entity['id'] == entity_id), None)

    def get_k_n_short_list(self, k, n):
        return self.entities[(k - 1) * n : k * n]

    def sort_by_field(self, field):
        self.entities.sort(key=lambda x: x.get(field, ""))

    def add_entity(self, entity):
        entity['id'] = str(uuid.uuid4())
        self.entities.append(entity)
        self._write_to_json()

    def replace_entity(self, entity_id, new_entity):
        for i, entity in enumerate(self.entities):
            if entity['id'] == entity_id:
                self.entities[i] = new_entity
                self._write_to_json()
                return
        print(f"Entity with ID {entity_id} not found.")

    def delete_entity(self, entity_id):
        self.entities = [entity for entity in self.entities if entity['id'] != entity_id]
        self._write_to_json()

    def get_count(self):
        return len(self.entities)

class MyEntity_rep_yaml:
    def __init__(self, filename):
        self.filename = filename
        self.entities = self._read_from_yaml()

    def _read_from_yaml(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []
                return data
        except FileNotFoundError:
            return []

    def _write_to_yaml(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            yaml.dump(self.entities, file, default_flow_style=False, allow_unicode=True)

    def get_by_id(self, entity_id):
        return next((entity for entity in self.entities if entity['id'] == entity_id), None)

    def get_k_n_short_list(self, k, n):
        return self.entities[(k - 1) * n : k * n]

    def sort_by_field(self, field):
        self.entities.sort(key=lambda x: x.get(field, ""))

    def add_entity(self, entity):
        entity['id'] = str(uuid.uuid4())
        self.entities.append(entity)
        self._write_to_yaml()

    def replace_entity(self, entity_id, new_entity):
        for i, entity in enumerate(self.entities):
            if entity['id'] == entity_id:
                self.entities[i] = new_entity
                self._write_to_yaml()
                return
        print(f"Entity with ID {entity_id} not found.")

    def delete_entity(self, entity_id):
        self.entities = [entity for entity in self.entities if entity['id'] != entity_id]
        self._write_to_yaml()

    def get_count(self):
        return len(self.entities)

class MyEntity_rep:
    def __init__(self, filename):
        self.filename = filename
        self.entities = self.read_from_file()

    def read_from_file(self):
        raise NotImplementedError("Метод должен быть реализован в дочерних классах")

    def write_to_file(self):
        raise NotImplementedError("Метод должен быть реализован в дочерних классах")

    def get_by_id(self, entity_id):
        for entity in self.entities:
            if entity['id'] == entity_id:
                return entity
        return None

    def get_k_n_short_list(self, k, n):
        return self.entities[n * k: (n + 1) * k]

    def sort_by_field(self, field):
        self.entities.sort(key=lambda x: x.get(field))

    def add_entity(self, entity):
        entity['id'] = str(uuid.uuid4())
        self.entities.append(entity)
        self.write_to_file()

    def replace_entity(self, entity_id, new_entity):
        for i, entity in enumerate(self.entities):
            if entity['id'] == entity_id:
                self.entities[i] = new_entity
                self.write_to_file()
                return
        raise ValueError(f"Entity with ID {entity_id} not found")

    def delete_entity(self, entity_id):
        self.entities = [entity for entity in self.entities if entity['id'] != entity_id]
        self.write_to_file()

    def get_count(self):
        return len(self.entities)

class MyEntity_rep_json(MyEntity_rep):
    def read_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.entities, file, indent=4)

class MyEntity_rep_yaml(MyEntity_rep):
    def read_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except (FileNotFoundError, yaml.YAMLError):
            return []

    def write_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            yaml.dump(self.entities, file)

class MyEntity_rep_DB:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                name TEXT,
                surname TEXT
            )
        ''')
        self.connection.commit()

    def add_entity(self, entity):
        entity_id = str(uuid.uuid4()) 
        self.cursor.execute('''
            INSERT INTO entities (id, name, surname) 
            VALUES (?, ?, ?)
        ''', (entity_id, entity['name'], entity['surname']))
        self.connection.commit()
        return entity_id 

    def get_by_id(self, entity_id):
        self.cursor.execute('''
            SELECT * FROM entities WHERE id = ?
        ''', (entity_id,))
        result = self.cursor.fetchone()
        if result:
            return {'id': result[0], 'name': result[1], 'surname': result[2]}
        return None

    def get_k_n_short_list(self, k, n):
        self.cursor.execute('''
            SELECT * FROM entities LIMIT ?, ?
        ''', ((k-1)*n, n))
        result = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'surname': row[2]} for row in result]

    def sort_by_field(self, field):
        self.cursor.execute(f'''
            SELECT * FROM entities ORDER BY {field}
        ''')
        result = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'surname': row[2]} for row in result]

    def get_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM entities')
        return self.cursor.fetchone()[0]

def test_json_operations():
    print("\nTesting JSON Operations:")
    json_filename = "entities.json"
    entity_json_rep = MyEntity_rep_json(json_filename)

    entity = {"name": "Andrey", "surname": "Minyaylo"}
    entity_json_rep.add_entity(entity)

    print("Added Entity:", entity)

    print("Entity Count:", entity_json_rep.get_count())

    entity_id = entity_json_rep.entities[0]['id']
    print("Get Entity by ID:", entity_json_rep.get_by_id(entity_id))

    entity_json_rep.sort_by_field("name")
    print("Sorted Entities:", entity_json_rep.entities)

    new_entity = {"id": entity_id, "name": "Dmitriy", "surname": "Liksukov"}
    entity_json_rep.replace_entity(entity_id, new_entity)
    print("Replaced Entity:", new_entity)

    entity_json_rep.delete_entity(entity_id)
    print("Entity Count after Deletion:", entity_json_rep.get_count())

def test_yaml_operations():
    print("\nTesting YAML Operations:")
    yaml_filename = "entities.yaml"
    entity_yaml_rep = MyEntity_rep_yaml(yaml_filename)

    entity = {"name": "Andrey", "surname": "Minyaylo"}
    entity_yaml_rep.add_entity(entity)

    print("Added Entity:", entity)

    print("Entity Count:", entity_yaml_rep.get_count())

    entity_id = entity_yaml_rep.entities[0]['id']
    print("Get Entity by ID:", entity_yaml_rep.get_by_id(entity_id))

    entity_yaml_rep.sort_by_field("name")
    print("Sorted Entities:", entity_yaml_rep.entities)

    new_entity = {"id": entity_id, "name": "Dmitriy", "surname": "Liksukov"}
    entity_yaml_rep.replace_entity(entity_id, new_entity)
    print("Replaced Entity:", new_entity)

    entity_yaml_rep.delete_entity(entity_id)
    print("Entity Count after Deletion:", entity_yaml_rep.get_count())


def test_db_operations():
    print("\nTesting DB Operations:")
    db_filename = "entities.db"
    entity_db_rep = MyEntity_rep_DB(db_filename)

    entity = {"name": "Andrey", "surname": "Minyaylo"}
    entity_id = entity_db_rep.add_entity(entity)
    print(f"Added Entity: {entity}, ID: {entity_id}")

    entity_by_id = entity_db_rep.get_by_id(entity_id)
    print("Get Entity by ID:", entity_by_id)

    count = entity_db_rep.get_count()
    print("Entity Count:", count)

    sorted_entities = entity_db_rep.sort_by_field("name")
    print("Sorted Entities:", sorted_entities)

    k_n_list = entity_db_rep.get_k_n_short_list(2, 2)
    print("K-N Short List:", k_n_list)

if __name__ == "__main__":
    test_json_operations()
    test_yaml_operations()
    test_db_operations()

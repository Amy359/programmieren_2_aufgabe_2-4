import json
from PIL import Image

class Person:

    @staticmethod
    def get_person_db(pfad_db):
        return "mydatabase"

    @staticmethod
    def load_person_data():
        try:
        
            with open("data/person_db.json", "r") as file:
                person_data = json.load(file)
        except FileNotFoundError:
            print("Datei 'data/person_db.json' nicht gefunden. Nutze Testdaten.")
            person_data = [
                {"id": 1, "date_of_birth": 1989, "firstname": "Julian", "lastname": "Huber", "picture_path": "data/pictures/tb.jpg", "ekg_tests": [], "gender": "male"}
            ]

        return [
            Person(p["id"], p["date_of_birth"], p["firstname"], p["lastname"], p["picture_path"], p["ekg_tests"], p.get("gender", "male"))
            for p in person_data
        ]

    
    @staticmethod
    def load_by_id(person_id):
       
        persons = Person.load_person_data()
        return next((p for p in persons if p.id == person_id), None)

    @staticmethod
    def get_person_list(persons_list):
        return [person.get_full_name() for person in persons_list]

    @staticmethod
    def find_person_data_by_name(full_name):
        if ", " not in full_name:
            return None
            
        lastname, firstname = full_name.split(", ", 1)
        return next((p for p in Person.load_person_data() if p.firstname == firstname and p.lastname == lastname), None)


    def __init__(self, id: int, date_of_birth: int, firstname, lastname, picture_path, ekg_tests, gender="male"):
        self.id = id
        self.date_of_birth = int(date_of_birth)
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.gender = gender
        self.hr_max = self.calc_max_heart_rate()

    
    def calc_age(self):
    
        return 2026 - self.date_of_birth

    def calc_max_heart_rate(self):
        return 220 - self.calc_age()

    def set_hr(self, hr):
        self.hr_max = hr

    def get_full_name(self):
        return f"{self.lastname}, {self.firstname}"

    def get_image(self):
        try:
            return Image.open(self.picture_path)
        except FileNotFoundError:
            print(f"Bild unter {self.picture_path} wurde nicht gefunden.")
            return None

    def __str__(self):
        return f"Person(ID: {self.id}, Name: {self.get_full_name()}, Alter: {self.calc_age()}, Max HR: {self.hr_max})"


if __name__ == "__main__":
    print("This is a module with some functions to read the person data\n")
    
    
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print("Gefundene Namen:", person_names)
    
   
    found_person = Person.find_person_data_by_name("Huber, Julian")
    print("Suchergebnis nach Name:", found_person)
    
    
    person_by_id = Person.load_by_id(1)
    print("Suchergebnis nach ID (load_by_id):", person_by_id)

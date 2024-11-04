from datetime import datetime, timedelta

class Field:
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додаємо перевірку коректності даних та перетворюємо рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = self.birthday.value.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if 0 <= (next_birthday - today).days < days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = next((rec for rec in book.records if rec.name.value == name), None)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = next((rec for rec in book.records if rec.name.value == name), None)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = next((rec for rec in book.records if rec.name.value == name), None)
    if record and record.birthday:
        return f"{record.name.value}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Birthday not found."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays(7)
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    result = "Upcoming birthdays:\n"
    for record in upcoming_birthdays:
        result += f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}\n"
    return result

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.strip().lower().split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "change":
            print("Functionality to be added.")
        elif command == "phone":
            print("Functionality to be added.")
        elif command == "all":
            for record in book.records:
                phones = ', '.join(phone.value for phone in record.phones)
                print(f"{record.name.value}: {phones}")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
def run_tests():
    book = AddressBook()
    
    # Додаємо запис
    print(add_contact(["John Doe", "1234567890"], book))
    print(add_contact(["Jane Doe", "0987654321"], book))
    
    # Додаємо день народження
    print(add_birthday(["John Doe", "15.05.1990"], book))
    print(add_birthday(["Jane Doe", "20.05.1995"], book))
    
    # Показуємо день народження
    print(show_birthday(["John Doe"], book))
    print(show_birthday(["Jane Doe"], book))
    
    # Показуємо всі контакти
    for record in book.records:
        phones = ', '.join(phone.value for phone in record.phones)
        print(f"{record.name.value}: {phones}")
    
    # Показуємо дні народження, які відбудуться протягом наступного тижня
    print(birthdays([], book))
    
    # Привітання від бота
    print("How can I help you?")
    
    # Закриття програми
    print("Good bye!")

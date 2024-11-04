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

# Приклад використання
book = AddressBook()

# Додаємо записи
record1 = Record("John Doe")
record1.add_phone("1234567890")
record1.add_birthday("05.11.1990")

record2 = Record("Jane Doe")
record2.add_phone("0987654321")
record2.add_birthday("06.11.1995")

record3 = Record("Alice Johnson")
record3.add_phone("5551234567")
record3.add_birthday("07.11.1992")

book.add_record(record1)
book.add_record(record2)
book.add_record(record3)

# Отримуємо найближчі дні народження
upcoming = book.get_upcoming_birthdays(7)
for record in upcoming:
    print(f"{record.name.value}'s birthday is in {record.days_to_birthday()} days")

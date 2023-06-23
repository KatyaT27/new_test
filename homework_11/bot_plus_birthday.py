from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value=None):
        self._value = None
        self.value = value

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.validate(new_value):
            raise ValueError("Invalid value")
        self._value = new_value

    def validate(self, value):
        return True


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, index):
        if 0 <= index < len(self.phones):
            del self.phones[index]

    def edit_phone(self, index, phone):
        if 0 <= index < len(self.phones):
            self.phones[index].value = phone

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = datetime.now().date()
        next_birthday = datetime.strptime(
            self.birthday.value, "%d-%m-%Y").date().replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __repr__(self):
        return f"Name: {self.name}, Phones: {self.phones}, Birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def edit_record_name(self, name, new_name):
        if name in self.data:
            record = self.data[name]
            record.name.value = new_name
            self.data[new_name] = record
            del self.data[name]

    def add_phone_to_record(self, name, phone):
        if name in self.data:
            record = self.data[name]
            record.add_phone(phone)

    def remove_phone_from_record(self, name, index):
        if name in self.data:
            record = self.data[name]
            record.remove_phone(index)

    def edit_phone_in_record(self, name, index, phone):
        if name in self.data:
            record = self.data[name]
            record.edit_phone(index, phone)

    def search_records(self, **kwargs):
        results = []
        for record in self.data.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(record, key) or getattr(record, key).value != value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

    def __iter__(self):
        return iter(self.data.values())


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter command (add/search/remove/edit/exit): ")
        if command == "exit":
            break
        elif command == "add":
            name = input("Enter name: ")
            birthday = input(
                "Enter birthday (DD-MM-YYYY) or press Enter to skip: ")
            record = Record(name, birthday)
            address_book.add_record(record)
            print("Contact added successfully.")
        elif command == "search":
            criteria = {}
            while True:
                field = input(
                    "Enter field name (name/phone) or press Enter to search: ")
                if field == "":
                    break
                value = input("Enter field value: ")
                criteria[field] = value
            results = address_book.search_records(**criteria)
            if results:
                print("Search results:")
                for result in results:
                    print(result)
            else:
                print("No matching records found.")
        elif command == "remove":
            name = input("Enter name: ")
            if name in address_book.data:
                address_book.remove_record(name)
                print("Contact removed successfully.")
            else:
                print("Contact not found.")
        elif command == "edit":
            name = input("Enter name: ")
            if name in address_book.data:
                record = address_book.data[name]
                phone = input("Enter phone number: ")
                record.add_phone(phone)
                print("Phone number added successfully.")
            else:
                print("Contact not found.")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, index):
        if 0 <= index < len(self.phones):
            del self.phones[index]

    def edit_phone(self, index, phone):
        if 0 <= index < len(self.phones):
            self.phones[index].value = phone

    def __repr__(self):
        return f"Name: {self.name}, Phones: {self.phones}"


class AddressBook(UserDict):
    def add_record(self, name):
        record = Record(name)
        self.data[name] = record

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
                if key == "name":
                    if record.name.value != value:
                        match = False
                        break
                elif key == "phone":
                    if not any(phone.value == value for phone in record.phones):
                        match = False
                        break
            if match:
                results.append(record)
        return results


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print("Good bye!")
            break
        elif command == "add":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            address_book.add_record(name)
            address_book.add_phone_to_record(name, phone)
            print("Contact added successfully.")
        elif command == "remove":
            name = input("Enter name: ")
            if name in address_book:
                address_book.remove_record(name)
                print("Contact removed successfully.")
            else:
                print("Contact not found.")
        elif command == "edit":
            name = input("Enter name: ")
            if name in address_book:
                new_name = input("Enter new name: ")
                address_book.edit_record_name(name, new_name)
                print("Contact name updated successfully.")
            else:
                print("Contact not found.")
        elif command == "add phone":
            name = input("Enter name: ")
            if name in address_book:
                phone = input("Enter phone number: ")
                address_book.add_phone_to_record(name, phone)
                print("Phone number added successfully.")
            else:
                print("Contact not found.")
        elif command == "remove phone":
            name = input("Enter name: ")
            if name in address_book:
                index = int(input("Enter phone index: "))
                address_book.remove_phone_from_record(name, index)
                print("Phone number removed successfully.")
            else:
                print("Contact not found.")
        elif command == "edit phone":
            name = input("Enter name: ")
            if name in address_book:
                index = int(input("Enter phone index: "))
                phone = input("Enter new phone number: ")
                address_book.edit_phone_in_record(name, index, phone)
                print("Phone number updated successfully.")
            else:
                print("Contact not found.")
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
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value: str):
        if value.isdigit():
            self._value = value
        else:
            print('The phone number must contain only digits')


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        try:
            datetime.strptime(value, '%d/%m/%Y')
            self._value = value
        except ValueError:
            print('Invalid birthday format. Please use DD/MM/YYYY.')


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime.strptime(
                self.birthday.value, '%d/%m/%Y').date().replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None


class AddressBook(UserDict):
    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]


def main():
    address_book = AddressBook()
    commands = {
        'add': add_contact,
        'remove': remove_contact,
        'edit': edit_contact,
        'search': search_contacts,
        'exit': exit_program
    }

    while True:
        print_commands()
        command = input('Enter command: ').lower().strip()

        if command in commands:
            commands[command](address_book)
        else:
            print('Invalid command. Please try again.')


def print_commands():
    print('COMMANDS:')
    print('add - Add a contact')
    print('remove - Remove a contact')
    print('edit - Edit a contact')
    print('search - Search contacts')
    print('exit - Exit the program')


def add_contact(address_book):
    name = input('Enter name: ')
    phone = input('Enter phone number: ')
    birthday = input('Enter birthday (DD/MM/YYYY): ')
    record = Record(name, phone, birthday)
    address_book.data[name] = record
    print('Contact added successfully.')


def remove_contact(address_book):
    name = input('Enter name: ')
    if name in address_book.data:
        del address_book.data[name]
        print('Contact removed successfully.')
    else:
        print('Contact not found.')


def edit_contact(address_book):
    name = input('Enter name: ')
    if name in address_book.data:
        record = address_book.data[name]
        print('Current contact details:')
        print('Name:', record.name.value)
        print('Phone:', record.phone.value)
        print('Birthday:', record.birthday.value)

        new_name = input(
            'Enter new name (leave empty to keep the current value): ')
        new_phone = input(
            'Enter new phone number (leave empty to keep the current value): ')
        new_birthday = input(
            'Enter new birthday (DD/MM/YYYY) (leave empty to keep the current value): ')

        if new_name:
            record.name.value = new_name
        if new_phone:
            record.phone.value = new_phone
        if new_birthday:
            record.birthday.value = new_birthday

        print('Contact edited successfully.')
    else:
        print('Contact not found.')


def search_contacts(address_book):
    field = input(
        'Enter field name (name/phone) or press Enter to search: ').lower().strip()
    value = input('Enter search value: ')

    results = []
    if field and field in ['name', 'phone']:
        for record in address_book.data.values():
            if field == 'name' and record.name.value.lower() == value.lower():
                results.append(record)
            elif field == 'phone' and record.phone.value == value:
                results.append(record)
    else:
        for record in address_book.data.values():
            results.append(record)

    print('Search results:')
    for result in results:
        print('Name:', result.name.value)
        print('Phone:', result.phone.value)
        print('Birthday:', result.birthday.value)
        print()

    if not results:
        print('No contacts found.')


def exit_program(address_book):
    print('Exiting the program.')
    # Additional cleanup or saving operations can be performed here, if needed.
    quit()


if __name__ == '__main__':
    main()

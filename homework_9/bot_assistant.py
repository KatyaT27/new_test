contacts = {}


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except (ValueError, IndexError):
            return "Invalid input."

    return inner


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_contact(name, phone):
    contacts[name] = phone
    return "Contact added successfully."


@input_error
def change_contact(name, phone):
    if name in contacts:
        contacts[name] = phone
        return "Phone number updated successfully."
    else:
        raise KeyError


@input_error
def get_phone_number(name):
    return f"The phone number for {name} is {contacts[name]}."


@input_error
def show_all_contacts():
    if not contacts:
        return "No contacts found."
    output = "Contacts:\n"
    for name, phone in contacts.items():
        output += f"{name}: {phone}\n"
    return output.strip()


def main():
    print(hello())
    while True:
        try:
            user_input = input("> ").lower().strip()
            if user_input in ["good bye", "close", "exit"]:
                print("Good bye!")
                break
            elif user_input == "/start":
                print(hello())
            elif user_input == "hello":
                print(hello())
            elif user_input.startswith("add"):
                command_parts = user_input.split(" ")
                if len(command_parts) == 3:
                    _, name, phone = command_parts
                    print(add_contact(name, phone))
                else:
                    raise ValueError
            elif user_input.startswith("change"):
                command_parts = user_input.split(" ")
                if len(command_parts) == 3:
                    _, name, phone = command_parts
                    print(change_contact(name, phone))
                else:
                    raise ValueError
            elif user_input.startswith("phone"):
                command_parts = user_input.split(" ")
                if len(command_parts) == 2:
                    _, name = command_parts
                    print(get_phone_number(name))
                else:
                    raise ValueError
            elif user_input == "show all":
                print(show_all_contacts())
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

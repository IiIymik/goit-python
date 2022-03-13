from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class Phone(Field):
    pass


class Name(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone):
        self.name = name
        self.phones = []
        self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        for el in self.phones:
            if phone == el.value:
                self.phones.remove(el)
                return
        print("Error number")

    def change_phone(self, old_phone, new_phone):
        for number in self.phones:
            print(number)
            if old_phone == number.value:
                new_phone = Phone(new_phone)
                self.phones.remove(number)
                self.add_phone(new_phone)
                return
        print("Error number")

    def __str__(self):
        return f'Name: {self.name} Phones: {", ".join([str(p) for p in self.phones if str(p) != ""])}'


class AddressBook(UserDict):

    def add_record(self, args):
        for contact_name in self.data:
            if args.name == contact_name:
                return print("Contact exist")
        self.data[args.name] = args

    def __str__(self):
        result = "\n".join([str(v) for v in self.data.values()])
        return result


def input_error(func):
    def verification(args):
        try:
            user_command = [args.split(" ")[0].lower()]
            user_info = args.split(" ")[1:]
            for el in user_info:
                user_command.append(el)
            if len(user_info) < 2:
                user_command.append("")
            verification_result = func(user_command)
            return verification_result
        except KeyError:
            print("Invalid command please try again!")
        except TypeError:
            print("Invalid command please try again!")
        except IndexError:
            print("Invalid command please try again!")
        except ValueError:
            print("Invalid command please try again!")

    return verification


CONTACT = AddressBook()


@input_error
def handler(commands):

    def new_user():
        record = Record(Name(commands[1]), Phone(commands[2]))
        CONTACT.add_record(record)

    def change():
        for name in CONTACT:
            if str(name) == commands[1]:
                new_phone = commands[3]
                old_phone = commands[2]
                CONTACT.data[name].change_phone(old_phone, new_phone)
                return
        print("Error name")

    def hello():
        print("Hello can I help you?")

    def show_all():
        print(CONTACT)

    def delete_number():
        for name in CONTACT:
            print(str(name) == commands[1])
            print(commands[2])
            if str(name) == commands[1]:
                CONTACT.data[name].delete_phone(commands[2])
                return
        print("Error name")

    def add_more_number():
        for name in CONTACT:
            if str(name) == commands[1]:
                CONTACT.data[name].add_phone(Phone(commands[2]))
                return
        print("Error name")

    COMMAND = {
        "hello": hello,
        "add": new_user,
        "show": show_all,
        "delete": delete_number,
        "more": add_more_number,
        "change": change
    }[commands[0]]()

    return


def main():
    print("You are Wellcome!")
    while True:
        user_input = input('==> ')
        if user_input in ["exit", "close", "good bye", "."]:
            break
        handler(user_input)
    print("Good bye!")


if __name__ == "__main__":
    main()

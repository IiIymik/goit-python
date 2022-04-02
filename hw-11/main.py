from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    def __repr__(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value


class Phone(Field):

    @property
    def values(self):
        return self._value

    @values.setter
    def values(self, new_value):
        if len(list(new_value)) >= 9:
            self._value = new_value
        else:
            print('Only 9+ numbers! Number is not add!')
            return


class Name(Field):

    @property
    def values(self):
        return self._value

    @values.setter
    def values(self, new_value):
        if len(list(new_value)) > 0:
            user_name = []
            for el in new_value.split(" "):
                user_name.append(el.capitalize())
            self._value = " ".join(user_name)
        else:
            print("More than one character! Try again")
            return


class Birthday(Field):

    @property
    def values(self):
        return self._value

    @values.setter
    def values(self, new_value):
        if len(list(new_value)) == 10 and int(new_value[0:4]) > 0 and int(new_value[5:7]) > 0 and int(
                new_value[8:10]) > 0:
            self._value = new_value
        else:
            print('Incorect data format! Data is not add')
            self._value = "Not found"
            return


class Record:
    def __init__(self, name: Name, phone: Phone, birthday=None):
        self.name = name
        self.phones = []  # спиисок экземпляр класа Phone
        self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday._value != "Not found":
            today = datetime.today()
            birthday = datetime.strptime(str(self.birthday), '%Y-%m-%d')
            current_year = datetime(year=today.year, month=birthday.month, day=birthday.day + 1)
            result = current_year - today
            if result.days == 0:
                return print(f'Birthday {self.name} Today!!!')
            elif result.days < 0:
                result = datetime(year=today.year + 1, month=birthday.month, day=birthday.day) - today
                return print(f'Days to br:{result.days}')
            else:
                return print(f'Days to birthday {self.name}: {result.days}')
        else:
            print("Birthday not found")

    def delete_phone(self, phone):
        for el in self.phones:
            if phone == el._value:
                self.phones.remove(el)
                return
        print("Error number")

    def change_phone(self, phone, new_phone: Phone):
        if new_phone._value == "":
            return
        for el in self.phones:
            if phone == el._value:
                self.add_phone(new_phone)
                self.phones.remove(el)
                return
        print("Error number")

    def __str__(self):
        return f'Name: {self.name} Phones: {", ".join([str(p) for p in self.phones if str(p) != ""])} Birthday: {self.birthday}'


class AddressBook(UserDict):

    def add_record(self, args):
        for contact_name in self.data:
            if args.name == contact_name:
                return print("Контакт з таким іменем вже існує")
        self.data[args.name] = args

    def iterator(self):
        def it():
            iter = 0
            result = [str(v) for v in self.data.values()]
            while len(result) >= iter:
                default = iter
                iter += int(input("Enter'[number]' for see more next records or press 'e' for exit: "))
                yield "\n".join(result[default:iter])
        all_contact = it()
        while True:
            print(next(all_contact))

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
            if len(user_info) <= 2:
                user_command.append("")
                user_command.append("")
            verification_result = func(user_command)
            return verification_result
        except KeyError:
            print("Invalid command please try again!KeyError")
        except TypeError:
            print("Invalid command please try again!TypeError")
        except IndexError:
            print("Invalid command please try again!IndexError")
        except ValueError:
            print("Exit")
        except StopIteration:
            print("No more contacts")

    return verification


CONTACT = AddressBook()


@input_error
def handler(commands):
    def new_user():
        phon = Phone("")
        phon.values = commands[2]
        birthdays = Birthday("")
        birthdays.values = commands[3]
        name = Name("")
        name.values = commands[1]
        record = Record(name, phon, birthdays)
        CONTACT.add_record(record)

    def change():
        for name in CONTACT:
            if str(name) == commands[1]:
                phon = Phone("")
                phon.values = commands[3]
                CONTACT.data[name].change_phone(commands[2], phon)
                return
        print("Error name")

    def birthday():
        for name in CONTACT:
            if str(name) == commands[1]:
                CONTACT.data[name].days_to_birthday()
                return
        print("Error name")

    def hello():
        print("Hello can I help you?")

    def show_all():
        print(CONTACT)

    def delete_number():
        for name in CONTACT:
            if str(name) == commands[1]:
                CONTACT.data[name].delete_phone(commands[2])
                return
        print("Error name")

    def pages_look():
        CONTACT.iterator()

    def add_more_number():
        for name in CONTACT:
            if str(name) == commands[1]:
                phon = Phone("")
                phon.values = commands[2]
                CONTACT.data[name].add_phone(phon)
                return
        print("Error name")


    COMMAND = {
        "hello": hello,
        "add": new_user,
        "show": show_all,
        "delete": delete_number,
        "more": add_more_number,
        "pages": pages_look,
        "birthday": birthday,
        "change": change
    }[commands[0]]()
    return


def main():
    print("Wellcom\n")
    while True:
        user_input = input('==> ')
        if user_input in ["exit", "close", "good bye", '.']:
            break
        handler(user_input)
    print("\nGood bye!")


if __name__ == "__main__":
    main()
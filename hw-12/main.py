from collections import UserDict
from datetime import datetime
import pickle
import json


class Field:
    def __init__(self, value="") -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class Phone(Field):

    @property
    def values(self):
        return self.value

    @values.setter
    def values(self, new_value):
        if len(list(new_value)) >= 9:
            self.value = new_value
        else:
            print('Only 9+ numbers! Number is not add!')
            return


class Name(Field):
    pass


class Birthday(Field):

    @property
    def values(self):
        return self.value

    @values.setter
    def values(self, new_value):
        if len(list(new_value)) == 10 and \
                int(new_value[0:4]) > 0 and \
                int(new_value[5:7]) > 0 and \
                int(new_value[8:10]) > 0:
            self.value = new_value
        else:
            print('Incorect data format!Need format yyyy-mm-dd. Data is not add')
            self.value = "Not found"
            return


class Record:

    def __init__(self, name: Name, phone: Phone, birthday=None) -> None:
        self.name = name
        self.phones = []
        self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday.value != "Not found":
            today = datetime.today()
            birthday = datetime.strptime(str(self.birthday), '%Y-%m-%d')
            current_year = datetime(year=today.year, month=birthday.month, day=birthday.day + 1)
            result = current_year - today
            if result.days == 0:
                return print(f'Birthday {self.name} Today!!!')
            elif result.days < 0:
                result = datetime(year=today.year + 1, month=birthday.month, day=birthday.day) - today
                return print(f'Days to birthday {self.name} :{result.days}')
            else:
                return print(f'Days to birthday {self.name}: {result.days}')
        else:
            print("Birthday not found")

    def delete_phone(self, phone: Phone):
        for contact_phone in self.phones:
            if phone == contact_phone.value:
                self.phones.remove(contact_phone)
                return
        print("Error number")

    def change_phone(self, phone: Phone, new_phone: Phone):
        if new_phone.value == "":
            return
        for contact_phone in self.phones:
            if phone == contact_phone.value:
                self.add_phone(new_phone)
                self.phones.remove(contact_phone)
                return
        print("Error number")

    def __str__(self) -> str:
        return f'Name: {self.name} Phones: {", ".join([str(p) for p in self.phones if str(p) != ""])} Birthday: {self.birthday}'


class AddressBook(UserDict):
    
    def add_record(self, args):
        for contact_name in self.data:
            if args.name == contact_name:
                return print("Сontact with this name exists")
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

    def find(self,item):
        result = [str(v) for v in self.data.values() if item in str(v)]
        print("\n".join(result))

    def __str__(self) -> str:
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


#file open or create new
try:
    file = open('contact_book.dat', 'rb')
    CONTACT = pickle.load(file)
    file.close()
except FileNotFoundError:
    CONTACT = AddressBook()

@input_error
def handler(commands):
    def new_user():
        phon = Phone()
        phon.values = commands[2]
        birthdays = Birthday()
        birthdays.values = commands[3]
        record = Record(Name(commands[1]), phon, birthdays)
        CONTACT.add_record(record)

    def add_more_number():
        for name in CONTACT:
            if str(name) == commands[1]:
                phon = Phone()
                phon.values = commands[2]
                CONTACT.data[name].add_phone(phon)
                return
        print("Error name")

    def change():
        for name in CONTACT:
            if str(name) == commands[1]:
                phon = Phone()
                phon.values = commands[3]
                CONTACT.data[name].change_phone(commands[2], phon)
                return
        print("Error name")

    def delete_number():
        for name in CONTACT:
            if str(name) == commands[1]:
                CONTACT.data[name].delete_phone(commands[2])
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

    def pages_look():
        CONTACT.iterator()

    def find():
        CONTACT.find(commands[1])

    COMMAND = {
        "find": find,
        "hello": hello,
        "add": new_user,
        "show": show_all,
        "change": change,
        "pages": pages_look,
        "birthday": birthday,
        "delete": delete_number,
        "more": add_more_number
    }[commands[0]]()
    return
    
    
def main():
    print("You are Wellcome!")
    while True:
        user_input = input('==>> ')
        if user_input in ["exit", "close", "good bye", '.']:
            file_dump = open('contact_book.dat', 'wb')
            pickle.dump(CONTACT, file_dump)
            file_dump.close()
            print('Save in contact_book.dat')
            break
        handler(user_input)
    print("\nGood bye!")


if __name__ == "__main__":
    main()
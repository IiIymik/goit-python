from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import os.path
import pickle
import re
from . import clean

# --------------------------------Prompt Toolkit-------------------------------
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter([
    'add', 'close', 'exit', 'save', 'remove', 'add address', 'add birthday', 'add email', 'add phone',
    'delete address', 'delete birthday', 'delete email', 'delete phone',
    'change email', 'change birthday', 'change address', 'change phone',
    'coming birthday', 'good bye', "add note", "find note", "change note",
    "delete note", "tag note", "help", 'show all', 'search', 'clean'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})
# --------------------------------Prompt Toolkit-------------------------------


class CustomException(Exception):
    def __init__(self, text):
        self.txt = text


class AddressBook(UserDict):

    def get_values_list(self):
        if self.data:
            return self.data.values()
        else:
            raise CustomException('Address book is empty.')

    def get_record(self, name):
        if self.data.get(name):
            return self.data.get(name)
        else:
            raise CustomException(
                'Such contacts doesn\'t exist.')

    def remove(self, name):
        if self.data.get(name):
            self.data.pop(name)
        else:
            raise CustomException(
                'Such contact  doesn\'t exist.')

    def load_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as fh:
                self.data = pickle.load(fh)
                if len(self.data):
                    return f'The contacts book is loaded from the file "{file_name}".'
                else:
                    return "This is empty contacts book. Add contacts to it using the command 'add < NAME > '."
        else:
            return "This is empty contacts book. Add contacts into it using the command 'add <NAME>'."

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)
        return f'The contacts book is saved in the file "{file_name}".'

    def search(self, query):
        result = AddressBook()
        for key in self.data.keys():
            if query.lower() in str(self.get_record(key)).lower():
                match = self.get_record(key)
                result[key] = match
        if len(result) > 0:
            return f'{len(result)} records found:\n {result}'
        else:
            return f'No records found.'

    def __repr__(self):
        result = ""
        for key in self.data.keys():
            result += str(self.data.get(key))
        return result


contacts = AddressBook()


class Record:

    def __init__(self, name, address=None, phones_list=None, email=None, birthday=None):
        self.name = name
        self._address = address
        self._phones_list = []
        self._email = email
        self._birthday = birthday

    def append_phone(self, phone):
        if re.search('\(0\d{2}\)\d{3}-\d{2}-\d{2}', phone):
            self._phones_list.append(phone)
        else:
            raise CustomException(
                'Wrong phone number format! Use (0XX)XXX-XX-XX format!')

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    def delete_address(self):
        self._address = None

    @property
    def phones_list(self):
        return self._phones_list

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if re.search('[a-zA-Z][\w.]+@[a-zA-z]+\.[a-zA-Z]{2,}', email):
            self._email = email
        else:
            raise CustomException(
                'Wrong email format! Correct format is aaaa@ddd.cc')

    def delete_email(self):
        self._email = None

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        if re.search('\d{2}\.\d{2}.\d{4}', birthday) and datetime.strptime(birthday, '%d.%m.%Y'):
            self._birthday = birthday
        else:
            raise CustomException(
                'Wrong date format! Correct format is DD.MM.YYYY')

    def delete_birthday(self):
        self._birthday = None

    def __repr__(self):
        name = self.name
        email = '---' if self.email == None else self.email
        address = '---' if self.address == None else self.address
        birthday = '---' if self.birthday == None else self.birthday
        if len(self.phones_list) == 0:
            phones = '---'
        else:
            phones = ', '.join(self.phones_list)
        return f'\n┌{"-" * 108}┐\n| {name:<51} Phones: {phones:<46} |\
                 \n| Email: {email:<73} Date of birth: {birthday:<10} |\
                 \n| Address: {address:<97} |\n└{"-" * 108}┘\n'


def input_error(func):

    def inner(command_line):

        try:
            result = func(command_line)

        except CustomException as warning_text:
            result = warning_text

        except Exception as exc:

            if func.__name__ == 'save_func':
                result = f'Error while saving.'
            elif func.__name__ == 'add_birthday':
                result = "Day out of range for this month."
            elif func.__name__ == 'coming_birthday' and exc.__class__.__name__ == "ValueError":
                result = "Use a number for getting list of birthdays more than next 7 days."
            elif func.__name__ == 'remove':
                result = f'Error while removing record.'
            elif func.__name__ == 'change_address':
                result = f'Error while changing address.'
            elif func.__name__ == 'change_birthday':
                result = f'Error while changing birthday.'
            elif func.__name__ == 'change_email':
                result = f'Error while changing email.'
            elif func.__name__ == 'change_phone':
                result = f'Error while changing phone.'
            elif func.__name__ == 'delete_address':
                result = f'Error while deleting address.'
            elif func.__name__ == 'delete_birthday':
                result = f'Error while deleting birthday.'
            elif func.__name__ == 'delete_email':
                result = f'Error while deleting email.'
            elif func.__name__ == 'delete_phone':
                result = f'Error while deleting phone.'
            elif func.__name__ == 'search':
                result = f'Error while searching.'
            elif func.__name__ == 'clean_func':
                result = f'Error while cleaning the folder.'

        return result

    return inner


@input_error
def exit_func(command_line):

    return 'Good bye!'


@input_error
def save_func(command_line):

    return contacts.save_to_file('contacts.bin')


def prepare_value(command_line):
    if command_line:
        value = command_line.pop(-1)
        key = ' '.join(command_line)
        return key, value
    else:
        raise CustomException(
            'The command must be with INFORMATION you want to add or change (Format: <command> <name> <information>).')


def prepare_value_3(command_line):
    if command_line:
        key = ' '.join(command_line)
        value = input('Enter the address >>> ')
        return key, value
    else:
        raise CustomException(
            'The command must be in the format: <command> <name>.')


@input_error
def add_name(command_line):
    if command_line:
        name = ' '.join(command_line)
        if name in contacts.keys():
            raise CustomException(
                f'Contact with name "{name}" has been already added!')
        else:
            record = Record(name)
            contacts[name] = record
            return f'Contact with the name "{name}" has been successfully added.'
    else:
        raise CustomException(
            'The command must be with a NAME you want to add (Format: <add> <name>).')


@input_error
def add_address(command_line):
    key, address = prepare_value_3(command_line)
    contacts.get_record(key).address = address
    return f'Address {address} for the contact "{key}" has been successfully added.'


@input_error
def add_birthday(command_line):
    key, birthday = prepare_value(command_line)
    contacts.get_record(key).birthday = birthday
    return f'Date of birth {birthday} for the contact "{key}" has been successfully added.'


@input_error
def add_email(command_line):
    key, email = prepare_value(command_line)
    contacts.get_record(key).email = email
    return f'Email {email} for the contact "{key}" has been successfully added.'


@input_error
def add_phone(command_line):
    key, phone = prepare_value(command_line)
    if not phone in contacts.get_record(key).phones_list:
        contacts.get_record(key).append_phone(phone)
        return f'Phone number {phone} for the contact "{key}" has been successfully added.'
    else:
        raise CustomException('Such phone number has been already added!')


def create_for_print(birthdays_dict):
    to_show = []
    for date, names in list(birthdays_dict.items()):
        to_show.append(
            f'{date.strftime("%A")}({date.strftime("%d.%m.%Y")}): {", ".join(names)}')
    if len(to_show) == 0:
        return f'There are no birthdays coming within this period.'
    else:
        return "\n".join(to_show)


@input_error
# можно задать другой диапазон вывода дней, по умолчанию 7
def coming_birthday(command_line):
    range_days = 7
    birthdays_dict = defaultdict(list)
    if command_line:
        range_days = int(command_line[0])
    current_date = datetime.now().date()
    timedelta_filter = timedelta(days=range_days)
    for name, birthday in [(i.name, i.birthday) for i in contacts.get_values_list()]:
        if name and birthday:  # проверка на None
            birthday_date = datetime.strptime(birthday, '%d.%m.%Y').date()
            current_birthday = birthday_date.replace(year=current_date.year)
            if current_date <= current_birthday <= current_date + timedelta_filter:
                birthdays_dict[current_birthday].append(name)
    return create_for_print(birthdays_dict)


@input_error
def search(command_line):
    #key, value = prepare_value(command_line)
    if command_line:
        return contacts.search(' '.join(command_line).strip())
    else:
        return 'Specify the search string.'


@input_error
def remove(command_line):
    key = ' '.join(command_line).strip()
    if contacts.get_record(key):
        contacts.remove(key)
        return f'Contact "{key}" has been successfully removed.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_address(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        address = contacts.get_record(key).address
        contacts.get_record(key).delete_address()
        return f'Address "{address}" for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_birthday(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        birthday = contacts.get_record(key).birthday
        contacts.get_record(key).delete_birthday()
        return f'Date of birth {birthday} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_email(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        email = contacts.get_record(key).email
        contacts.get_record(key).delete_email()
        return f'Email {email} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_phone(command_line):
    key, phone = prepare_value(command_line)
    if phone in contacts.get_record(key).phones_list:
        ix = contacts.get_record(key).phones_list.index(phone)
        if ix >= 0:
            contacts.get_record(key).phones_list.pop(ix)
        return f'Phone number {phone} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such phone number does not exist!!!')


@input_error
def change_email(command_line):
    key, email = prepare_value(command_line)
    if key in contacts.keys():
        contacts.get_record(key).email = email
        return f'Email for "{key}" has been successfully changed to {email}.'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist or you have not specified new email!!!')


@input_error
def change_birthday(command_line):
    key, birthday = prepare_value(command_line)
    if key in contacts.keys():
        contacts.get_record(key).birthday = birthday
        return f'Date of birth for "{key}" has been successfully changed to {birthday}.'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist or you have not specified new date of birth!!!')


@input_error
def change_address(command_line):
    key, address = prepare_value_3(command_line)
    if key in contacts.keys():
        contacts.get_record(key).address = address
        return f'Address for the contact "{key}" has been successfully changed to "{address}".'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist!')


@input_error
def change_phone(command_line):
    phones = [command_line.pop(-1)]
    phones.insert(0, command_line.pop(-1))
    key = ' '.join(command_line).strip()
    if key not in contacts.keys():
        return f'Wrong name "{key}" or you have not specified the new phone number.'
    if len(phones) != 2:
        raise CustomException(
            '''The command must be with a NAME and 2 phones you want to change 
            (Format: <change> <name> <old phone> <new phone>)''')
    if re.search('\(0\d{2}\)\d{3}-\d{2}-\d{2}', phones[1]):
        if phones[0] in contacts.get_record(key).phones_list:
            ix = contacts.get_record(key).phones_list.index(phones[0])
            if ix >= 0:
                contacts.get_record(key).phones_list[ix] = phones[1]
            return f'Phone number for "{key}" has been successfully changed to {phones[1]}.'
        else:
            raise CustomException(
                f'Phone number {phones[0]} does not exist!!!')
    else:
        raise CustomException(
            'Wrong phone number format. Use (0XX)XXX-XX-XX format!')

 # блок кода касающийся заметок###########


@input_error
def add_note(command_line):
    """ Сама структура заметок это обычный текстовый файл, каждая строка
        которого это есть одна заметка
        В качестве идентификатора выступет дата и время создания заметки,
        приведенные к строковому виду - чтобы файл можно было открывать
        обычным текстовым редактором. Далее этот идентификатор используется
        для индексации по заметкам (редактирование, удаление, поиск)
    """
    note = ' '.join(command_line)
    current_id = datetime.now()
    # преобразовали в строку дату время создания
    crt = current_id.strftime("%d.%m.%Y - %H:%M:%S")
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "a+") as file:
        file.write(crt+" :: "+note+"\n")  # первые 21 символ - строка
    return "The note is added."


@input_error
def find_note(command_line):
    """ Поиск задается по трем переменным
        ключевое слово - без этого слова заметка не интересует
        дата старта - ранее этой даты заметки не интересуют
        дата конца - позже этой даты заметки не интересуют

        сейчас ограничиваем поиск датами, но не временем. Исключительно для удобства пользователя
        после вывода массива заметок он найдет интересующую, скопирует ее полный идентификатор и перейдет к ней
        непосредственно, если нужно
    """
    # разбираем команду в формат (keyword:str, start:'start date' = '', end:'end_date' = ''):
    if len(command_line) >= 3:
        keyword = command_line[0].lower()
        start = command_line[1]
        end = command_line[2]
    elif len(command_line) == 2:
        keyword = command_line[0].lower()
        start = command_line[1]
        end = ''
    elif len(command_line) == 1:
        keyword = command_line[0].lower()
        start = ''
        end = ''
    else:
        keyword = ''
        start = ''
        end = ''

    try:
        start_date = datetime.strptime(start, "%d.%m.%Y")
    except:
        print("Search start date is not stated in the DD.MM.YYYY format. The search will be performed from the first note.")
        # начало поиска с даты начала Эпохи
        start_date = datetime.strptime("01.01.1970", "%d.%m.%Y")

    try:
        end_date = datetime.strptime(end, "%d.%m.%Y")
    except:
        print("Search end date is not stated in the DD.MM.YYYY format. The search will be performed till the last note.")
        end_date = datetime.now()   # конец поиска до текущего момента

    if (type(keyword) == str) and (keyword != ''):
        pass
    else:
        print("The keyword is not stated. The search will be performed for all notes.")

    with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "r+") as file:
        lines = file.readlines()  # список строк из файла заметок

    msg = "No one note is found."
    for i in lines:
        date_id = i[:10]  # вырезали кусок строки - дата создание заметки
        # конверт в объект, чтобы сравнивать
        n_id = datetime.strptime(date_id, "%d.%m.%Y")
        if (n_id >= start_date) and (n_id <= end_date):
            if (type(keyword) == str) and (keyword != ''):
                j = i.lower()      # приводим оригинальную строку к нижнеему регистру
                # если есть ключ(нижний регистр) в строке (нижний регистр ) выводим оригинальную
                if keyword in j:
                    # забили последний символ переноса строки - для красивого вывода
                    print(i[:len(i)-1])
                    msg = "Notes are found."
            else:
                print(i[:len(i)-1])  # выводим все строки - нет ключа
                msg = "Notes are found."
    return msg


@input_error
def change_note(command_line):
    """Для изменения заметки нужно дать аргументом ее полный идентификатор со временем,
       его удобно скопировать после общего поиска
       а также данные которые должны быть записаны в эту заметку с этим же идентификатором

    """
    # разбираем команду в формат (dt_id:"%d.%m.%Y - %H:%M:%S" = '', data:str = '')
    if len(command_line) >= 4:
        dt_id = command_line[0]+' '+command_line[1]+' '+command_line[2]
        command_line.pop(0)
        command_line.pop(0)
        command_line.pop(0)
        data = ' '.join(command_line)
    elif len(command_line) == 3:
        dt_id = command_line[0]+command_line[1]+command_line[2]
        data = ''
    else:
        dt_id = ''
        data = ''

    msg = "No one note is changed."
    try:
        # проверка что идентификатор задан в формате
        loc_id = datetime.strptime(dt_id, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "r") as file:
                buffer = file.readlines()
            for i in range(len(buffer)):
                d_id = buffer[i][:21]  # полный идентификатор
                n_id = datetime.strptime(d_id, "%d.%m.%Y - %H:%M:%S")
                if n_id == loc_id:  # совпадение текущего ид с заданным
                    if data != '':
                        # замена строки, идентификатор остается
                        buffer[i] = d_id+" :: "+data+"\n"
                        msg = "The note is changed"
                        break
                    else:
                        in_q = input(
                            "The field for change is empty. Are you sure? y or n")
                        if in_q == 'y':
                            # замена строки, идентификатор остается
                            buffer[i] = d_id+" :: "+data+"\n"
                            msg = "The note is changed"
                        break
            # удаляем содержимое старого файла, пишем заново
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "w") as file:
                file.writelines(buffer)  # пишем построчно из буфера
        except:
            print("ID selection error. Maybe the reason is manual file editing.")

    except:
        print("The ID is not in the DD.MM.YYYY - hh.mm.ss format. Copy ID from the search results.")
    return msg


@input_error
def delete_note(command_line):
    """Для удаления заметки нужно дать аргументом ее полный идентификатор со временем,
       его удобно скопировать после общего поиска - вместе с кавычками
    """
    # разбираем команду в формат (dt_id:"%d.%m.%Y - %H:%M:%S" = '')
    if len(command_line) == 3:
        dt_id = command_line[0]+' '+command_line[1]+' '+command_line[2]
    else:
        dt_id = ''

    msg = "No one note is deleted"
    try:
        # проверка что идентификатор задан в формате
        loc_id = datetime.strptime(dt_id, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "r") as file:
                buffer = file.readlines()
            for i in range(len(buffer)):
                d_id = buffer[i][:21]  # полный идентификатор
                n_id = datetime.strptime(d_id, "%d.%m.%Y - %H:%M:%S")
                if n_id == loc_id:  # совпадение текущего ид с заданным
                    buffer.pop(i)
                    msg = "The note is deleted"
                    break
            # удаляем содержимое старого файла, пишем заново
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "w") as file:
                file.writelines(buffer)  # пишем построчно из буфера
        except:
            print("ID selection error. Maybe the reason is manual file editing.")

    except:
        print("The ID is not in the DD.MM.YYYY - hh.mm.ss format. Copy ID from the search results.")
    return msg


@input_error
def tag_note(command_line):
    """Привязка тега к заметке, далее поиск с хештегом осуществляется
       обычной командой find note #....
    """
    # разбираем команду в формат (dt_id:"%d.%m.%Y - %H:%M:%S" = '', tag:str = '')
    if len(command_line) >= 4:
        dt_id = command_line[0] + ' ' + command_line[1] + ' ' + command_line[2]
        tag = command_line[3]
    elif len(command_line) == 3:
        dt_id = command_line[0] + command_line[1] + command_line[2]
        tag = ''
    else:
        dt_id = ''
        tag = ''

    msg = "The hashtag is not acceptable."
    try:
        # проверка что идентификатор задан в формате
        loc_id = datetime.strptime(dt_id, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "r") as file:
                buffer = file.readlines()
            for i in range(len(buffer)):
                d_id = buffer[i][:21]  # полный идентификатор
                n_id = datetime.strptime(d_id, "%d.%m.%Y - %H:%M:%S")
                if n_id == loc_id:  # совпадение текущего ид с заданным
                    if tag != '':
                        # забили перенос строки, добавили хештег и перенос
                        j = buffer[i][:len(buffer[i])-1] + '  #' + tag + '\n'
                        # строка неизменяема, нельзя сразу писать buffer[i] = buffer[i] + tag
                        buffer[i] = j
                        msg = "The hashtag is accepted."
                        break
                    else:
                        in_q = input("The tag is empty. Are you sure? y or n")
                        if in_q == 'y':
                            # забили перенос строки, добавили хештег и перенос
                            j = buffer[i][:len(buffer[i])-1] + \
                                '  #' + tag + '\n'
                            # строка неизменяема, нельзя сразу писать buffer[i] = buffer[i] + tag
                            buffer[i] = j
                            msg = "The hashtag is accepted."
                        break
            # удаляем содержимое старого файла, пишем заново
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", "w") as file:
                file.writelines(buffer)  # пишем построчно из буфера
        except:
            print("ID selection error. Maybe the reason is manual file editing.")

    except:
        print("The ID is not in the DD.MM.YYYY - hh.mm.ss format. Copy ID from the search results.")
    return msg


@input_error
def help_common(command_line):

    try:
        file = open(
            f"{os.path.dirname(os.path.abspath(__file__))}/help.txt", 'r')
        help_lines = file.readlines()
        for i in help_lines:
            # забили последний символ переноса строки - для красивого вывода
            print(i[:len(i)-1])
        file.close()
        msg = "The end of the help."
    except:
        msg = "File help.txt is not found."
    return msg


def start_note():  # проверка что файл существует или его создание

    try:
        file = open(
            f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", 'r')
        print("File note.txt with notes is loaded.")
    except:
        # создаем новый
        file = open(
            f"{os.path.dirname(os.path.abspath(__file__))}/note.txt", 'w')
        print("File note.txt with notes is created.")
    finally:
        file.close()


@input_error
def show_all(command_line):

    if len(contacts.items()) > 0:
        return str(contacts)
    else:
        return 'There are no contacts in the book.'


@input_error
def clean_func(command_line):
    return clean.start_cleaning(command_line)


COMMANDS = {
    'close': exit_func,
    'exit': exit_func,
    'good bye': exit_func,
    'save': save_func,
    'add': add_name,
    'add address': add_address,
    'add birthday': add_birthday,
    'add email': add_email,
    'add phone': add_phone,
    'remove': remove,
    'delete address': delete_address,
    'delete birthday': delete_birthday,
    'delete email': delete_email,
    'delete phone': delete_phone,
    'change email': change_email,
    'change birthday': change_birthday,
    'change address': change_address,
    'change phone': change_phone,
    'coming birthday': coming_birthday,
    "add note": add_note,
    "find note": find_note,
    "change note": change_note,
    "delete note": delete_note,
    "tag note": tag_note,
    "help": help_common,
    'show all': show_all,
    'search': search,
    'clean': clean_func
}

ONE_WORD_COMMANDS = ['add', 'clean', 'close', "help",
                     'exit', 'save', 'remove', 'search']
TWO_WORDS_COMMANDS = ['add address', 'add birthday', 'add email', 'add phone',
                      'delete address', 'delete birthday', 'delete email', 'delete phone',
                      'change email', 'change birthday', 'change address', 'change phone',
                      'coming birthday', 'good bye', "add note", "find note", "change note",
                      "delete note", "tag note", 'show all']


def get_handler(command):
    return COMMANDS[command]


def main():

    print("Enter 'help' command to see all the commands available.")
    start_note()
    print(contacts.load_from_file(
        f"{os.path.dirname(os.path.abspath(__file__))}/contacts.bin"))

    while True:
        command_line = []
        while not command_line:
            command_line = prompt('>>> ',
                                  history=FileHistory('history'),
                                  auto_suggest=AutoSuggestFromHistory(),
                                  completer=SqlCompleter,
                                  style=style
                                  ).split()

        right_command = False

        if len(command_line) > 1 and \
           f'{command_line[0].lower()} {command_line[1].lower()}' in TWO_WORDS_COMMANDS:
            command = f'{command_line.pop(0).lower()} {command_line.pop(0).lower()}'
            right_command = True

        if not right_command:
            command = command_line.pop(0).lower()
            right_command = command in ONE_WORD_COMMANDS

        if not right_command:
            print(
                f'The "{command}" command is wrong! The allowable commands are {", ".join(ONE_WORD_COMMANDS + TWO_WORDS_COMMANDS)}.')
            continue

        handler = get_handler(command)
        print(handler(command_line))
        if handler is exit_func:
            print(contacts.save_to_file(
                f"{os.path.dirname(os.path.abspath(__file__))}/contacts.bin"))
            break


if __name__ == '__main__':
    main()

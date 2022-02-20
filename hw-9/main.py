def bot_assistant():
    while True:
        try:
            answer = input('==> ').lower().strip()
            if answer in exit_answer:
                return print_answer(f"{exit_answer[3].capitalize()}!")
            elif answer.startswith(OPERATIONS[0]):
                add_contact(answer)
            elif answer.startswith(OPERATIONS[1]):
                change_contact(answer)
            elif answer.startswith(OPERATIONS[2]):
                show_contact(answer)
            elif answer.startswith(OPERATIONS[3]):
                print_answer()
            elif answer.startswith(OPERATIONS[4]):
                show_phone_book(answer)
        except KeyboardInterrupt:
            return print_answer(f"{exit_answer[3].capitalize()}!")


def print_answer(txt='How can I help you?'):
    print(txt)


def input_error(func):
    def inner(s):
        try:
            func(s)
        except (KeyError, ValueError, IndexError, KeyboardInterrupt):
            if KeyError or ValueError or IndexError:
                print_answer('Write correct value:')

    return inner


@input_error
def add_contact(arr):
    _, name, phone = arr.split(' ')
    phone_book.update({name: phone})


@input_error
def change_contact(arr):
    _, name = arr.split(' ')
    if phone_book.get(name):
        answer = input('new phone number =>> ')
        phone_book.update({name: answer})
    else:
        print(f"Sorry,{name} can't find")


@input_error
def show_phone_book(_):
    phoneBook = ''
    for k, v in phone_book.items():
        phoneBook += '| {name}: {value}'.format(name=k, value=v)

    print_answer(phoneBook)


@input_error
def show_contact(arr):
    _, name = arr.split(' ')
    print_answer(phone_book.get(name))


OPERATIONS = [
    'add',
    'change',
    'phone',
    'hello',
    'show all'
]
exit_answer = ['.', 'close', 'exit', 'good bye']
phone_book = {}

if __name__ == '__main__':
    bot_assistant()

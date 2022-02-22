def bot_assistant():
    while True:
        try:
            answer = input('==> ').lower().strip()
            command, *args = answer.split(' ')
            if answer in exit_answer:
                return print_answer(f"{exit_answer[3].capitalize()}!")
            elif answer.startswith(OPERATIONS[0]):
                new_contact = add_contact(args)
                if new_contact:
                    print_answer(new_contact)
                else:
                    pass
            elif answer.startswith(OPERATIONS[1]):
                update_contact = change_contact(args)
                print_answer(update_contact)
            elif answer.startswith(OPERATIONS[2]):
                contact = show_contact(args)
                print_answer(contact)
            elif answer.startswith(OPERATIONS[3]):
                print_answer()
            elif answer.startswith(OPERATIONS[4]):
                book = show_phone_book(answer)
                print_answer(book)
            else:
                print_answer("Sorry, don't know this command. Try again.")
        except KeyboardInterrupt:
            return print_answer(f"{exit_answer[3].capitalize()}!")


def print_answer(txt='How can I help you?'):
    print(txt)


def input_error(func):
    def inner(s):
        try:
            return func(s)
        except KeyError:
            print_answer('Write correct value:')
        except ValueError:
            print_answer('Write correct value:')
        except IndexError:
            print_answer('Write correct value:')

    return inner


@input_error
def add_contact(args):
    phone_book.update({args[0]: args[1]})
    return f'Contact > {args[0].capitalize()} has been added'


@input_error
def change_contact(args):
    if phone_book.get(args[0]):
        answer = input('new phone number =>> ')
        phone_book.update({args[0]: answer})
        return f'Contact > {args[0].capitalize()} has been update'
    else:
        return f"Sorry,{args[0].capitalize()} can't find"


@input_error
def show_phone_book(_):
    phoneBook = ''
    for k, v in phone_book.items():
        phoneBook += '| {name}: {value}'.format(name=k, value=v)

    return phoneBook


@input_error
def show_contact(args):
    return f'{phone_book.get(args[0])}'


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

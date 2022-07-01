from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models import Note, Record, Tag

from personal_helper import *

engine = create_engine("sqlite:///ContactBooks.db")
Session = sessionmaker(bind=engine)
session = Session()




tag1 = Tag(name="продукты")
tag2 = Tag(name="покупки")

note = Note(name="Сбегать в магазин")

note.tags = [tag1, tag2]

rec1 = Record(description="Купить хлеб", note=note)
rec2 = Record(description="Купить колбасу 0.5 кг", note=note)
rec3 = Record(description="Купить помидоры 1кг", note=note)

session.add(note)
session.commit()

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
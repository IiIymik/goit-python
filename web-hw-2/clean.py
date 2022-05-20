import os
import re
import shutil


STANDARD_FOLDERS = ['archives', 'audio', 'documents', 'images', 'video']

FILE_TYPES = {'images': ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP', 'TIF', 'TIFF', 'GIF'),
              'archives': ('ZIP', 'GZ', 'TAR'),
              'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
              'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
              'video':  ('AVI', 'MP4', 'MOV', 'MKV', 'MPG')
              }

files_info = {'images': [], 'archives': [], 'documents': [],
              'audio': [], 'video': [], 'unknown': [], 'known': []}


def create_folder(name):

    if not os.path.exists(name):
        os.mkdir(name)


def create_folders_chain(chain, root, file_type):

    next_folder = ''
    # Просмотр элементов пути для папки назначения
    for folder_part in chain.split('/'):
        if folder_part:
            next_folder += f'/{folder_part}'
            # Создаем вложенную папку по цепочке
            create_folder(fr'{root}/{file_type}{next_folder}')


def normalize(string):

    translit_table = {'а': 'a', 'А': 'A',
                      'б': 'b', 'Б': 'B',
                      'в': 'v', 'В': 'V',
                      'г': 'g', 'Г': 'G',
                      'ґ': 'g', 'Ґ': 'G',
                      'д': 'd', 'Д': 'D',
                      'е': 'e', 'Е': 'E',
                      'ё': 'io', 'Ё': 'Io',
                      'є': 'ye', 'Є': 'Ye',
                      'ж': 'zh', 'Ж': 'Zh',
                      'з': 'z', 'З': 'Z',
                      'и': 'i', 'И': 'I',
                      'й': 'y', 'Й': 'Y',
                      'і': 'i', 'І': 'I',
                      'ї': 'yi', 'Ї': 'Yi',
                      'к': 'k', 'К': 'K',
                      'л': 'l', 'Л': 'L',
                      'м': 'm', 'М': 'M',
                      'н': 'n', 'Н': 'N',
                      'о': 'o', 'О': 'O',
                      'п': 'p', 'П': 'P',
                      'р': 'r', 'Р': 'R',
                      'с': 's', 'С': 'S',
                      'т': 't', 'Т': 'T',
                      'у': 'u', 'У': 'U',
                      'ф': 'f', 'Ф': 'F',
                      'х': 'h', 'Х': 'H',
                      'ц': 'ts', 'Ц': 'Ts',
                      'ч': 'ch', 'Ч': 'Ch',
                      'ш': 'sh', 'Ш': 'Sh',
                      'щ': 'sch', 'Щ': 'Sch',
                      'ъ': '', 'Ъ': '',
                      'ы': 'y', 'Ы': 'Y',
                      'ь': '', 'Ь': '',
                      'э': 'e', 'Э': 'E',
                      'ю': 'iu', 'Ю': 'Iu',
                      'я': 'ia', 'Я': 'Ia'}

    for key in translit_table:
        string = string.replace(key, translit_table[key])

    return re.sub('[^A-Za-z0-9_\./:]', '_', string)


def order_by_ext(file_type, extensions, item, folder, root):

    # Расширение файла
    ext = item[item.rfind(".") + 1:]
    ext_upper = ext.upper()
    normalized_item = normalize(item)
    # Определяем нормализованное имя папки назначения без учета корневой папки
    destination_folder = normalize(folder.replace(root, ''))
    destination_file_path = fr'{root}/{file_type}{destination_folder}/{normalized_item}'
    if ext_upper in extensions:
        files_info[file_type].append(destination_file_path)
        if ext_upper not in files_info['known']:
            files_info['known'].append(ext_upper)
        create_folders_chain(destination_folder, root, file_type)
        shutil.move(fr'{folder}/{item}', destination_file_path)

        if file_type == 'archives':
            archive_folder = normalized_item.removesuffix(f'.{ext}')
            create_folders_chain(
                f'{destination_folder}/{archive_folder}', root, 'archives')
            shutil.unpack_archive(
                destination_file_path, fr'{root}/archives{destination_folder}/{archive_folder}')
            shutil.move(destination_file_path,
                        fr'{root}/archives{destination_folder}/{archive_folder}')
    else:
        files_info['unknown'].append(ext_upper)


def order_files(folder, root):

    # Перебираем элементы в текущей папке
    for item in os.listdir(folder):
        if os.path.isdir(f'{folder}/{item}'):
            if item not in STANDARD_FOLDERS:                                # Если папка не относится к стандартным
                # Рекурсивный просмотр папки
                order_files(f'{folder}/{item}', root)
        else:
            for file_type, extensions in FILE_TYPES.items():
                # Перебираем категории файлов и рассортировываем по стандартным папкам
                order_by_ext(file_type, extensions, item, folder, root)


def remove_empty(folder):

    while True:
        empty_nonstd_folders_count = 0
        tree = os.walk(folder)
        for item in tree:
            if item[1] == [] and item[2] == [] and not item[0].endswith(tuple(STANDARD_FOLDERS)):
                empty_nonstd_folders_count += 1
                os.rmdir(item[0])
        if empty_nonstd_folders_count == 0:
            break


def start_cleaning(command_line):

    global files_info
    if len(command_line) == 0:
        folder_name = ''
    elif os.path.exists(command_line[0]):
        folder_name = command_line[0]
    else:
        folder_name = ''
    print(folder_name)
    if folder_name:
        create_folder(fr'{folder_name}/archives')
        create_folder(fr'{folder_name}/audio')
        create_folder(fr'{folder_name}/documents')
        create_folder(fr'{folder_name}/images')
        create_folder(fr'{folder_name}/video')
        print('Start cleaning...')
        order_files(folder_name, folder_name)
        print('Removing empty folders...')
        remove_empty(folder_name)
        for key, value in files_info.items():
            if key == 'unknown':
                pass
            elif key == 'known':
                pass
            else:
                print('-' * 30)
                print(f'{key}:')
                print('-' * 30)
                for file in value:
                    print(file)
        print('-' * 30)
        print(f'Known extensions: {files_info["known"]}')
        print('-' * 30)
        unknown_set = set(files_info["unknown"]) - set(files_info["known"])
        if len(unknown_set) == 0:
            return_str = f'Unknown extensions: NOT FOUND'
        else:
            return_str = f'Unknown extensions: {set(files_info["unknown"]) - set(files_info["known"])}'

        files_info = {'images': [], 'archives': [], 'documents': [],
                      'audio': [], 'video': [], 'unknown': [], 'known': []}
    elif len(command_line) > 0:
        return_str = f'There is no folder {command_line[0]}.'
    else:
        return_str = 'Specify the folder for cleaning.'

    return return_str

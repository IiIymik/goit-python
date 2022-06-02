import sys
import os
import shutil
from threading import Thread

IMAGES_TYPE = ['jpeg', 'png', 'jpg', 'svg']
VIDEO_TYPE = ['avi', 'mp4', 'mov', 'mkv']
AUDIO_TYPE = ['mp3', 'ogg', 'wav', 'amr']
DOCUMENTS_TYPE = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
ARCHIVES_TYPE = ['zip', 'gz', 'tar']
FOLDER_EXEPTION = ['image', 'video', 'audio', 'documents', 'archives']

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
         "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC, LATIN):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def translate_file(name):
    return name.translate(TRANS)

class SortingThread(Thread):

    def __init__(self, files, base_folder,  root, ):
        super().__init__()
        self.files = files
        self.base_folder = base_folder
        self.root = root

    def run(self):
        
        for name in self.files:

                file_name = name.split('.')
                new_file_name = normalize(file_name[0], file_name[1])
                
                if file_name[1] in IMAGES_TYPE:
                    create_folder_and_replace_file(self.base_folder, FOLDER_EXEPTION[0], self.root, name, new_file_name)
                elif file_name[1] in VIDEO_TYPE:
                    create_folder_and_replace_file(self.base_folder, FOLDER_EXEPTION[1], self.root, name, new_file_name)
                elif file_name[1] in AUDIO_TYPE:
                    create_folder_and_replace_file(self.base_folder, FOLDER_EXEPTION[2], self.root, name, new_file_name)
                elif file_name[1] in DOCUMENTS_TYPE:
                    create_folder_and_replace_file(self.base_folder, FOLDER_EXEPTION[3], self.root, name, new_file_name)
                elif file_name[1] in ARCHIVES_TYPE:
                    create_folder_and_replace_file(self.base_folder, FOLDER_EXEPTION[4], self.root, name, new_file_name)
                    
                    shutil.unpack_archive(f'{self.base_folder}\\archives\\{new_file_name}',
                                        f'{self.base_folder}\\archives\\{file_name[0]}')
                    os.remove(f'{self.base_folder}\\{FOLDER_EXEPTION[4]}\\{new_file_name}')
                else:
                    create_folder_and_replace_file(self.base_folder, 'other', self.root, name, new_file_name)
 

def main(base_folder):

    for root, dirs, files in os.walk(base_folder):
        
        if os.path.basename(root) in FOLDER_EXEPTION:
            return
        else:
            SortingThread(files, base_folder, root).start()

    delete_empty_folder(base_folder)        
    


def delete_empty_folder(base_folder):
    try:
        for root, dirs, files in os.walk(base_folder):
            if os.listdir(root):
                continue
            else:
                os.rmdir(root)

        return delete_empty_folder(base_folder)
    except RecursionError:
        return


def create_folder_and_replace_file(base_folder, folder_name, root, name, new_file_name):
    if os.path.isdir(f'{base_folder}\\{folder_name}'):
        os.replace(f'{root}\\{name}', f'{base_folder}\\{folder_name}\\{new_file_name}')
    else:
        os.mkdir(f'{base_folder}\\{folder_name}')
        os.replace(f'{root}\\{name}', f'{base_folder}\\{folder_name}\\{new_file_name}')


def normalize(file_name, file_extension):
    chars = ' ()!?,./|@^%&*'
    tran_file_name = translate_file(file_name)
    for sym in chars:
        tran_file_name = tran_file_name.replace(sym, '_')

    return f'{tran_file_name}.{file_extension}'


if __name__ == '__main__':
    if len(sys.argv) == 1:

        print(f'Clean this folder => {os.getcwd()} ?')

        answ = input('Y/n =>  ').lower()

        if answ == 'y':

            main(os.getcwd())
        else:
            print('Try again ...')
    else:
        print(f'Start clean this folder => {sys.argv[1]}')
        main(sys.argv[1])

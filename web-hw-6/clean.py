import asyncio
import os
import sys
import aioshutil
from aiopath import AsyncPath

IMAGES_TYPE = ['jpeg', 'png', 'jpg', 'svg']
VIDEO_TYPE = ['avi', 'mp4', 'mov', 'mkv']
AUDIO_TYPE = ['mp3', 'ogg', 'wav', 'amr']
DOCUMENTS_TYPE = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
ARCHIVES_TYPE = ['zip', 'gz', 'tar']
FOLDER_EXEPTION = ['image', 'video', 'audio', 'documents', 'archives','other']

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
         "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC, LATIN):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def translate_file(name):
    return name.translate(TRANS)
        

async def create_folder(base_folder):
    for folder_name in FOLDER_EXEPTION:
        if not os.path.exists(fr'{base_folder}\\{folder_name}'):
            os.mkdir(f'{base_folder}\\{folder_name}') 


async def main():
    try:
        base_folder = AsyncPath(sys.argv[1])
        print(f'Clean this folder => {os.getcwd()}')
    except Exception:
        print("Wrong! Please try again")
  
    await create_folder(base_folder)

    for root, dirs, files in os.walk(base_folder):
   
        if os.path.basename(root) in FOLDER_EXEPTION:
            return
        else:
            for file in files:
                file_name, ext = file.split('.')
                new_file_name = await normalize(file_name, ext)
                if ext in IMAGES_TYPE:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[0]}\\{new_file_name}' )
                elif ext in VIDEO_TYPE:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[1]}\\{new_file_name}' )
                elif ext in AUDIO_TYPE:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[2]}\\{new_file_name}' )
                elif ext in DOCUMENTS_TYPE:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[3]}\\{new_file_name}' )
                elif ext in ARCHIVES_TYPE:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[4]}\\{new_file_name}' )
                    aioshutil.unpack_archive(f'{base_folder}\\archives\\{new_file_name}',
                                        f'{base_folder}\\archives\\{ext}')
                    os.remove(f'{base_folder}\\{FOLDER_EXEPTION[4]}\\{new_file_name}')
                else:
                    await replace_file(f'{root}\\{file}',f'{base_folder}\\{FOLDER_EXEPTION[5]}\\{new_file_name}' )

    await delete_empty_folder(base_folder)        
    


async def delete_empty_folder(base_folder):
    try:
        for root in os.walk(base_folder):
            if os.listdir(root):
                continue
            else:
                os.rmdir(root)

        return delete_empty_folder(base_folder)
    except RecursionError:
        return


async def replace_file(source,destination):
    os.replace(source, destination)



async def normalize(file_name, file_extension):
    chars = ' ()!?,./|@^%&*'
    tran_file_name = translate_file(file_name)
    for sym in chars:
        tran_file_name = tran_file_name.replace(sym, '_')

    return f'{tran_file_name}.{file_extension}'


if __name__ == '__main__':
    asyncio.run(main())

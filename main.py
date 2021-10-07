from pprint import  pprint
import requests
import os


def get_path_to_file(name_file_to_send):
    """Данная финкция на вход принимает имя файла,который мы хотим отправить.
     Если фаил находится в корневом каталоге программы, мы получим сразу path.
     Если файл находится в другом месте ,тогда необходимо указать путь к файлу.
     Функция проверить на достоверность указанный путь и нахождения файла в
     указанной директории. Если  указаной все верно мы получил path.
     Иначе выдает сообщение об ошибке.
    """
    res = False
    phath_our_dir = os.getcwd()
    list_files_in_our_dir = (os.listdir(phath_our_dir))

    for element in range(len(list_files_in_our_dir)):
        if name_file_to_send == list_files_in_our_dir[element]:
            res = True
            break

    if res:
        res = os.path.join(phath_our_dir, name_file_to_send)
    else:
        pprint(f"Файла  {name_file_to_send} в корневом каталоке программы нет")
        path = input(f"Укажите путь до {name_file_to_send}:")
        if os.path.isdir(path):
            os.chdir(path)
            path = os.getcwd()
            res = os.path.join(path, name_file_to_send)
            if os.path.isfile(res) == False :
                print(f"в {path} нет файла {name_file_to_send} ")
                res = False
        else:
            print(f"директории {path} нет ")
            res = False

    return res


class Yan:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, dick_file_path):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": dick_file_path, "overwrite": "true"}
        response = requests.get(files_url, headers=headers, params=params)

        return response.json()


    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()



token = ''
ya = Yan(token=token)

name_file_to_send = "test.txt"
file_path = get_path_to_file(name_file_to_send)
ya.upload_file_to_disk(name_file_to_send, file_path)






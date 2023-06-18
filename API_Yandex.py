import requests
from datetime import datetime

class YandexApi:
    base_url = 'https://cloud-api.yandex.net/v1'


    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'}


    def create_folder(self, folder_name: str): #cоздание папки на YD
        url = self.base_url + '/disk/resources'
        params = {
                'path': folder_name,
                'overwrite': True}
        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code == 409:
            curent_date = datetime.now()
            date_str = curent_date.strftime('%Y-%m-%d_%H-%M-%S')
            params = {
                'path': f'{folder_name}_{date_str}',
                'overwrite': True
            }
            requests.put(url, headers=self.headers, params=params)


    def upload_foto(self, path, url_foto): #загрузка в нужную папку в path принимает имя папки и имя файла
        url = self.base_url + '/disk/resources/upload'
        params = {'path': path,
                  'url': url_foto
                  }
        response = requests.post(url, headers=self.headers, params=params)






import requests
from datetime import datetime

class VkApi:

    base_url = 'https://api.vk.com/method/'

    def __init__(self, access_token, version):
        self.params = {
            'access_token': access_token,
            'v': version}
        self.list_foto = []
        self.dict_foto = {
                "file_name": "",
                "size": "",
                "url": ""}


    def get_last_foto(self, user_id): #моя собственная логика получения фото, так как не заметил метод в api
        method_url = f'{self.base_url}photos.get'
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': 'likes',
                  **self.params
        }
        respons = requests.get(method_url, params=params)
        data = respons.json()['response']['items']
        date_id = max(data, key=lambda x: x['id'])['id'] #последнее фото профиля
        data_photo = [photo for photo in data if photo['id'] == date_id] #находим по id в словаре фото
        max_size = max(data_photo[0]['sizes'], key=lambda x: x['type'])['type'] #Находим максимальное разрешение
        url_photo_max_size = [photo['url'] for photo in data_photo[0]['sizes'] if photo['type'] == max_size]
        return url_photo_max_size[0]

    def get_few_foto(self, user_id, count): #метод получения фото в список для загрузки на YD
        method_url = f'{self.base_url}photos.get'
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': 'likes',
                  'rev': '1',
                  'count': count,
                  **self.params
                  }
        respons = requests.get(method_url, params=params)
        data = respons.json()['response']['items']

        for foto in data:
            list_likes = []
            if foto['likes']['count'] in list_likes: #если количство лайков совпадает добавляется дата без формата
                datetime_obj = datetime.fromtimestamp(foto['date'])
                formatted_date = datetime_obj.strftime("%Y-%m-%d")
                self.dict_foto['file_name'] = f"{foto['likes']['count']}{formatted_date}.jpg"
            else:
                self.dict_foto['file_name'] = f"{foto['likes']['count']}.jpg"
                list_likes.append(foto['likes']['count'])


            max_size_foto = max(foto['sizes'], key=lambda x: x['type'])['type']
            self.dict_foto['size'] = max_size_foto
            self.dict_foto['url'] = [foto_url['url'] for foto_url in foto['sizes'] if foto_url['type'] == max_size_foto][0]
            self.list_foto.append(self.dict_foto.copy()) #в список мы добавляем копию, чтобы последующие не перетирали старые данные



    def id_in_screen_name(self, screen_name):
        if screen_name.isdigit():
            return int(screen_name)
        else:
            method_url = f'{self.base_url}utils.resolveScreenName'
            params = {'screen_name': screen_name,
                      **self.params}
            respons = requests.get(method_url, params=params)
            return respons.json()['response']['object_id']










import os
import json
from API_VKontakte import VkApi
from API_Yandex import YandexApi
from Data_processing import Processing
from dotenv import load_dotenv
from tqdm import tqdm


if __name__ == '__main__':
    load_dotenv() #Обязательный вызов при вызове .env

    vk_token = os.getenv('VK_API_TOKEN')
    ya_token = os.getenv('YANDEX_TOKEN')
    vers = os.getenv('VERSION')
    vk = VkApi(vk_token, vers)
    ya = YandexApi(ya_token)
    w = Processing()

    print("Приветствую вас!")
    id = input(f'Введите ID или SCREEN_NAME: ')
    count = int(input(f'Введите количество фотографий профиля: '))
    folder = ya.create_folder(input('Введите название папки: '))
    id = vk.id_in_screen_name(id)
    data_foto = vk.get_few_foto(id, count)
    list_foto = vk.list_foto
    w.write_dock(list_foto) #запись в json

    for foto in tqdm(list_foto, desc='Uploading file'): #библиотека для лодера
        ya.upload_foto(f"{folder}/{foto['file_name']}", foto['url'])

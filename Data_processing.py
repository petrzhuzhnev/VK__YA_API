import json


class Processing():

    def write_dock(self, dict_foto): #запись в файл
        with open('new.json', 'w') as f:
            json.dump(dict_foto, f, indent=1)



import json
from pprint import pprint
from typing import Any
from cerberus import Validator

class JsonManager:
    '''Класс для работы с json файлами во время парсинга'''

    def __init__(self, encoding: str = 'utf8') -> None:
        '''Конструктор

        encoding: кодировка открываемого файла'''
        schema = {
            'encoding': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate({'encoding': encoding}):
            raise ValueError(v.errors)

        self.encoding = encoding

    def pprint(self, data: Any) -> None:
        '''Выводим данные в удобочитаемом виде

        data: данные которые надо вывести'''
        pprint(data)

    def load(self, pathToJsonFile: str) -> Any:
        '''Получаем данные из json файла

        pathToJsonFile: путь до json файла'''

        schema = {
            'pathToJsonFile': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate({'pathToJsonFile': pathToJsonFile}):
            raise ValueError(v.errors)

        with open(pathToJsonFile, encoding=self.encoding) as jsonFile:
            src = json.load(jsonFile)
        return src

    def dump(self, pathToJsonFile: str, data: Any) -> None:
        '''Записываем данные в json файл

        pathToJsonFile: путь до json файла
        data: данные которые надо записать'''

        schema = {
            'pathToJsonFile': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate({'pathToJsonFile': pathToJsonFile}):
            raise ValueError(v.errors)

        with open(pathToJsonFile, 'w', encoding=self.encoding) as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=0)

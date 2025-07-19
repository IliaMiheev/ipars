from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep
import requests
from os import mkdir
from os.path import exists

class Pars:
    '''Модуль для работы с запросами и bs4'''

    def mkdir(self, nameDir: str):
        '''Создаёт папку если её ещё нет
        
        nameDir: название папки которая будет создана'''
        if not exists(nameDir):
            mkdir(nameDir)

    def returnBs4Object(self, pathToFile: str, encoding: str = 'utf8', parser: str = 'lxml'):
        '''Возвращаем объект beautifulsoup

        pathToFile: путь до html файла
        encoding: кодировка открытия html файла
        parser: парсер, который будет использоваться для работы'''
        with open(pathToFile, encoding=encoding) as file:
            src = file.read()
        soup = BeautifulSoup(src, parser)
        return soup

    def getTexts(self, arr: list, needFix: bool = 0) -> list:
        '''Возвращаем текст из элементов bs4
        
        arr: список объектов bs4 из которых будет извлекаться текст
        needFix (0/1): если этот параметр установлен как True, то из текста будут удалены \\n, \\t и пробелы с концов'''
        result = []
        for item in arr:
            data = item.text
            if needFix:
                data = data.strip()
                data = data.replace('\t', '')
                data = data.replace('\n', '')

            if not data:
                continue
            result.append(data)

        if not result:
            return None
        return result

    def getAttributes(self, arr: list, att: str) -> list:
        '''Возвращаем список значений атрибутов
        
        arr: список объектов bs4 из которых будет извлекаться атрибут
        att: строка с названием атрибута по которому будет осуществляться поиск'''
        result = []
        for item in arr:
            data = item.get(att)
            if data is not None:
                result.append(item.get(att))

        if not result:
            return None
        return result

    def pprint(self, data: any) -> None:
        '''Выводим данные в удобочитаемом виде

        data: данные которые надо вывести'''
        pprint(data)

    def getStaticPage(self, pathToSaveFile: str, url: str, writeMethod: str = 'w', headers: dict = None) -> int:
        '''Получаем статическую страницу и возвращаем статус ответа от сервера

        pathToSaveFile: путь, куда сохранится полученный файл
        url: ссылка на данные
        writeMethod: метод записи данных в файл. "W" записывает текст, "WB" — байты
        headers: заголовки запроса к серверу'''

        if headers is None:
            # Получаем случайный user agent
            software_names = [
                SoftwareName.FIREFOX.value, 
                SoftwareName.CHROME.value, 
                SoftwareName.EDGE.value, 
                SoftwareName.SAFARI.value, 
                SoftwareName.YANDEX.value, 
                ]
            operating_systems = [
                OperatingSystem.WINDOWS.value, 
                OperatingSystem.LINUX.value,
                OperatingSystem.IOS.value,
                OperatingSystem.MACOS.value, 
                ]   
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)
            user_agent = user_agent_rotator.get_random_user_agent()

            headers = {
                "Accept": "*/*",
                "User-Agent": user_agent
            }

        try:
            # Отправляем запрос
            req = requests.get(url, headers=headers)

            # Записываем данные
            if writeMethod == 'w':
                src = req.text
                with open(pathToSaveFile, 'w', encoding='utf-8') as file:
                    file.write(src)

            elif writeMethod == 'wb':
                src = req.content
                with open(pathToSaveFile, 'wb') as file:
                    file.write(src)
            else:
                raise ValueError(f"Неподдерживаемый метод записи: {writeMethod}")

            return req.status_code  # Возвращаем статус ответа от сервера

        except requests.exceptions.HTTPError as httpErr:
            raise RuntimeError(f"HTTP ошибка: {httpErr}") from http_err
        except Exception as e:
            raise RuntimeError(e) from e

    def __scrollAndSave(self, driver, timeSleep, pathToSaveFile):
        # Прокручиваем страницу до самого низа
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Прокручиваем до низа страницы
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Ждем загрузки страницы
            sleep(timeSleep)
            # Вычисляем новую высоту страницы
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        htmlContent = driver.page_source
        with open(pathToSaveFile, "w", encoding="utf-8") as file:
            file.write(htmlContent)

    def getDinamicPage(self, pathToSaveFile: str, url: str, closeWindow: bool = 1, timeSleep: int = 2) -> None:
        '''Получаем динамическую страницу

        pathToSaveFile: путь, куда сохранится полученный файл
        url: ссылка на сайт
        closeWindow (0/1): если указана единица, то браузер открывается в фоновом режиме, 0 — открывается как обычное приложение
        timeSleep: время ожидания браузера перед тем как скролить страницу дальше'''

        # Устанавливаем опции для Chrome WebDriver
        options = Options()
        if closeWindow:
            options.add_argument('--headless')

        # открываем браузер
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            self.__scrollAndSave(driver, timeSleep, pathToSaveFile)

    def gpsa(self, pathToSaveFile: str, url: str, timeSleep=2):
        '''Получаем страницу в полуавтоматическом режиме 
        gpsa - get page semi-automatically

        pathToSaveFile: путь, куда сохранится полученный файл
        url: ссылка на сайт
        timeSleep: время ожидания браузера перед тем как скролить страницу дальше'''

        with webdriver.Chrome() as driver:
            driver.get(url)
            a = input('Нажми ENTER когда закончишь')
            self.__scrollAndSave(driver, timeSleep, pathToSaveFile)

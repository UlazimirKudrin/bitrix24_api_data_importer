from urllib.parse import urlencode
import requests
import time
from datetime import datetime


def get_bitrix24_data(access_token, endpoint, params={}, type = ''):
    base_url = f"{access_token}"
    url = base_url + endpoint

    all_data = []  # Список для хранения данных со всех страниц

    start = 0  # Начальная страница

    while True:
        try:
            # Добавление параметра "start" для указания текущей страницы
            params['start'] = start
            
            # Выполнение POST-запроса к API
            response = requests.post(url, json=params)
            # response.raise_for_status()  # Проверка на ошибки

            # Парсинг JSON-ответа
            data = response.json()


            if 'error' in data and data['error'] == 'QUERY_LIMIT_EXCEEDED':
                # Пауза на 5 секунд
                time.sleep(5)
                print("Пауза 5 секунд")
                continue
            
            if type=='items':
                items = data['result']['items']
            elif type=='tasks':
                items = data['result']['tasks']
            elif type=='catalogs':
                items = data['result']['catalogs']
            elif type=='products':
                items = data['result']['products']
            elif type=='workgroups':
                items = data['result']['workgroups']
            elif type=='categories':
                items = data['result']['categories']
            else:
                # items =  ("result", [])
                items = data['result']
            
            # Добавление данных текущей страницы к общему списку
            all_data.extend(items)
            time.sleep(1)

            
            
            if ('next' in data) and (data['next']<data['total']):
                # Переход к следующей странице
                # print('total =', data['total'])
                # print('next = ', data['next'])
                # start = start + data['next']
                start = data['next']
                print(start,"/", data['total'], "элементов экспортированы")
            else:
                break
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    return all_data




def get_bitrix24_overdue_tasks_data(access_token, endpoint, params={}):
    base_url = f"{access_token}"
    url = base_url + endpoint

    all_data = []  # Список для хранения данных со всех страниц

    start = 0  # Начальная страница

    while True:
        try:
            # Добавление параметра "start" для указания текущей страницы
            params['start'] = start
            
            # Выполнение POST-запроса к API
            response = requests.post(url, json=params)
            # response.raise_for_status()  # Проверка на ошибки

            # Парсинг JSON-ответа
            data = response.json()


            if 'error' in data and data['error'] == 'QUERY_LIMIT_EXCEEDED':
                # Пауза на 5 секунд
                time.sleep(5)
                print("Пауза 5 секунд")
                continue
            
            items = data['result']['tasks']

            # Обрабатываем каждую задачу - добавляем нужные поля
            for task in items:
                processed_task = {
                    # 'id': str(uuid.uuid4()),    # Генерируем уникальный UUID
                    'taskid': task.get('id'),  # Переименовываем ID в task_id                    
                    'overduedatetime': datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),
                    'deadline': task.get('deadline'),
                    'createddate': task.get('createdDate'),
                    'closeddate': task.get('closedDate'),
                }
                all_data.append(processed_task)
            
            
            # # Добавление данных текущей страницы к общему списку
            # all_data.extend(items)
            time.sleep(1)

            
            
            if ('next' in data) and (data['next']<data['total']):
                # Переход к следующей странице
                # print('total =', data['total'])
                # print('next = ', data['next'])
                # start = start + data['next']
                start = data['next']
                print(start,"/", data['total'], "элементов экспортированы")
            else:
                break
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    return all_data



def get_bitrix24_data_all(access_token, endpoint, params={}, type=''):
    base_url = f"{access_token}"
    url = base_url + endpoint

    all_data = []

    res_id = 0  # Начальное значение ID

    while True:
        try:
            if 'filter' in params:
                params['filter'].update({'>ID': res_id})  # Дополняем фильтр по ID
            else:
                params['filter'] = {'>ID': res_id}  # Фильтр по ID

            # Используем start = -1
            params['start'] = -1

            
            
            response = requests.post(url, json=params)
            data = response.json()

            # print(data)

            if 'error' in data and data['error'] == 'QUERY_LIMIT_EXCEEDED':
                time.sleep(5)
                print("Пауза 5 секунд")
                continue
            
            if type == 'items':
                items = data['result']['items']
            elif type == 'tasks':
                items = data['result']['tasks']
            elif type == 'catalogs':
                items = data['result']['catalogs']
            elif type == 'products':
                items = data['result']['products']
            elif type == 'workgroups':
                items = data['result']['workgroups']
            elif type == 'categories':
                items = data['result']['categories']
            else:
                items = data['result']
            
            if len(items) > 0:
                # Обновляем значение ID
                res_id = items[-1]['ID']
                all_data.extend(items)
                time.sleep(1)
            else:
                break
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    return all_data
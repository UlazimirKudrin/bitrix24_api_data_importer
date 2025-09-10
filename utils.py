import json
from datetime import datetime
from datetime import timedelta
from pytz import timezone

def save_to_json(filename, data):
    # Запись данных в файл
    with open(f"/var/www/export.b24/json/{filename}", "w") as json_file:
        json.dump(data, json_file, indent=4)
        print("Данные записаны в файл", filename)

def save_to_csv(filename, df):
    # Запись данных в CSV файл
    df.to_csv(f"/var/www/export.b24/csv/{filename}", index=False, encoding="utf-8")
    print("Данные записаны в файл", filename)



def get_start_of_previous_day():
    tz = timezone('Europe/Moscow')
    current_time = datetime.now(tz)  # Текущее время с учётом временной зоны
    start_of_previous_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    return start_of_previous_day.strftime('%Y-%m-%dT%H:%M:%S%z')

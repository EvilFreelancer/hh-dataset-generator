import json
import os
import requests
import time

# Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле 
for fl in os.listdir('./docs/pagination'):

    # Открываем файл, читаем его содержимое, закрываем файл
    f = open('./docs/pagination/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    # Преобразуем полученный текст в объект справочника
    jsonObj = json.loads(jsonText)

    # Получаем и проходимся по непосредственно списку вакансий
    for v in jsonObj['items']:
        # Обращаемся к API и получаем детальную информацию по конкретной вакансии
        req = requests.get(v['url'])
        data = req.content.decode()
        req.close()

        print(v['id'])

        # Создаем файл в формате json с идентификатором вакансии в качестве названия
        # Записываем в него ответ запроса и закрываем файл
        fileName = './docs/vacancies/{}.json'.format(v['id'])
        f = open(fileName, mode='w', encoding='utf8')

        jsonVocObj = json.loads(data)
        f.write(json.dumps(jsonVocObj, ensure_ascii=False, sort_keys=True, indent=2))
        f.close()

        time.sleep(0.25)

print('Вакансии собраны')

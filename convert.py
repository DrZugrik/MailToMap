### Add libraries

import os
import csv
import imbox
import traceback
import re

###

with open('mail_settings.txt', 'r') as file:
    content = file.read()
    filename = content.split('filename=')[1].split('\n')[0]
    file.close()

# Имя файла, куда будут сохраняться данные
filename_csv = filename + '.csv'
filename_DS_data_csv = filename + '_DS_data.csv'


# Открываем файл csv на чтение и добавление строк, указываем правильную кодировку
with open(filename_csv, 'r', encoding='utf-8-sig') as f1, open(filename_DS_data_csv, 'w', newline='', encoding='utf-8-sig') as f2:
    reader = csv.reader(f1, delimiter=',')
    writer = csv.writer(f2, delimiter=',')

    # Проходимся циклом по строкам из первого файла
    for row in reader:
        # Считываем нужные столбцы
        uid, head, _from, data, body, body_short, num, price, address, cadastral = row[:10]

        # Проверяем, что в столбце body_short нет слов про подписание
        pattern_ = r'\b(?:[Пп]одпи|подпи|ПОДПИ)\w*\b'
        #pattern_from = r'\bKikteva\w*\b'

        if not re.search(pattern_, body_short) is not None:
            # Записываем нужные столбцы во второй файл
            writer.writerow([uid, head, _from, data, body_short, num, price, address, cadastral])

print("Готово!")

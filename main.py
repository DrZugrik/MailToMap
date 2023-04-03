### Импорт необходимых библиотек

import csv
import imbox
import traceback
import re

###

with open('mail_settings.txt', 'r') as file:
    content = file.read()
    email = content.split('email=')[1].split('\n')[0]
    passwrd = content.split('pass=')[1].split('\n')[0]
    filename = content.split('filename=')[1].split('\n')[0]
    mail_from = content.split('mail_from=')[1].split('\n')[0]

# Имя файла, куда будут сохраняться данные
filename_csv = filename+'.csv'

# Загрузка данных почтового ящика из файла
# Указываем данные для подключения к почтовому ящику
imbox_instance = imbox.Imbox('imap.gmail.com',
                             username=email,
                             password=passwrd,
                             ssl=True,
                             ssl_context=None)

m = 1 # счетчик обработанных писем

try:
    # Формирование запроса
    query = {
        "sent_from": f"{mail_from}",
    }

    # Получение списка писем
    messages = imbox_instance.messages(folder='INBOX', **query)

    with open(filename_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Head', 'From', 'Data', 'Body', 'Num', 'Price', 'Adress', 'Cadastr'])
        for uid, message in messages:
            pattern_num = r'\b\w\d{1,4}\b|\b\d{2,6}\b'
            num = re.findall(pattern_num, message.subject)

            #pattern_address = r'(?:(?P<region>[А-ЯЁ][а-яё]+(?:\s+область|\s+край|\s+республика))\s*,\s*)?(?:(?P<city>[А-ЯЁ][а-яё]+(?:\s+город|\s+поселок|\s+деревня|\s+станция))\s*,\s*)?(?:(?P<street>(?:ул\.|улица|пер\.|переулок|пр\.|проспект|бульвар)\s*\w+)\s*,\s*)?(?P<building>\w+\s*\d+(?:\s*к(?:орпус)?\.?\s*\d+)?(?:\s*стр\.?\s*\d+)?(?:\s*кв\.?\s*\d+)?(?:\s*,?\s*(?P<postcode>\d{6}))?)'
            #address = re.findall(pattern_address, message.body['plain'][0])

            #pattern_price = r'(?:прими\s+)?(?:в\s+)?работу\s+(?P<cost>\d{4,6})\s*(?:руб(?:лей)?|рэ|р|p.|т|т.)'
            #price = re.findall(pattern_price, message.body['plain'][0])

            cadastr_num = r'\d{2,3}:\d{2,3}:\d{6}:\d{2,3}'
            cadastr = re.findall(cadastr_num, message.body['plain'][0])

            writer.writerow([message.subject, message.sent_from, message.date, message.body['plain'][0], num, 'price', 'address', cadastr])

            print(f'Записано письмо {m} из {len(messages)}')
            m+=1

except Exception as e:
    print(traceback.format_exc())


'''
text = "Напишите мне на example@mail.ru или позвоните по телефону +7 (123) 456-78-90"
email_pattern = r'\b[\w.-]+@[a-zA-Z_-]+?\.[a-zA-Z]{2,3}\b'
phone_pattern = r'\+?\d[\d()-]{8,}\d'

text_without_emails = re.sub(email_pattern, '', text)
text_without_contacts = re.sub(phone_pattern, '', text_without_emails)
'''

#filename.close()    # Закрываем файл csv
imbox_instance.logout()     # Закрываем обращение к почтовому ящику



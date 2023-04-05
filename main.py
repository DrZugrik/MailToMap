import csv
import imbox
import traceback
import re
import pandas as pd
import os

with open('mail_settings.txt', 'r') as file:
    content = file.read()
    email = content.split('email=')[1].split('\n')[0]
    passwrd = content.split('pass=')[1].split('\n')[0]
    filename = content.split('filename=')[1].split('\n')[0]
    mail_from = content.split('mail_from=')[1].split('\n')[0]

# Имя файла, куда будут сохраняться данные
filename_csv = filename + '.csv'

# Загрузка данных почтового ящика из файла
# Указываем данные для подключения к почтовому ящику
imbox_instance = imbox.Imbox('imap.gmail.com',
                             username=email,
                             password=passwrd,
                             ssl=True,
                             ssl_context=None)
m = 1  # счетчик обработанных писем

try:
    # Формирование запроса
    query = {
        "sent_from": f"{mail_from}",
    }

    # Получение списка писем
    messages = imbox_instance.messages(folder='INBOX', **query)


    # Открываем файл csv на чтение и добавление
    with open(filename_csv, 'a+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')

        # Если файл пустой, записываем заголовок
        if file.tell() == 0:
            writer.writerow(['UID', 'Head', 'From', 'Data', 'Body', 'Body_short', 'Num', 'Price', 'Adress', 'Cadastr'])

        # Читаем CSV файл в DataFrame
        df = pd.read_csv(filename_csv)
        num_rows = df.shape[0]
        # Обходим все письма
        for uid, message in messages:
            # Проверяем, был ли уже сохранен UID этого письма в CSV файле
            if uid in df['UID'].values:
                continue  # Если да, то переходим к следующему письму

            pattern_num = r'\b\w\d{1,4}\b|\b\d{2,6}\b'
            num = re.findall(pattern_num, message.subject)

            body = message.body['plain'][0]
            cleaned_body = "\n".join([line.strip() for line in body.split("\n") if line.strip()])

            # вставить регулярное выражение начиная с С уважением и до конца всего текста
            cleaned_body = re.sub(r"с уважением.*$", "", cleaned_body, flags=re.DOTALL | re.IGNORECASE)

            pattern_body_short = r'^(From:|To:|Sent:|Cc:|Subject:|[>|Тел\.|E-mail:|Моб\.]).*$'
            body_short = re.sub(pattern_body_short, '', cleaned_body, flags=re.MULTILINE)

            body_short = "\n".join([line.strip() for line in body_short.split("\n") if line.strip()])

            #pattern_address = r'(?:(?P<region>[А-ЯЁ][а-яё]+(?:\s+область|\s+край|\s+республика))\s*,\s*)?(?:(?P<city>[А-ЯЁ][а-яё]+(?:\s+город|\s+поселок|\s+деревня|\s+станция))\s*,\s*)?(?:(?P<street>(?:ул\.|улица|пер\.|переулок|пр\.|проспект|бульвар)\s*\w+)\s*,\s*)?(?P<building>\w+\s*\d+(?:\s*к(?:орпус)?\.?\s*\d+)?(?:\s*стр\.?\s*\d+)?(?:\s*кв\.?\s*\d+)?(?:\s*,?\s*(?P<postcode>\d{6}))?)'
            #adress = re.findall(pattern_address, body_short)



            cadastr_num = r'\d{2,3}:\d{2,3}:\d{6}:\d{2,3}'
            cadastr = re.findall(cadastr_num, cleaned_body)

            writer.writerow([uid, message.subject, message.sent_from, message.date, cleaned_body, body_short, num, 'coast', 'adress', cadastr])

            print(f'В почтовом ящике содержится {len(messages)} писем. В файле уже есть {num_rows + m} записей. Записано письмо {m} из {len(messages) - num_rows - m} оставшихся.')
            m+=1

            if (num_rows + m) >= len(messages) or len(df[df['UID'] == uid]) > 0:
                break

except Exception as e:
    print(traceback.format_exc())

imbox_instance.logout()     # Закрываем обращение к почтовому ящику


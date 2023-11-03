import csv

season_dict = {'Осень' : ['.09', '.10', '.11'],
               'Зима' : ['.12', '.01', '.02'],
               'Весна' : ['.03', '.04', '.05'],
               'Лето' : ['.06', '.07', '.08']
                }

file = 'total_reports.csv'
with open (file, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    autum = 0
    winter = 0
    spring = 0
    summer = 0

    for row in reader:
        for i in range(3):
            if season_dict['Осень'][i] in row['Дата']:
                autum += 1
                break
            elif season_dict['Зима'][i] in row['Дата']:
                winter += 1
                break
            elif season_dict['Весна'][i] in row['Дата']:
                spring += 1
                break
            elif season_dict['Лето'][i] in row['Дата']:
                summer += 1
                break

print(f'Запросы по сезону:\nОсень: {autum}\nЗима: {winter}\nВесна: {spring}\nЛето: {summer}\n')

result = round(50000 / 11, 2)
print(result)
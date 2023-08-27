from time import sleep
import requests
from bs4 import BeautifulSoup
import json, csv

url = 'https://health-diet.ru/table_calorie/'


headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0'

}

# req = requests.get(url, headers=headers)
# src = req.text

# # with open('index.html', 'w', encoding='utf-8') as file:
# #     file.write(src)

# with open('index.html',encoding='utf-8') as file:
#     src = file.read()
    
# soup = BeautifulSoup(src, 'lxml')

# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
# all_categories_dict = {}


# for item in all_products_hrefs:
#     item_title = item.text
#     item_href = 'https://health-diet.ru' + item['href']
    
#     all_categories_dict[item_title] = item_href
    

# with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open('all_categories_dict.json', 'r', encoding='utf-8') as file:
    all_categories = json.load(file)
    
    
iteration_count = int(len(all_categories)) - 1
print(f'Всего {iteration_count} итераций ')
count = 0

for category_name, category_href in all_categories.items():

    rep = [' ', ',', '-']
    
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    
    req = requests.get(category_href, headers=headers) 
    src = req.text
    
    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)
        
    with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')
           
        
    #Проверка страницы на наличие таблицы
    alert_block = soup.find(class_='uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top')
    if alert_block is not  None:
        continue    
    
    
    #Собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    
    product = table_head[0].text
    calories = table_head[1].text
    porteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    
    
    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
            product,
            calories,
            porteins,
            fats,
            carbohydrates
            )
        )
         
    
    #Собираем данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    
    product_info = []
    
    for item in products_data:
        products_tds = item.find_all('td')
        
        title = products_tds[0].find('a').text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text
        
        product_info.append(
            {
                'Title':title,
                'Calories': calories,
                "Proteins": proteins,
                'Fats': fats,
                "Carbohydrates": carbohydrates
            }
        )
        
        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                title,
                calories,
                porteins,
                fats,
                carbohydrates
                )
            )
        
    with open(f'data/{count}_{category_name}.json', 'w', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
            
        
    count += 1
    print(f'# {count}-я итерация. {category_name} записана в таблицу...')
    iteration_count = iteration_count - 1
    if iteration_count == 0:
        print('Работа закончена!!!')
        break
    print(f'# Осталось {iteration_count} итераций')
    sleep(0.1)
    
import requests
from bs4 import BeautifulSoup
import time

def send_message(message):
    ## Отправляем сообщение о новой статье
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHANNEL_ID, 'text': message, "parse_mode": "HTML"}
    response = requests.post(url, data=data)
    return response.json()

def is_post_published(url):
    ## Проверяем, была ли данная статья уже опубликована ботом в чате
    with open(FILE_NAME, 'r') as f:
        published_posts = f.readlines()
        if url + '\n' in published_posts:
            return True
        else:
            return False
        
def add_to_published(url):
    ## Добавляем ссылку на статью в список опубликованных ботом
    with open(FILE_NAME, 'a') as f:
        f.write(url + '\n')

def check_for_new_posts():
    # Получаем HTML-страницу сайта
    url = 'https://what-used-to-be.blogspot.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Получаем все статьи на странице
    posts = soup.find_all('div', class_='post hentry')##забираем все <div>ы с классом "post hentry" со страницы
    
    # Перебираем статьи
    for post in posts:
        # Получаем заголовок и URL статьи
        header = post.find('h3', class_='post-title entry-title').text.strip()
        short_description = post.find('div', class_='post-body entry-content').text.strip()
        link_para = post.find('div', class_='jump-link')
        if link_para == None:
            continue
        url = link_para.find('a')['href']

        # Проверяем, была ли статья уже опубликована
        if not is_post_published(url):
            # Если статья новая, отправляем ее в канал
            message = f'<b>{header}</b>\n \n{short_description}\n \n<a href="{url}">Читать полностью</a>'
            print (message)
            send_message(message)

            # Добавляем URL статьи в файл опубликованных статей
            add_to_published(url)
          
########################################################################################
## Переменные для указания id бота и чата, без них код работать не будет!
########################################################################################
BOT_TOKEN =
CHANNEL_ID =
########################################################################################
FILE_NAME = 'published_posts.txt' ##файл, где хранится информация об уже опубликованных статьях

while True:
    check_for_new_posts()
    time.sleep(300)

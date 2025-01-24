import requests
import re
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
    return response.text


def extract_vacancy_data(html: str) -> str:
   soup = BeautifulSoup(html, 'html.parser')

   # Title
   title = soup.find('h1', class_='text-1')
   title = title.text.strip() if title else 'Название не найдено'

   # Budget
   budget_el = soup.find('span', class_='fl-rub')
   budget = budget_el.parent.text.strip() if budget_el else 'Бюджет не указан'

   # Description
   desc_el = soup.find('div', {'id': re.compile(r'^projectp\d+$')})
   description = desc_el.text.strip() if desc_el else 'Описание не найдено'

   # Dates
   date_el = soup.find(string=re.compile('Опубликован:'))
   date = date_el.parent.find_next('div').text.strip() if date_el else 'Дата не указана'

   deadline_el = soup.find(string=re.compile('Дедлайн:'))
   deadline = deadline_el.parent.text.strip() if deadline_el else 'Дедлайн не указан'

   # Category
   category_el = soup.find('div', {'class': 'text-5 mb-4 b-layout__txt_padbot_20'})
   category = category_el.text.strip() if category_el else "Категория не найдена"

   return f"""# {title}

**Бюджет:** {budget}

**Описание:**
{description}

**Опубликован:** {date} 
**Дедлайн:** {deadline}
**Категория:** {category}"""

def extract_candidate_data(html: str) -> str:
   soup = BeautifulSoup(html, 'html.parser')

   # Main info
   content = soup.find('td', {'style': 'padding:19px'})
   resume = content.get_text(strip=True) if content else 'Резюме не найдено'

   # Basic info
   name = soup.find('h1').text.replace('Информация ', '').strip() if soup.find('h1') else 'Имя не указано'
   rating_el = soup.find('tr', {'class': 'first'})
   rating = rating_el.find_next('td').text.strip() if rating_el else 'Рейтинг не указан'

   # Additional info
   attendance_el = soup.find(string=re.compile('Посещаемость:'))
   attendance = attendance_el.find_next('td').text.strip() if attendance_el else 'Нет данных'

   experience_el = soup.find(string=re.compile('На сайте:'))
   experience = experience_el.find_next('td').text.strip() if experience_el else 'Опыт не указан'

   location_el = soup.find(string=re.compile('Местонахождение:'))
   location = location_el.find_next('td').text.strip() if location_el else 'Местоположение не указано'

   date_el = soup.find(string=re.compile('Дата регистрации:'))
   registration_date = date_el.find_next('td').text.strip() if date_el else 'Дата не указана'

   lang_el = soup.find(string=re.compile('Языки:'))
   languages = lang_el.find_next('td').text.strip() if lang_el else 'Языки не указаны'

   return f"""# {name}

**Рейтинг:** {rating}  
**Посещаемость:** {attendance}

**Опыт работы:** {experience}
**Местоположение:** {location}
**Дата регистрации:** {registration_date}
**Языки:** {languages}

**Резюме:**
{resume}"""

def get_candidate_info(url: str) -> str:
    html = get_html(url)
    return extract_candidate_data(html)


def get_job_description(url: str) -> str:
    html = get_html(url)
    return extract_vacancy_data(html)




print(get_candidate_info('https://www.fl.ru/users/mavrussco/info/'))
print(get_job_description('https://www.fl.ru/projects/5391729/razrabotka-telegram-bota-v-formate-web.html'))
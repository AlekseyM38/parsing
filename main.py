import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Инициализация веб-драйвера (здесь используется Chrome)
driver = webdriver.Chrome()

# Открытие страницы с вакансиями
url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
driver.get(url)

# Список для хранения ссылок на вакансии
vacancy_urls = []

# Находим все ссылки на вакансии на странице с помощью XPath
vacancy_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/vacancy/") and not(contains(@href, "advanced")) and not(contains(@href, "map"))]')

# Сохраняем ссылки на вакансии в виде URL
for link in vacancy_links:
    vacancy_urls.append(link.get_attribute('href'))

# Список для хранения информации о подходящих вакансиях
vacancies = []

# Проходим по каждой ссылке на вакансию
for vacancy_url in vacancy_urls:
    # Переходим к странице вакансии
    driver.get(vacancy_url)
    # Получаем информацию о вакансии
    company = driver.find_element(By.CSS_SELECTOR, ".vacancy-company-name").text
    # Пытаемся получить информацию о зарплате
    try:
        salary_element = driver.find_element(By.CSS_SELECTOR, ".vacancy-salary")
        salary = salary_element.text.strip()
    except NoSuchElementException:
        salary = "Не указано"
    # Получаем информацию о городе
    try:
        city_element = driver.find_element(By.CSS_SELECTOR, ".vacancy-company-address-text")
        city = city_element.text.strip()
    except NoSuchElementException:
        city = "Не указан"
    description = driver.find_element(By.CSS_SELECTOR, ".vacancy-description").text
    # Проверяем наличие ключевых слов "Django" и "Flask" в описании вакансии
    if "Django" in description and "Flask" in description:
        # Записываем информацию о вакансии в список
        vacancies.append({
            "url": vacancy_url,
            "company": company,
            "city": city,
            "salary": salary
        })

# Закрываем драйвер после завершения работы
driver.quit()

# Записываем информацию о подходящих вакансиях в JSON файл
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print("Информация о подходящих вакансиях успешно записана в vacancies.json")

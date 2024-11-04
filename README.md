Контактна інформація виконавця
Ім'я: Vasil Bolekhan
Email: bolehanw@gmail.com
Опис проєкту
Цей проєкт – Python-скрипт для асинхронного веб-скрапінгу продуктів із вебсайту Igefa store. Скрипт переходить на сторінки товарів, збирає дані та зберігає їх у CSV-файлі для подальшого аналізу.

This project is a Python-based asynchronous web scraper that collects product data from the Igefa store. It navigates product pages, extracts relevant details, and saves the data to a CSV file for further analysis.

Налаштування середовища та запуск скрипта
1. Клонування репозиторію
git clone https://github.com/bolekhan1508/igefa-web-scraper.git
cd igefa-web-scraper
2. Створення та активація віртуального середовища
Create and activate a virtual environment.
На Windows:
python -m venv venv
venv\Scripts\activate
3. Інсталяція необхідних бібліотек
Install the required libraries using:
pip install -r requirements.txt
4. Запуск скрипта
Run the script to start scraping:
python scrape.py

## parser_b2b-center
# Как это работает
  Парсинг тендеров:   
    Приложение использует BeautifulSoup для парсинга HTML-страницы B2B-Center, извлекая информацию о тендерах (номер, тему, заказчика, цену, дату окончания и ссылку).  
  Сохранение данных:   
    Данные можно сохранить в CSV или SQLite формате.  
  CLI интерфейс:  
    python main.py --max 10 --output tenders.csv - парсит 10 тендеров и сохраняет в CSV  
    python main.py --max 50 --output tenders.db - парсит 50 тендеров и сохраняет в SQLite  
    python main.py --serve - запускает FastAPI сервер  
  API endpoint:  
    GET /tenders?max_tenders=10 - возвращает JSON с тендерами  
# Что использовал:  
  BeautifulSoup - для парсинга HTML  
  Requests - для HTTP запросов  
  SQLite3 - для работы с базой данных  
  FastAPI - для создания API  
  Uvicorn - ASGI сервер  
  Argparse - для обработки аргументов командной строки  
# Что можно улучшить:  
  Добавить больше проверок на ошибки  
  Улучшить обработку множества страниц  
  Парсить больше информации о каждом тендере  
  Вынести настройки в конфигурационный файл  
# Как запускать:  
Установите зависимости:  
  pip install -r requirements.txt  
Запустите парсер:  
  python main.py --max 10 --output tenders.csv  
Или запустите сервер:  
  python main.py --serve  
  Затем откройте http://localhost:8000/tenders в браузере  
  

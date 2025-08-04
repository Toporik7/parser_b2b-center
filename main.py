import argparse
import csv
import sqlite3
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()
BASE_URL = "https://www.b2b-center.ru/market/"


def parse_tenders(max_tenders: int) -> List[Dict]:
    tenders = []
    page = 1
    
    while len(tenders) < max_tenders:
        url = f"{BASE_URL}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tender_rows = soup.select('table.search-results tr')[1:]
        
        for row in tender_rows[:max_tenders - len(tenders)]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                tender = {
                    'name': cols[0].get_text(strip=True),
                    'organization': cols[1].get_text(strip=True),
                    'start_date': cols[2].get_text(strip=True),
                    'end_date': cols[3].get_text(strip=True),
                    'link': BASE_URL[:-8] + cols[1].find('a')['href'] if cols[1].find('a') else ''
                }
                tenders.append(tender)
        
        if not tender_rows:
            break
            
        page += 1
    
    return tenders


def save_to_csv(tenders: List[Dict], filename: str):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'organization', 'start_date', 'end_date', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tenders)


def save_to_sqlite(tenders: List[Dict], filename: str):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenders (
        name TEXT,
        organization TEXT,
        start_date TEXT,
        end_date TEXT,
        link TEXT
    )
    ''')
    
    for tender in tenders:
        cursor.execute('''
        INSERT INTO tenders VALUES (?, ?, ?, ?, ?)
        ''', (tender['name'], tender['organization'], tender['start_date'], 
              tender['end_date'], tender['link']))
    
    conn.commit()
    conn.close()


@app.get("/tenders")
async def get_tenders(max_tenders: int = 100):
    tenders = parse_tenders(max_tenders)
    return {"tenders": tenders}


def main():
    parser = argparse.ArgumentParser(description='Парсер тендеров с B2B-Center')
    parser.add_argument('--max', type=int, default=100, help='Максимальное количество тендеров')
    parser.add_argument('--output', type=str, default='tenders.csv', 
                       help='Файл для сохранения (CSV или SQLite)')
    parser.add_argument('--serve', action='store_true', help='Запустить FastAPI сервер')
    
    args = parser.parse_args()
    
    if args.serve:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        tenders = parse_tenders(args.max)
        
        if args.output.endswith('.csv'):
            save_to_csv(tenders, args.output)
        elif args.output.endswith('.sqlite') or args.output.endswith('.db'):
            save_to_sqlite(tenders, args.output)
        else:
            print("Неподдерживаемый формат файла. Используйте .csv или .sqlite/.db")


if __name__ == '__main__':
    main()
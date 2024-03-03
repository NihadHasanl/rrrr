import requests
from bs4 import BeautifulSoup
import sqlite3

class Database:
    def __init__(self, db_name='websites.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS websites
                            (id INTEGER PRIMARY KEY, url TEXT)''')
        self.conn.commit()

    def add_website(self, url):
        self.cursor.execute("INSERT INTO websites (url) VALUES (?)", (url,))
        self.conn.commit()

    def get_websites(self):
        self.cursor.execute("SELECT * FROM websites")
        return self.cursor.fetchall()

    def clear_history(self):
        self.cursor.execute("DELETE FROM websites")
        self.conn.commit()
        print("История удалена.")

class WebsiteParser:
    def __init__(self, url):
        self.url = url

    def parse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all("p")

class UserInterface:
    def __init__(self):
        self.db = Database()

    def run(self):
        while True:
            choice = input("Выберите действие:\n1. Добавить сайт\n2. Поиск информации\n3. Удалить историю\n4. Выход\n")
            if choice == '1':
                url = input("Введите URL сайта: ")
                self.db.add_website(url)
                print("Сайт добавлен.")
            elif choice == '2':
                keyword = input("Введите ключевое слово для поиска: ")
                websites = self.db.get_websites()
                for website in websites:
                    parser = WebsiteParser(website[1])
                    paragraphs = parser.parse()
                    count = 0
                    for paragraph in paragraphs:
                        if keyword in paragraph.get_text():
                            print(f"На сайте {website[1]} найдено '{keyword}' в параграфе:")
                            print(paragraph.get_text())
                            count += 1
                            if count == 3:
                                break
                    if count == 3:
                        break
            elif choice == '3':
                self.db.clear_history()
            elif choice == '4':
                print("Программа завершена.")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()

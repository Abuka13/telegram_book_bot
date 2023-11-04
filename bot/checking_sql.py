import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Выполняем запрос данных
cursor.execute("SELECT * FROM books")

# Получаем все строки результата
rows = cursor.fetchall()

# Обрабатываем результат
for row in rows:
    id = row[0]
    title = row[1]
    genre = row[2]
    price = row[3]
    name = row[4]

    # Делайте с данными, что вам необходимо
    print(f"ID: {id}, Title: {title}, Genre: {genre}, Price: {price}, Name: {name}")

# Закрываем соединение
conn.close()
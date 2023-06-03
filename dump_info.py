import sqlite3
import csv

conn = sqlite3.connect('file:data/mcpdict.db?mode=ro', uri=True)
cursor = conn.cursor()

cursor.execute('SELECT * FROM info')

rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]

with open('data/info.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n', strict=True)
    writer.writerow(column_names)
    for row in rows:
        writer.writerow(row)

conn.close()

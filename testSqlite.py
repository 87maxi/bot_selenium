
import sqlite3
from datetime import datetime



cursor= sqlite3.connect("test.db")

cursor.execute("""
DROP TABLE IF EXISTS selenium;
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS selenium (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	titulo TEXT NOT NULL,
	url TEXT NOT NULL,
	created_at TEXT DEFAULT (datetime('now','localtime')) NOT NULL);
""")

cursor.execute("""insert into selenium(titulo,url) values ( 'titulo', 'url' )""")

data=  {"titulo": "test selenium qwerty", "url":"https://www.tutorialsandyou.com/python/insert-data-python-sqlite-21.html"}


cursor.execute("""insert into selenium(titulo,url) values ( :titulo, :url )""", data) 



data2 = [
   ("titulo 3", "https://www.zabbix.com/features"), 
   ("titulo 4", "https://www.zabbix.com/forum/zabbix-help")

]


cursor.executemany("""insert into selenium(titulo, url) values(?, ?)""", data2)






values = {
    'titulo':'selenium dict', 'url':'https://stackoverflow.com/questions/14108162/python-sqlite3-insert-into-table-valuedictionary-goes-here',
	'titulo':'selenium dict 2', 'url':'https://stackoverflow.com/questions/21981709/error-binding-parameter-0-probably-unsupported-type'
}
cursor.execute(
    '''INSERT INTO selenium ( titulo, url)
     VALUES ( :titulo, :url);''', 
    values
)


data3 = (
   ("titulo 3", "https://www.zabbix.com/features"), 
   ("titulo 4", "https://www.zabbix.com/forum/zabbix-help")

)


cursor.executemany("""insert into selenium(titulo, url) values(?, ?)""", data3)


cursor.commit()
cursor.close()

   
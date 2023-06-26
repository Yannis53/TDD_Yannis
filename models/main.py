import pyodbc

server = 'localhost'
database = 'TDD_Yannis'
username = 'sa'
password = 'Sql2019'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

cursor = conn.cursor()
cursor.execute("SELECT * FROM Book")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

class Main:

    def __init__(self):
        self.books = []
        self.members = []
        self.reservations = []

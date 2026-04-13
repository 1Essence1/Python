import psycopg2

try:
    conn = psycopg2.connect(
        dbname="phonebook",
        user="farkhat",
        password="123",
        host="localhost",
        port="5432"
    )
    print("CONNECTED ✅")
except Exception as e:
    print("ERROR:", e)
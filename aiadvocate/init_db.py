import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS advocates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    specialization TEXT,
    region TEXT,
    phone TEXT,
    email TEXT
)
""")

cur.execute("""
INSERT INTO advocates (full_name, specialization, region, phone, email)
VALUES 
('Aliyev Bekzod', 'family law', 'Tashkent', '+998901234567', 'bekzod@mail.uz'),
('Karimova Dilnoza', 'criminal law', 'Samarkand', '+998909876543', 'dilnoza@mail.uz')
""")

conn.commit()
conn.close()

print("Database yaratildi ✅")
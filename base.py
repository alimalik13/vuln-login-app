# base.py
import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Drop existing table (optional cleanup)
cursor.execute("DROP TABLE IF EXISTS users")

# Create a new users table
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        email TEXT,
        dob TEXT,
        location TEXT
    )
""")

# Insert 20 sample records
sample_data = [
    ("admin", "admin123", "admin@example.com", "1990-01-01", "USA"),
    ("john", "pass123", "john@example.com", "1992-05-10", "UK"),
    ("alice", "alice321", "alice@example.com", "1995-07-22", "Canada"),
    ("bob", "bobpass", "bob@example.com", "1993-03-15", "Germany"),
    ("charlie", "charliepw", "charlie@example.com", "1989-12-01", "France"),
    ("dave", "davepass", "dave@example.com", "1991-06-18", "Australia"),
    ("eve", "evepass", "eve@example.com", "1994-04-25", "Brazil"),
    ("frank", "frankie", "frank@example.com", "1996-09-30", "Italy"),
    ("grace", "gracepw", "grace@example.com", "1997-08-12", "Spain"),
    ("hank", "hankpass", "hank@example.com", "1998-11-23", "Mexico"),
    ("irene", "irene123", "irene@example.com", "1990-02-05", "India"),
    ("jack", "jackpw", "jack@example.com", "1993-10-09", "China"),
    ("kate", "katepw", "kate@example.com", "1992-03-03", "Pakistan"),
    ("leo", "leopw", "leo@example.com", "1991-07-04", "Russia"),
    ("maya", "mayapw", "maya@example.com", "1994-01-17", "Japan"),
    ("nina", "ninapw", "nina@example.com", "1995-11-19", "Sweden"),
    ("omar", "omarpw", "omar@example.com", "1996-12-20", "Egypt"),
    ("paul", "paulpw", "paul@example.com", "1997-05-08", "Turkey"),
    ("quinn", "quinnpw", "quinn@example.com", "1998-06-14", "Norway"),
    ("rose", "rosepw", "rose@example.com", "1999-09-01", "UAE")
]

cursor.executemany("INSERT INTO users (username, password, email, dob, location) VALUES (?, ?, ?, ?, ?)", sample_data)
conn.commit()
conn.close()

print("[+] Database created and populated with 20 records.")
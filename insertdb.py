import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="honyakuyouyaku",
    user="・・・",
    password="・・・"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE  urltable(
    id SERIAL PRIMARY KEY, 
    page_url VARCHAR(5000) NOT NULL, 
    page_title VARCHAR(5000) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


conn.commit()
conn.close()
import sqlite3

from utils import hash
import settings


DB_NAME = settings.envvars.database_name


def setup():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS 
        posts(id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL, body TEXT NOT NULL)''')
    
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS 
        users(id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    
    conn.commit()

    cur.close()
    conn.close()

def new_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    res = None

    password = hash(password)

    try:
        cur.execute(
        '''INSERT INTO users(email, password) VALUES (?, ?) RETURNING *''', (email, password))
    except sqlite3.IntegrityError:
        res = 'integrity error while inserting.'
    
    if not res:
        res = cur.fetchone()
    
    conn.commit()

    

    cur.close()
    conn.close()
    return res

def get_user(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM users WHERE id = ?''', (str(id)))
    
    usr = cur.fetchone()

    cur.close()
    conn.close()
    return usr

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    #print(email,'-------', type(email))
    cur.execute(
        '''SELECT * FROM users WHERE email = ?''', (email,))
    
    usr = cur.fetchone()

    cur.close()
    conn.close()
    return usr

def new_post(title, body):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    res = None
    try:
        cur.execute(
        '''INSERT INTO posts(title, body) VALUES (?, ?) RETURNING *''', (title, body))
    except sqlite3.IntegrityError:
        res = 'integrity error while inserting.'
    

    if not res: 
        res = cur.fetchone()
    
    conn.commit()

    

    cur.close()
    conn.close()
    return res

def get_posts():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM posts''')
    
    posts = cur.fetchall()

    cur.close()
    conn.close()
    return posts

def get_post(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM posts WHERE id = ?''', (str(id)))
    
    post = cur.fetchone()

    cur.close()
    conn.close()
    return post

def delete_post(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''DELETE FROM posts WHERE id = ? RETURNING *''', (str(id)))
    
    post = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()
    return post

def update_post(id, title, body):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        '''UPDATE posts SET title = ?, body = ? WHERE id = ? RETURNING *''', 
        (title, body, str(id)))
    
    post = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()
    return post
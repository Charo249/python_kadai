import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(name,password):
    sql = 'INSERT INTO user_acc VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (name,hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

#図書登録
def insert_book(title,writer,company,isbn):
    connection = get_connection()
    cursor = connection.cursor()
    print(f'title:{title}, weiter:{writer}, {company}, {isbn}')
    try :
        sql = "INSERT INTO book_kadai VALUES(%s, %s, %s, %s)"

        cursor.execute(sql, (title, writer, company, int(isbn)))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

    #図書一覧
def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title, writer, company, isbn FROM book_kadai"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

#図書削除
def delete_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM book_kadai WHERE title =%s"
    
    cursor.execute(sql,(title,))
    connection.commit()
    
    cursor.close()
    connection.close()

#図書更新
def update_book(oldtitle, title,writer,company,isbn):
    connection = get_connection()
    cursor = connection.cursor()
    try :
        #sql = "UPDATE book_kadai SET title = 'sample233', writer = 22, company = 11, isbn = 33 where title = 'sample23'"
        sql = 'UPDATE book_kadai SET title = %s, writer = %s, company = %s, isbn = %s where title = %s'
        print(f'title:{title}, weiter:{writer}, {company}, {isbn}')
        cursor.execute(sql, (title, writer, company, int(isbn), oldtitle))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        print('error')
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

#図書検索
def search_books(keyword):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT * FROM book_kadai WHERE title LIKE %s"
        cursor.execute(sql, (keyword))
        count = cursor.fetchall()
        
        
    except psycopg2.DatabaseError:
        print("検索中にエラーが発生しました:")
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count

#ログイン
def login(name,password):
    sql = 'SELECT hashed_passward, salt FROM user_acc WHERE name = %s'
    flg = False
    try :
        connection = get_connection()
        cursor = connection.cursor()
        print(f'name:{name}')
        cursor.execute(sql, (name,))
        print("sql")
        user = cursor.fetchone()
        
        print(f'user{user}')
  
        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()
        print('処理終了')
        return flg
    
    
    
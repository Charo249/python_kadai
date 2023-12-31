import os, psycopg2,string,random,hashlib

def get_connection():
    url =os.environ['DATEBASE_URL']
    connection=psycopg2.connect(url)
    return connection

def insert_user(user_name,mail, password):
    sql='INSERT INTO user VALUES (default, %s, %s, %s, %s)'
    
    salt= get_salt() # ソルトの生成
    hashed_password = get_hash(password, salt) # 生成したソルトでハッシュ
    
    try : # 例外処理
        connection=get_connection()
        cursor=connection.cursor()
    
        cursor.execute(sql, (user_name,mail, hashed_password,salt))
        count=cursor.rowcount# 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count=0# 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()

    return count

# ランダムなソルトを生成
def get_salt():
# 文字列の候補(英大小文字+ 数字)
    charset=string.ascii_letters+string.digits
# charset からランダムに30文字取り出して結合
    salt=''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw=bytes(password, "utf-8")
    b_salt=bytes(salt, "utf-8")
    hashed_password=hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password
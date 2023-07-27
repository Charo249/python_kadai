# [エラーにならない方法（スクリプト更新時）]
# ターミナルにて
# python app と入力
# Tab 2回押す
# python .\app2.py を実行

from flask import Flask, render_template, request, redirect, url_for,session
from datetime import timedelta
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('login.html')
    else :
        return render_template('login.html', msg=msg)

#ログイン aaa

@app.route('/', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')

    # ログイン判定
    if db.login(name,password):
        session['user'] = True      # session にキー：'user', バリュー:True を追加
        session.permanent = True    # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=3)   # session の有効期限を 3分に設定
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'name':name,'password':password}
        return render_template('login.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('login'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    name = request.form.get('name')
    password = request.form.get('password')

    if name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, name=name,password=password)

    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(name,password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('login', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

#図書登録
@app.route('/bookregi')
def book_register():
    return render_template('bookregi.html')

@app.route('/book_register_exe', methods=['POST'])
def book_register_exe():
    title = request.form.get('title')
    writer = request.form.get('writer')
    company = request.form.get('company')
    isbn = request.form.get('isbn')
           
    count = db.insert_book(title, writer, company, isbn)
           
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('mypage', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('bookregi.html', error=error)

#図書一覧
@app.route('/bookall')
def book_all():
    book_all = db.select_all_books()
    return render_template('bookall.html', books=book_all)

@app.route('/returnbookall')
def return_bookall():
    return render_template('mypage.html')

#図書削除
@app.route('/book_del')
def book_delete():
    return render_template('bookdel.html')

@app.route('/book_select_delete', methods=['POST'])
def book_select_delete():
    title = request.form.get('book_title')
    count = db.delete_book(title)
  
    if count == 1:
        msg = '削除が完了しました。'
        return redirect(url_for('mypage', msg=msg))
    else:
        error = '削除に失敗しました。'
        return render_template('bookdel.html', error=error)

#図書検索
@app.route('/book_sear')
def book_search():
    return render_template('booksear.html')

@app.route('/book_search_exe', methods=['POST'])
def book_search_exe():

    keyword = request.form.get('title')
    count = db.search_books(keyword)

    if count:
        return redirect(url_for('booksear', book2=count))
    else:
        error=("該当するデータが見つかりませんでした。")
        return render_template('booksea_f.html', error=error)





    


#図書更新
@app.route('/bookup')
def book_update():
    return render_template('bookup.html')

@app.route('/book_update_exe', methods=['POST'])
def book_update_exe():
    oldtitle = request.form.get('oldtitle')
    print(oldtitle)
    title = request.form.get('title')
    writer = request.form.get('writer')
    company = request.form.get('company')
    isbn = request.form.get('isbn')
    count = db.update_book(oldtitle ,title,writer,company,isbn)
           
    if count == 1:
        msg = '更新が完了しました。'
        return redirect(url_for('mypage', msg=msg))
    else:
        error = '更新に失敗しました。'
        return render_template('bookup.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)   # session の破棄
    return redirect(url_for('index'))   # ログイン画面にリダイレクト



if __name__ == '__main__':
    app.run(debug=True)
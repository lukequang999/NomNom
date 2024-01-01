from flask import Flask, render_template, request, redirect, url_for
import os
import pyodbc

app = Flask(__name__, template_folder=os.path.abspath('C:\\Users\\Administrator\\Desktop\\NomNom-main\\NomNom-main'))

server = 'DESKTOP-9S1RJDI'
database = 'ArticleDatabase'
username = 'Admin'
password = ''

try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = conn.cursor()
    print('success')
except:
    print('false')

# Dữ liệu tài khoản người dùng
user_accounts = {'admin': '1234', 'guest': 'password','member':'1234'}

@app.route('/')
def home():
    return render_template('NomNom-main/index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in user_accounts and user_accounts[username] == password:
        if username == 'admin':
            # Nếu là admin, chuyển hướng đến trang Dashboard
            return redirect(url_for('dashboard'))
        if username == 'member':
            return redirect(url_for('member'))
        else:
            # Nếu là người dùng khác, chuyển hướng đến trang home
            return redirect(url_for('home', username=username))
    else:
        # Nếu thông tin đăng nhập không chính xác, chuyển hướng lại trang đăng nhập
        return redirect(url_for('home'))

@app.route('/article/<int:ID_article>')
def display_article(ID_article):
    cursor.execute('SELECT Title, Content FROM Articles WHERE ID_article = ?', (ID_article,))
    article = cursor.fetchone()

    if article is None:
        return 'Article not found'
    
    return render_template('NomNom-main/templates/content.html', article=article)


@app.route('/content_manage/<int:ID_User>')
def display_list(ID_User):
    cursor.execute('SELECT Title, ID_article FROM Articles WHERE ID_user = ?', (ID_User,))
    articles = cursor.fetchall()

    return render_template('NomNom-main/templates/ContentManage.html', articles=articles)

@app.route('/delete_article/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        cursor.execute("DELETE FROM Articles WHERE ID_article = ?", (article_id,))
        conn.commit()

        return '', 204
    except pyodbc.Error as e:
        print(f'Error deleting article: {e}')
        return '', 500
    
@app.route('/addcontent', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        author = request.form['author']

        try:
            cursor.execute("SELECT ID_user FROM User_Accounts WHERE Username = ?", author)
            
            row = cursor.fetchone()
            if row is None:
                return 'Người dùng không tồn tại.'
            
            user_id = row[0]

            cursor.execute("INSERT INTO Articles (ID_user, Title, Content, Descript) VALUES (?, ?, ?, ?)",(user_id, title, content, description))

            return 'Bài viết đã được thêm thành công!'
        
        except pyodbc.Error as e:
                return f'Lỗi khi thêm bài viết: {str(e)}'
    
    return render_template('NomNom-main/templates/AddContent.html')

@app.route('/editcontent/<int:ID_user>/<int:ID_Article>', methods=['GET', 'POST'])
def edit_article(ID_User,ID_Article):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        author = request.form['author']

    try:
        cursor.execute("SELECT ID_user FROM User_Accounts WHERE ID_user = ?", (ID_User,))          
        row = cursor.fetchone()
        if row is None:
            return 'Người dùng không tồn tại.'

        else:
            cursor.execute("SELECT Username FROM User_Accounts WHERE ID_user = ?", (ID_User,))
            row_1 = cursor.fetchone()
            author = row_1[0]
            cursor.execute('SELECT Title, Content, Descript FROM Articles WHERE ID_user = ? AND ID_article = ?', (ID_User,ID_Article,))
            row_2 = cursor.fetchone()

            title = row_2[0]
            content = row_2[1]
            description = row_2[2]

            return render_template('NomNom-main/templates/EditContent.html',title=title, content=content, description=description, author=author)
      
    except pyodbc.Error as e:
        return f'Lỗi khi { "cập nhật" if ID_Article else "thêm"} bài viết: {str(e)}'

if __name__ == '__main__':
    app.run()
    
@app.route('/dashboard')
def dashboard():
    return render_template('NomNom-main/templates/dashboard.html')

@app.route('/member')
def member():
    return render_template('NomNom-main/templates/member.html')

if __name__ == '__main__':
    app.run(debug=True)
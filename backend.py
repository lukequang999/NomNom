from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pyodbc

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'nhatquang3391'
login_manager = LoginManager(app)
login_manager.login_view = 'form_login'

server = 'DESKTOP\Q'
database = 'ArticleDatabase'
username = 'Administrator'
password = ''

try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = conn.cursor()
    print('Kết nối database thành công'.encode('utf-8'))
except Exception as e:
    print('Kết nối database thất bại:'.encode('utf-8'), str(e))

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    # Truy vấn CSDL để lấy thông tin người dùng
    query = 'SELECT * FROM User_Accounts WHERE ID_user = ?'
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = User(user_data.ID_user, user_data.Username, user_data.Email, user_data.Pass_word)
        return user
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Truy vấn CSDL để kiểm tra đăng nhập
        query = 'SELECT * FROM User_Accounts WHERE Username = ? AND Pass_word = ?'
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user = load_user(user_data.ID_user)
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Tên người dùng hoặc mật khẩu không đúng.'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Truy vấn CSDL để kiểm tra xem email hoặc tên người dùng đã được sử dụng chưa
        check_query = 'SELECT * FROM User_Accounts WHERE Email = ? OR Username = ?'
        cursor.execute(check_query, (email, username))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'Email hoặc tên người dùng đã được sử dụng. Vui lòng chọn email hoặc tên người dùng khác.'
            flash(error, 'danger')
            return render_template('login.html', error=error)
        else:
            # Thêm người dùng mới vào CSDL
            insert_query = 'INSERT INTO User_Accounts (Username, Email, Pass_word) VALUES (?, ?, ?)'
            cursor.execute(insert_query, (username, email, password))
            conn.commit()
            flash('Tạo tài khoản thành công!', 'success')
            return redirect(url_for('login'))

    return render_template('login.html', error=error)
@app.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username
    return render_template('dashboard.html', username=username)

@app.route('/member')
@login_required
def member():
    # Truy vấn CSDL để lấy danh sách bài viết của người dùng
    query = 'SELECT ID_article, Title, Content, Descript FROM Articles WHERE ID_user = ?'
    cursor.execute(query, (current_user.get_id(),))
    articles = cursor.fetchall()

    return render_template('member.html', current_user=current_user, articles=articles)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/form_login')
def form_login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_article/<int:article_id>', methods=['DELETE'])
@login_required
def delete_article(article_id):
    try:
        cursor.execute("DELETE FROM Articles WHERE ID_article = ?", article_id)
        conn.commit()
        return "Bài viết đã được xóa thành công"
    except Exception as e:
        print("Đã xảy ra lỗi khi xóa bài viết:", e)
        return "Đã xảy ra lỗi khi xóa bài viết"

@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        author = current_user.username

        try:
            # Truy vấn CSDL để lấy ID_user
            query_user_id = 'SELECT ID_user FROM User_Accounts WHERE Username = ?'
            cursor.execute(query_user_id, (author,))
            row = cursor.fetchone()

            if row is None:
                return 'Người dùng không tồn tại.'

            user_id = row[0]

            # Truy vấn CSDL để thêm bài viết
            query_insert = 'INSERT INTO Articles (ID_user, Title, Content, Descript) VALUES (?, ?, ?, ?)'
            cursor.execute(query_insert, (user_id, title, content, description))
            conn.commit()

            flash('Bài viết đã được thêm thành công!', 'success')
            # Tạm thời thoát ra phần bài DS bài viết
            return redirect(url_for('member', ID_User=user_id))

        except pyodbc.Error as e:
            flash(f'Lỗi khi thêm bài viết: {str(e)}', 'danger')

    return render_template('AddContent.html')

@app.route('/article/<int:ID_article>')
def display_article(ID_article):
    cursor.execute('SELECT Title, Content FROM Articles WHERE ID_article = ?', (ID_article,))
    article = cursor.fetchone()

    if article is None:
        return 'Article not found'
    return render_template('content.html', article=article)

app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        author = current_user.username

        try:
            # Truy vấn CSDL để lấy ID_user
            query_user_id = 'SELECT ID_user FROM User_Accounts WHERE Username = ?'
            cursor.execute(query_user_id, (author,))
            row = cursor.fetchone()
            if row is None:
                    return 'Người dùng không tồn tại.'
            
            user_id = row[0]

            query_update = "UPDATE Articles SET Title=?, Content=?, Descript=? WHERE ID_article=?"
            cursor.execute(query_update, (title, content, description, article_id))
            conn.commit()
            
            flash('Chỉnh sửa bài viết thành công!', 'success')

            return redirect(url_for('member', ID_User=user_id))
        
        except pyodbc.Error as e:
            flash(f'Lỗi khi sửa bài viết: {str(e)}', 'danger')
    
    return render_template('member.html')

@app.route('/edit-account', methods=['GET'])
@login_required
def edit_account():
    return render_template('AccountManager.html')

@app.route('/update-account', methods=['POST'])
@login_required
def update_account():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    query_update = "UPDATE User_Accounts SET Username = ?, Email = ?, Pass_word = ? WHERE ID_user = ?"
    cursor.execute(query_update,(username, email, password, current_user.id))
    conn.commit()

    flash('Account updated successfully!', 'success')
    return redirect(url_for('member'))

@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    print(current_user.id)
    query_delete_content = "DELETE FROM Articles WHERE ID_user = ?"
    cursor.execute(query_delete_content,(current_user.id))

    query_delete_accont = "DELETE FROM User_Accounts WHERE ID_user = ?"
    cursor.execute(query_delete_accont,(current_user.id))
    conn.commit()

    logout_user()

    flash('Account deleted successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
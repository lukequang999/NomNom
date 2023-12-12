from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dữ liệu tài khoản người dùng
user_accounts = {'admin': '1234', 'guest': 'password'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in user_accounts and user_accounts[username] == password:
        if username == 'admin':
            # Nếu là admin, chuyển hướng đến trang Dashboard
            return redirect(url_for('dashboard', username=username))
        else:
            # Nếu là người dùng khác, chuyển hướng đến trang home
            return redirect(url_for('home', username=username))
    else:
        # Nếu thông tin đăng nhập không chính xác, chuyển hướng lại trang đăng nhập
        return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder=os.path.abspath('C:\\Users\\trann\\OneDrive\\Desktop\\NomNom-main\\NomNom'))

# Dữ liệu tài khoản người dùng
user_accounts = {'admin': '1234', 'guest': 'password','member':'1234'}

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
            return redirect(url_for('dashboard'))
        if username == 'member':
            return redirect(url_for('member'))
        else:
            # Nếu là người dùng khác, chuyển hướng đến trang home
            return redirect(url_for('home', username=username))
    else:
        # Nếu thông tin đăng nhập không chính xác, chuyển hướng lại trang đăng nhập
        return redirect(url_for('home'))
    


@app.route('/dashboard')
def dashboard():
    return render_template('static/dashboard.html')
@app.route('/member')
def member():
    return render_template('static/member.html')

if __name__ == '__main__':
    app.run(debug=True)

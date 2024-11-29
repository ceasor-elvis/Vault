from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, File
from cyp import upload_files, generate_key, download_files

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vault.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/vault', methods=['GET', 'POST'])
@login_required
def vault():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            new_filename = upload_files(app.config['UPLOAD_FOLDER'], file, current_user.key)
            new_file = File(
                original_filename = file.filename,
                encrypt_filename = new_filename,
                user_id = current_user.id
            )
            db.session.add(new_file)
            db.session.commit()

    data = current_user   
    return render_template("vault.html", data=data)

@app.route('/download/<int: file_id>', methods=['GET', 'POST'])
def download(file_id):
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    d_link = download_files(app.config['UPLOAD_FOLDER'], file.original_filename, file.encrypt_filename, current_user.key)
    return redirect(d_link)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['password']

        try:
            new_user = User(username=username, password=password, key=generate_key())
            db.session.add(new_user)
            db.session.commit()
        except:
            flash("Username is already in use")
            return redirect(url_for('signup'))
        flash("Signup successful! You can login in now.")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash(f"Welcome back, {user.username}")
            return redirect(url_for("vault"))
        flash("Login failed. Check your credentials.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
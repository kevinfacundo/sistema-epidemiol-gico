from flask import Flask, render_template
from flask_mysqldb import MySQLdb
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__,  static_url_path= '/static' )
load_dotenv()

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

#Configuracion de flask_login
app.secret_key= "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesion para acceder"


#Modelo de usuario
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor
    cur.execute("SELECT id, email, password FROM users WHERE id = %s", (user_id))
    user = cur.fetchone()
    cur.close()
    if user:
        return User (user[0], user[1], user[2])
    return None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        email = request.form['email']
        cur = mysql.connection.cursor
        cur.execute('SELECT id , email, password FROM users WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            user_obj = User(user[0], user[1],user[2])
            login_user(user_obj)
            flash('Login', 'success')

@app.route('/edit/<id>')
def get_client(id):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM contact WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-cliente.html', usuarios = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_cliente(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute ("""UPDATE """)
        
        
if __name__ == '__main__':
    init_db()
    App.run(port=5000, debug=True)
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__, static_folder='Static', template_folder='Templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wintech:17012021@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(success=False, message='Email e senha são obrigatórios')

    if User.query.filter_by(email=email).first():
        return jsonify(success=False, message='Usuário já existe')

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(success=True, message='Cadastro realizado com sucesso!')

if __name__ == '__main__':
    app.run(debug=False)
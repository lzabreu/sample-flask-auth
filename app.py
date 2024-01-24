from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['secret_key'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data['username']
  password = data['password']

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({'message': 'Login efetuado com sucesso'}), 200

    return jsonify({'message': 'Credenciais Incorretas'}), 401

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logout efetuado com sucesso'}), 200

@app.route('/user', methods=['POST'])
def create_user():
  data = request.get_json()
  username = data['username']
  password = data['password']

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'}), 200


@app.route('/hello', methods=['GET'])
def hello():
  return 'Hello, World!'

if __name__ == '__main__':
  app.secret_key = 'secret'
  app.run(debug=True)
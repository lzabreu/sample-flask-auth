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
#@login_required
def create_user():
  data = request.get_json()
  username = data['username']
  password = data['password']

  if username and password:
    if User.query.filter_by(username=username).first():
      return jsonify({'message': 'Usuário ja existe'}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'}), 200
  return jsonify({'message': 'Credenciais Incorretas'}), 401

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
  user = User.query.get(user_id)
  if user:
    return jsonify({'username': user.username}), 200
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
  user = User.query.get(user_id)
  if user:
    data = request.get_json()
    user.username = data['username']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
  user = User.query.get(user_id)
  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200
  return jsonify({'message': 'Usuário não encontrado'}), 404


if __name__ == '__main__':
  app.secret_key = 'secret'
  app.run(debug=True)
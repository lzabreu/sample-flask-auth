from flask import Flask
from models.user import User
from database import db

app = Flask(__name__)
app.config['secret_key'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

db.init_app(app)

@app.route('/hello', methods=['GET'])
def hello():
  return 'Hello, World!'

if __name__ == '__main__':
  app.run(debug=True)
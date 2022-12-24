from flask import Flask  
from flask_cors import CORS
from dbLayer import db 
from customers import customers
from books import books
from loans import loans


app = Flask(__name__)
app.register_blueprint(customers)
app.register_blueprint(books)
app.register_blueprint(loans)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"

db.init_app(app)

@app.route('/')
def index():
    return "hello"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Message {self.recipient}: {self.content}"


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

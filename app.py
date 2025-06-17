from flask import Flask, jsonify
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


@app.route("/messages")
def get_unread_messages():
    unread_messages = Message.query.filter_by(is_read=False).all()
    return_msg = []
    for message in unread_messages:
        message.is_read = True
        db.session.commit()
        return_msg.append(str(message))
    return return_msg


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

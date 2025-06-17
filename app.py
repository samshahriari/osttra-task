from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f"Message {self.message_id} at {self.timestamp} to {self.recipient}: {self.content}"


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


@app.route("/messages", methods=['POST'])
def add_message():
    message = Message(recipient=request.json['recipient'], content=request.json['content'], timestamp=datetime.datetime.now())
    db.session.add(message)
    db.session.commit()
    return str(message.message_id)


@app.route("/messages/<message_id>", methods=['DELETE'])
def delete_single_message(message_id):
    message = Message.query.get(message_id)
    if not message:
        return f"Message {message_id} not found!"
    db.session.delete(message)
    db.session.commit()
    return f"Message {message_id} deleted successfully!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

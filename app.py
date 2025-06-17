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

    def get_dict(self):
        return {
            'message_id': self.message_id,
            'recipient': self.recipient,
            'content': self.content,
            'is_read': self.is_read,
            'timestamp': self.timestamp.isoformat()
        }


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/messages/unread", methods=['GET'])
def get_unread_messages():
    unread_messages = Message.query.filter_by(is_read=False).all()
    return_msg = []
    for message in unread_messages:
        return_msg.append(message.get_dict())
        message.is_read = True
        db.session.commit()
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


@app.route("/messages", methods=['DELETE'])
def delete_multiple_messages():
    message_ids = request.json.get('message_ids', None)
    if not message_ids or not isinstance(message_ids, list):
        return "'message_ids' must be a list!"
    messages = Message.query.filter(Message.message_id.in_(message_ids)).all()
    if not messages:
        return "No messages found for the specified IDs!"
    deleted_ids = []
    for message in messages:
        deleted_ids.append(message.message_id)
        db.session.delete(message)
    db.session.commit()
    return f"Messages {', '.join(map(str, deleted_ids))} deleted successfully!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

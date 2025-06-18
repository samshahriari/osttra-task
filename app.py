from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Message(db.Model):
    """
    Class to represent a message in the database.
    Attributes:
        message_id (int): Unique identifier for the message.
        recipient (str): Email address of the message recipient.
        content (str): Content of the message.
        is_read (bool): Flag indicating whether the message has been read.
        timestamp (datetime): Timestamp when the message was created.
    """
    message_id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)

    def get_dict(self):
        """        
        Convert the message object to a dictionary format.
        Returns:
            dict: Dictionary representation of the message.
        """
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
    """
    Fetch all unread messages and mark them as read.
    Returns:
        List of unread messages in JSON format.
    """
    unread_messages = Message.query.filter_by(is_read=False).all()
    return_msg = []
    for message in unread_messages:
        return_msg.append(message.get_dict())
        message.is_read = True
    db.session.commit()
    return return_msg


@app.route("/messages", methods=['POST'])
def add_message():
    """
    Add a new message to the database.
    Request Body:
    ```
        {
            "recipient": "test@example.com",
            "content": "Hello, how are you?"
        }
    ```
    Returns:
        The ID of the newly created message.
    """
    message = Message(recipient=request.json['recipient'], content=request.json['content'], timestamp=datetime.datetime.now())
    db.session.add(message)
    db.session.commit()
    return str(message.message_id)


@app.route("/messages/<message_id>", methods=['DELETE'])
def delete_single_message(message_id):
    """
    Delete a single message by its ID.
    Args:
        message_id (int): The ID of the message to be deleted.
    Returns:
        Status message indicating whether the deletion was successful or not.
        """
    message = Message.query.get(message_id)
    if not message:
        return f"Message {message_id} not found!"
    db.session.delete(message)
    db.session.commit()
    return f"Message {message_id} deleted successfully!"


@app.route("/messages", methods=['DELETE'])
def delete_multiple_messages():
    """
    Delete multiple messages based on a list of message IDs provided in the request body.
    Request Body:
    ```
        {
            "message_ids": [1, 2, 3]
        }
    ```
    Returns:
        Status message indicating which messages were deleted.
    """
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


@app.route("/messages", methods=['GET'])
def get_multiple_messages():
    """
    Fetch messages (including previously fetched) ordered by time, according to start
    and/or stop index.

    Query Parameters:
        from_index (int, optional): Starting index for message to be fetched. If not provided, returns from index 0.
        to_index (int, optional): Ending index for message to be fetched (not included). If not provided, returns all messages from the starting index.
    Returns:
        List of messages in JSON format.
    """
    from_index = request.args.get('from_index', type=int, default=None)
    to_index = request.args.get('to_index', type=int, default=None)

    messages = Message.query.order_by(Message.timestamp).slice(from_index, to_index)
    return_msg = []
    for message in messages:
        return_msg.append(message.get_dict())
    return return_msg


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# osttra-task

## Setup
1. Install the requirements in [requirements.txt](./requirements.txt), preferably in a virtual environment.
2. Start the web server with `python3 app.py`. It should automatically create the SQLite database.
3. You can now make REST requests to the server with curl. Default address: `http://127.0.0.1:5000`. See below for targets.

## Features
#### Submit a message to a defined recipient
Send a POST request to `/messages` with the following json body:
```json
{
    "recipient": "test@example.com",
    "content": "Hello, how are you?"
}
```

#### Fetch unread messages.
Send a GET request to `/messages/unread`.

Assumptions:
- When a message is fetched it is marked as read.

#### Delete a single message.
Send a DELETE request to `/messages/<id>`

#### Delete multiple messages
Send a DELETE request to `/messages` with the following json body:
```json
{
    "message_ids": [1, 2, 3]
}
```

####  Fetch messages (including previously fetched) ordered by time, according to start and/or stop index
Send a GET request to `/messages?from_index=<index>&to_index=<index>`

## Next steps
- Return HTTP response status codes
- Implement error handling
- Implement tests
- Use a scalable database
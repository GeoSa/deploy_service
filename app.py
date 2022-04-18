import os
from flask import Flask, request, jsonify

app = Flask(__name__)
AUTH_TOKEN = os.getenv('AUTH_TOKEN', None)


@app.route('/', methods=['POST'])
def process_webhook():
    if request.headers.get('Authorization', '') != AUTH_TOKEN:
        return jsonify({'message': 'Bad token'}), 401

    return jsonify({'message': 'Deploy complete'}), 200


if __name__ == '__main__':
    app.run()

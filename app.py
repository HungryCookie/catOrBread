from flask import Flask, jsonify, request, abort
import main

app = Flask(__name__)


@app.route('/cb', methods=['POST'])
def post_data():
    if not request.json:
        abort(400)
    chat_id = request.json['user_id']
    user_answer = request.json['answer']
    a = main.Main(chat_id, user_answer)
    return a.get_response(), 201


if __name__ == '__main__':
    app.run()

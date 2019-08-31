from flask import Flask, request, abort
from main import Main
from SQLiter import SQLiter
import const

app = Flask(__name__)


@app.route('/game', methods=['POST'])
def post_data():
    if not request.json:
        abort(400)

    db = SQLiter(const.DATABASE_NAME)

    body = request.json
    chat_id = body.get('user_id')
    user_answer = body.get('answer')

    a = Main(chat_id, user_answer, db)
    db.close()
    return a.get_response(), 200


@app.route('/', methods=['GET'])
def get_data():
    return const.NOTHING_HERE_YET


if __name__ == '__main__':
    app.run(host='0.0.0.0')

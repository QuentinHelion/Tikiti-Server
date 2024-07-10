""" 
Main app file, all api route are declared there
"""

from flask import Flask, jsonify
from application.interfaces.controllers.database_controller import DatabaseController
from infrastructure.data.env_reader import EnvReader

dotenv = EnvReader()
db_controller = DatabaseController(
    host=dotenv.get("DB_HOST"),
    database=dotenv.get("DB_NAME"),
    user=dotenv.get("DB_USER"),
    password=dotenv.get("DB_PASS")
)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    bla bla bla
    """
    return jsonify({
        "status": "200",
        "response": "pong"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
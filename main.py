""" 
Main app file, all api route are declared there
"""

from flask import Flask, request, jsonify
from application.interfaces.controllers.database_controller import DatabaseController
from application.use_cases.create_user import CreateUser
from infrastructure.data.env_reader import EnvReader

dotenv = EnvReader()
db_controller = DatabaseController(
    host=dotenv.get("DB_HOST"),
    database=dotenv.get("DB_NAME"),
    user=dotenv.get("DB_USER"),
    password=dotenv.get("DB_PASS")
)

app = Flask(__name__)


@app.route('/auth/signup', methods=['GET'])
def signup():
    """
    Create user
    """
    uc_create_user = CreateUser(controller=db_controller)
    result = uc_create_user.create(
            username=request.args["username"],
            email=request.args["email"],
            password=request.args["password"]
        )
    
    return jsonify({
        "status": "200" if result else "500",
        "repsonse": result
    })



if __name__ == '__main__':
    app.run(debug=True)

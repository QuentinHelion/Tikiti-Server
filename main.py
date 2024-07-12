""" 
Main app file, all api route are declared there
"""

from flask import Flask, request, jsonify, abort
from application.interfaces.controllers.database_controller import DatabaseController
from application.use_cases.auth_user import UserAuthentication
from application.use_cases.create_user import CreateUser
from infrastructure.data.env_reader import EnvReader
from infrastructure.data.token import generate_token

dotenv = EnvReader()
db_controller = DatabaseController(
    host=dotenv.get("DB_HOST"),
    database=dotenv.get("DB_NAME"),
    user=dotenv.get("DB_USER"),
    password=dotenv.get("DB_PASS")
)

app = Flask(__name__)
TOKEN_SIZE = 16
USERS_TOKENS = []


@app.route('/auth/signup', methods=['GET'])
def signup():
    """
    Create user
    """

    if "email" not in request.args or "password" not in request.args or "username" not in request.args:
        abort(
                code=400,
                description=jsonify({
                    "status": "400",
                    "message": "Missing args"
                })
            )
        
    uc_create_user = CreateUser(controller=db_controller)
    result = uc_create_user.create(
            username=request.args["username"],
            email=request.args["email"],
            password=request.args["password"]
        )
    
    return jsonify({
        "status": "200" if result else "500",
        "repsonse": result
    }), 200 if result else 500

@app.route('/auth/login', methods=['GET'])
def login():
    """
    User login
    :return: token
    """

    uc_auth_user = UserAuthentication(
        db_controller=db_controller
    )

    if "email" not in request.args or "password" not in request.args:
        abort(
                code=400,
                description=jsonify({
                    "status": "400",
                    "message": "Missing args"
                })
            )

    result = uc_auth_user.login(
        email=request.args["email"],
        password=request.args["password"]
    )

    if result:
        token = generate_token(TOKEN_SIZE)
        USERS_TOKENS.append(token)
        return jsonify({
            "status": "200",
            "repsonse": token
        }), 200

    else:
        return jsonify({
            "status": "500",
            "resposne": "Bad credentials"
        }), 500


@app.route('/auth/logout', methods=['GET'])
def disconnect():
    """
    delete user token from USERS_TOKEN array
    """
    if "token" not in request.args:
        return jsonify({
            "status": "400",
            "response": "Missing token"
        }), 400
    token = request.args["token"]
    USERS_TOKENS.remove(token)
    return jsonify({
        "status": "200",
        "message": "Successfully disconnected"
    }), 200



if __name__ == '__main__':
    app.run(debug=True)

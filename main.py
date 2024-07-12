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
EXCLUDED_ROUTES = ["/auth/login", "/auth/logout","/auth/signup"]


@app.before_request
def before_request():
    """
    Before request, check if token is give and if it is valid
    """
    if request.path not in EXCLUDED_ROUTES:
        if "token" in request.args:
            if request.args["token"] not in USERS_TOKENS:
                abort(
                    code=401,
                    description=jsonify({
                        "status": "401",
                        "response": "Unautorized"
                    })
                )
        else:
            abort(
                code=401,
                description=jsonify({
                    "status": "401",
                    "response": "Unautorized"
                })
            )


@app.route('/auth/signup', methods=['GET'])
def signup():
    """
    Create user
    """

    if ("email" not in request.args
            or "password" not in request.args
            or "username" not in request.args):
        abort(
            code=400,
            description=jsonify({
                "status": "400",
                "response": "Missing args"
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
        "response": result
    }), 200 if result else 500


@app.route('/auth/login', methods=['GET'])
def auth_login():
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
                "response": "Missing args"
            })
        )

    result = uc_auth_user.login(
        email=request.args["email"],
        password=request.args["password"]
    )

    if result:
        token = generate_token(TOKEN_SIZE)
        USERS_TOKENS.append({
            "token": token,
            "email": request.args['email']
        })
        return jsonify({
            "status": "200",
            "response": token
        }), 200

    return jsonify({
        "status": "500",
        "response": "Bad credentials"
    }), 500


@app.route('/auth/logout', methods=['GET'])
def auth_logout():
    """
    delete user token from USERS_TOKEN array
    """
    if "token" not in request.args:
        return jsonify({
            "status": "400",
            "response": "Missing token"
        }), 400
    token = request.args["token"]
    print(f"before: {USERS_TOKENS}")
    try:
        USERS_TOKENS.remove(next(item for item in USERS_TOKENS if item['token'] == token))
    except StopIteration:
        print(f"No item found with token: {token}")
        return jsonify({
            "status": "400",
            "response": "Unknown token"
        }), 400
    print(f"after: {USERS_TOKENS}")
    return jsonify({
        "status": "200",
        "response": "Successfully disconnected"
    }), 200


@app.route('/task/add', methods=['GET'])
def task_add():
    """
    add task
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
        "response": "Successfully disconnected"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)

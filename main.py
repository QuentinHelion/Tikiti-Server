""" 
Main app file, all api route are declared there
"""

from flask import Flask, request, jsonify, abort

from application.interfaces.controllers.database_controller import DatabaseController
from application.use_cases.auth_user import UserAuthentication
from application.use_cases.create_user import CreateUser
from application.use_cases.task_management import TaskManager
from infrastructure.data.env_reader import EnvReader
from infrastructure.data.token import generate_token

dotenv = EnvReader()
db_controller = DatabaseController(
    host=dotenv.get("DB_HOST"),
    database=dotenv.get("DB_NAME"),
    user=dotenv.get("DB_USER"),
    password=dotenv.get("DB_PASS")
)
uc_user = UserAuthentication(
    db_controller=db_controller
)

app = Flask(__name__)
TOKEN_SIZE = 16
USERS_TOKENS = [{
    "token": "rr8Rh24Eff1UvRTR",
    "email": "qhel.spam@gmail.com"
}]
EXCLUDED_ROUTES = ["/auth/login", "/auth/logout", "/auth/signup"]


@app.before_request
def before_request():
    """
    Before request, check if token is give and if it is valid
    """
    if request.path not in EXCLUDED_ROUTES:
        if "token" in request.args:
            if uc_user.check_login(request.args["token"], USERS_TOKENS) is False:
                print("Token is not valid")
                abort(
                    code=401,
                    description=jsonify({
                        "status": "401",
                        "response": "Unautorized"
                    })
                )
        else:
            print("Missing token")
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
    if "title" not in request.args and "deadline" not in request.args:
        return jsonify({
            "status": "400",
            "response": "Missing args"
        }), 400

    if "description" not in request.args:
        description = None
    else:
        description = request.args["description"]

    email = uc_user.check_login(
        token=request.args["token"],
        tokens_list=USERS_TOKENS
    )

    uc_task_manager = TaskManager(
        db_controller=db_controller
    )

    result = uc_task_manager.new(
        title=request.args["title"],
        user_id=uc_user.get_user_id(email),
        deadline=request.args["deadline"],
        descript=description
    )

    print(result)

    return jsonify({
        "status": "200" if result else "500",
        "response": "Successfully saved" if result else "Error on save task"
    }), 200 if result else 500


@app.route('/task/update', methods=['GET'])
def task_update():
    """
    Update task
    """
    if ("task_id" not in request.args and "values" not in request.args
            and "columns" not in request.args):
        return jsonify({
            "status": "400",
            "response": "Missing args"
        }), 400

    email = uc_user.check_login(
        token=request.args["token"],
        tokens_list=USERS_TOKENS
    )

    uc_task_manager = TaskManager(
        db_controller=db_controller
    )

    result = uc_task_manager.update(
        task_id=request.args["task_id"],
        user_id=uc_user.get_user_id(email),
        columns=request.args["columns"],
        values=request.args["values"]
    )

    return jsonify({
        "status": "200" if result else "500",
        "response": "Successfully saved" if result else "Error on save task"
    }), 200 if result else 500

@app.route('/task/delete', methods=['GET'])
def task_delete():
    """
    delete task
    """
    if "task_id" not in request.args:
        return jsonify({
            "status": "400",
            "response": "Missing args"
        }), 400

    email = uc_user.check_login(
        token=request.args["token"],
        tokens_list=USERS_TOKENS
    )

    uc_task_manager = TaskManager(
        db_controller=db_controller
    )

    result = uc_task_manager.delete(
        task_id=request.args["task_id"],
        user_id=uc_user.get_user_id(email)
    )

    return jsonify({
        "status": "200" if result else "500",
        "response": "Successfully saved" if result else "Error on save task"
    }), 200 if result else 500

@app.route('/task/get', methods=['GET'])
def task_get():
    """
    Get all tasks
    """
    email = uc_user.check_login(
        token=request.args["token"],
        tokens_list=USERS_TOKENS
    )

    uc_task_manager = TaskManager(
        db_controller=db_controller
    )

    result = uc_task_manager.get_all(
        user_id=uc_user.get_user_id(email)
    )

    print(result)

    return jsonify({
        "status": "200" if result else "500",
        "response": result if result else "Error on getting task"
    }), 200 if result else 500


if __name__ == '__main__':
    app.run(debug=True)

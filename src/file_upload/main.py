from flask import Flask
from flask_jwt_extended import JWTManager

from .blueprints.auth import auth_blueprint
from .blueprints.task import task_bp


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "sjckci348dfktocfmekxcjemtkmejf5k3o"

jwt = JWTManager(app)

app.route("/")
def home():
    return {
        "message": "Welcome to the Flask API"
    }
app.register_blueprint(auth_blueprint)
app.register_blueprint(task_bp)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
from flask_app import app
from flask_app.controllers import users,posts,comments


if __name__ == "__main__":
    app.run(debug=True, port=8000)

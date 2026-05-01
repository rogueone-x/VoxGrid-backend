from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from routes import issues, users, comments, discussions, votes, polls

app = Flask(__name__)
CORS(app)

app.register_blueprint(users.auth_bp, url_prefix="/auth")
app.register_blueprint(issues.issues_bp, url_prefix="/issues")
app.register_blueprint(comments.comments_bp, url_prefix="/comments")
app.register_blueprint(discussions.discussions_bp, url_prefix="/comments")


if __name__ == "__main__":
    app.run(debug=True)

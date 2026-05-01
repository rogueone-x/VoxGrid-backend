from flask import Blueprint, request, jsonify
from models.issue_model import create_issue, get_all_issues, get_issue_by_id

issues_bp = Blueprint("issues", __name__)


@issues_bp.route("/", methods=["POST"])
def add_issue():
    data = request.json

    title = data.get("title")
    summary = data.get("summary")
    category_id = data.get("category_id")

    # basic validation
    if not title or not summary or not category_id:
        return jsonify({"error": "Missing required fields"}), 400

    issue_id = create_issue(title, summary, category_id)

    return jsonify({"message": "Issue created successfully", "issue_id": issue_id}), 201


@issues_bp.route("/issues", methods=["POST"])
def fetch_issues():
    category = request.args.get("category")
    sort = request.args.get("sort")  # optional

    issues = get_all_issues(category, sort)

    return jsonify(issues)


@issues_bp.route("/<int:issue_id>", methods=["GET"])
def fetch_issue(issue_id):
    issue = get_issue_by_id(issue_id)

    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    return jsonify(issue)

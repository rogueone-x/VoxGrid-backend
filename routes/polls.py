from flask import Blueprint, request, jsonify
from models.poll_model import (
    get_poll_by_issue,
    create_poll,
    add_poll_options,
    vote_poll,
    get_poll_results,
)

polls_bp = Blueprint("polls", __name__)


@polls_bp.route("/", methods=["GET"])
def fetch_poll():
    issue_id = request.args.get("issue_id")

    if not issue_id:
        return jsonify({"error": "issue_id is required"}), 400

    poll = get_poll_by_issue(issue_id)

    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    return jsonify(poll)


@polls_bp.route("/", methods=["POST"])
def add_poll():
    data = request.json

    issue_id = data.get("issue_id")
    question = data.get("question")
    options = data.get("options")  # array

    if not issue_id or not question or not options:
        return jsonify({"error": "Missing required fields"}), 400

    if len(options) < 2:
        return jsonify({"error": "At least 2 options required"}), 400

    poll_id = create_poll(issue_id, question)
    add_poll_options(poll_id, options)

    return jsonify({"message": "Poll created", "poll_id": poll_id}), 201


@polls_bp.route("/<int:poll_id>/vote", methods=["POST"])
def vote(poll_id):
    data = request.json
    option_id = data.get("option_id")

    if not option_id:
        return jsonify({"error": "option_id required"}), 400

    vote_poll(poll_id, option_id)

    results = get_poll_results(poll_id)

    return jsonify({"message": "Vote recorded", "results": results})

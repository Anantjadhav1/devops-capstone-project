from datetime import date
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from service import db
from service.models import Account

accounts_bp = Blueprint("accounts", __name__)

REQUIRED = ("name", "email", "address")

def validate_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return "Request body must be a JSON object"
    if not partial:
        missing = [field for field in REQUIRED if not payload.get(field)]
        if missing:
            return "Missing required fields: " + ", ".join(missing)
    return None

@accounts_bp.post("/accounts")
def create_account():
    payload = request.get_json(silent=True)
    error = validate_payload(payload)
    if error:
        return jsonify({"error": error}), 400
    account = Account(
        name=payload["name"], email=payload["email"], address=payload["address"],
        phone_number=payload.get("phone_number"),
        date_joined=date.fromisoformat(payload["date_joined"]) if payload.get("date_joined") else date.today(),
    )
    db.session.add(account)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An account with this email already exists"}), 409
    return jsonify(account.to_dict()), 201

@accounts_bp.get("/accounts")
def list_accounts():
    return jsonify([account.to_dict() for account in Account.query.order_by(Account.id).all()]), 200

@accounts_bp.get("/accounts/<int:account_id>")
def read_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.to_dict()), 200

@accounts_bp.put("/accounts/<int:account_id>")
def update_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    payload = request.get_json(silent=True)
    error = validate_payload(payload, partial=True)
    if error:
        return jsonify({"error": error}), 400
    allowed = {"name", "email", "address", "phone_number", "date_joined"}
    for key, value in payload.items():
        if key in allowed:
            if key == "date_joined" and value:
                try:
                    value = date.fromisoformat(value)
                except (TypeError, ValueError):
                    return jsonify({"error": "date_joined must use YYYY-MM-DD"}), 400
            setattr(account, key, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An account with this email already exists"}), 409
    return jsonify(account.to_dict()), 200

@accounts_bp.delete("/accounts/<int:account_id>")
def delete_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    db.session.delete(account)
    db.session.commit()
    return "", 204

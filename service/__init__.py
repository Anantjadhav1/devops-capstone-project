import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///accounts.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # HTTPS is disabled for local/test usage; enable it behind HTTPS in production.
    Talisman(app, force_https=False, content_security_policy=None)

    from service.routes import accounts_bp
    app.register_blueprint(accounts_bp)

    @app.get("/")
    def index():
        return jsonify({"service": "Customer Accounts Microservice", "status": "ok"})

    with app.app_context():
        db.create_all()

    return app

app = create_app()

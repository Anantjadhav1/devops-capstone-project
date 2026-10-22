from datetime import date
from service.models import Account

def test_account_to_dict(app):
    with app.app_context():
        account = Account(
            id=7, name="Anita Rao", email="anita@example.com",
            address="Pune, India", phone_number="9876543210", date_joined=date(2025, 1, 2)
        )
        result = account.to_dict()
        assert result["id"] == 7
        assert result["name"] == "Anita Rao"
        assert result["date_joined"] == "2025-01-02"

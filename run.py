from shop import app, db
from shop.admin.models import User


def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

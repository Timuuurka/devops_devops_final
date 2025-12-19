from app import create_app, db
from app import models

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        models.seed_initial_data(db)
        print("DB init complete: tables created and seed ensured.")

if __name__ == "__main__":
    main()

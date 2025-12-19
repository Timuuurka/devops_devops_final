from datetime import datetime
from app import db

class Film(db.Model):
    __tablename__ = "films"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration_min = db.Column(db.Integer, nullable=False)
    age_rating = db.Column(db.String(10), nullable=False)  # e.g., "PG-13"
    description = db.Column(db.Text, nullable=True)

    screenings = db.relationship("Screening", backref="film", lazy=True)

class Hall(db.Model):
    __tablename__ = "halls"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    rows = db.Column(db.Integer, nullable=False)
    seats_per_row = db.Column(db.Integer, nullable=False)

    screenings = db.relationship("Screening", backref="hall", lazy=True)

class Screening(db.Model):
    __tablename__ = "screenings"
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey("halls.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    bookings = db.relationship("Booking", backref="screening", lazy=True, cascade="all, delete-orphan")

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    screening_id = db.Column(db.Integer, db.ForeignKey("screenings.id"), nullable=False)

    row_number = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)

    customer_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("screening_id", "row_number", "seat_number", name="uq_screening_seat"),
    )

def seed_initial_data(db):
    """
    Seeds initial demo data ONLY if DB is empty.
    """
    if Film.query.first():
        return

    # Films
    films = [
        Film(
            title="Interstellar",
            duration_min=169,
            age_rating="PG-13",
            description="A team travels through a wormhole in space in an attempt to ensure humanity's survival."
        ),
        Film(
            title="Spirited Away",
            duration_min=125,
            age_rating="PG",
            description="A young girl enters a mysterious world ruled by gods, witches, and spirits."
        ),
        Film(
            title="The Dark Knight",
            duration_min=152,
            age_rating="PG-13",
            description="Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos."
        )
    ]
    db.session.add_all(films)

    # Halls
    halls = [
        Hall(name="Hall A", rows=6, seats_per_row=10),   # 60 seats
        Hall(name="Hall B", rows=5, seats_per_row=8),    # 40 seats
        Hall(name="Hall C", rows=4, seats_per_row=12),   # 48 seats
    ]
    db.session.add_all(halls)
    db.session.commit()

    # Screenings (today/tomorrow demo schedule)
    now = datetime.utcnow()
    screenings = [
        Screening(film_id=films[0].id, hall_id=halls[0].id, start_time=now.replace(hour=14, minute=0, second=0, microsecond=0)),
        Screening(film_id=films[0].id, hall_id=halls[1].id, start_time=now.replace(hour=19, minute=30, second=0, microsecond=0)),
        Screening(film_id=films[1].id, hall_id=halls[2].id, start_time=now.replace(hour=16, minute=15, second=0, microsecond=0)),
        Screening(film_id=films[2].id, hall_id=halls[0].id, start_time=now.replace(hour=21, minute=0, second=0, microsecond=0)),
    ]
    db.session.add_all(screenings)
    db.session.commit()

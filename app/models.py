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
    Safe to run multiple times (idempotent enough for demo).
    """
    # If we already have films and halls, assume seeded.
    if Film.query.first() and Hall.query.first() and Screening.query.first():
        return

    # Films
    films_data = [
        dict(
            title="Interstellar",
            duration_min=169,
            age_rating="PG-13",
            description="A team travels through a wormhole in space in an attempt to ensure humanity's survival."
        ),
        dict(
            title="Spirited Away",
            duration_min=125,
            age_rating="PG",
            description="A young girl enters a mysterious world ruled by gods, witches, and spirits."
        ),
        dict(
            title="The Dark Knight",
            duration_min=152,
            age_rating="PG-13",
            description="Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos."
        )
    ]

    for f in films_data:
        if not Film.query.filter_by(title=f["title"]).first():
            db.session.add(Film(**f))

    # Halls
    halls_data = [
        dict(name="Hall A", rows=6, seats_per_row=10),
        dict(name="Hall B", rows=5, seats_per_row=8),
        dict(name="Hall C", rows=4, seats_per_row=12),
    ]

    for h in halls_data:
        if not Hall.query.filter_by(name=h["name"]).first():
            db.session.add(Hall(**h))

    db.session.commit()

    # Screenings
    from datetime import datetime
    now = datetime.utcnow()

    # Refresh objects
    films = Film.query.all()
    halls = Hall.query.all()

    # helper lookups
    film_by_title = {f.title: f for f in films}
    hall_by_name = {h.name: h for h in halls}

    screenings_data = [
        ("Interstellar", "Hall A", now.replace(hour=14, minute=0, second=0, microsecond=0)),
        ("Interstellar", "Hall B", now.replace(hour=19, minute=30, second=0, microsecond=0)),
        ("Spirited Away", "Hall C", now.replace(hour=16, minute=15, second=0, microsecond=0)),
        ("The Dark Knight", "Hall A", now.replace(hour=21, minute=0, second=0, microsecond=0)),
    ]

    for film_title, hall_name, start_time in screenings_data:
        film = film_by_title.get(film_title)
        hall = hall_by_name.get(hall_name)
        if not film or not hall:
            continue

        exists = Screening.query.filter_by(film_id=film.id, hall_id=hall.id, start_time=start_time).first()
        if not exists:
            db.session.add(Screening(film_id=film.id, hall_id=hall.id, start_time=start_time))

    db.session.commit()

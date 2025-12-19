from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app import db
from app.models import Film, Hall, Screening, Booking

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    screenings = Screening.query.order_by(Screening.start_time.asc()).all()
    return render_template("index.html", screenings=screenings)

@main_bp.route("/screenings/<int:screening_id>", methods=["GET", "POST"])
def screening_detail(screening_id):
    screening = Screening.query.get_or_404(screening_id)
    hall = screening.hall

    # Build occupied seats map for quick checks in template
    bookings = Booking.query.filter_by(screening_id=screening.id).all()
    occupied = {(b.row_number, b.seat_number): b for b in bookings}

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        row_number = request.form.get("row_number", "").strip()
        seat_number = request.form.get("seat_number", "").strip()

        # Basic validation
        if not customer_name:
            flash("Customer name is required.", "danger")
            return redirect(url_for("main.screening_detail", screening_id=screening.id))

        try:
            row_number = int(row_number)
            seat_number = int(seat_number)
        except ValueError:
            flash("Row and seat must be numbers.", "danger")
            return redirect(url_for("main.screening_detail", screening_id=screening.id))

        if row_number < 1 or row_number > hall.rows or seat_number < 1 or seat_number > hall.seats_per_row:
            flash("Invalid seat coordinates for this hall.", "danger")
            return redirect(url_for("main.screening_detail", screening_id=screening.id))

        # Try booking (DB unique constraint will protect from double-booking)
        new_booking = Booking(
            screening_id=screening.id,
            row_number=row_number,
            seat_number=seat_number,
            customer_name=customer_name
        )

        db.session.add(new_booking)
        try:
            db.session.commit()
            flash(f"Booked successfully: Row {row_number}, Seat {seat_number} for {customer_name}.", "success")
        except IntegrityError:
            db.session.rollback()
            flash(f"Seat already taken: Row {row_number}, Seat {seat_number}. Please select another seat.", "warning")

        return redirect(url_for("main.screening_detail", screening_id=screening.id))

    return render_template(
        "screening.html",
        screening=screening,
        hall=hall,
        occupied=occupied
    )

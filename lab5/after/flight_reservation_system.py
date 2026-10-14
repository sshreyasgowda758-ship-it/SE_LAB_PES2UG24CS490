
"""Flight reservation system for static analysis lab."""

import hashlib
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

RESERVATION_STATE = {"total_revenue": 0.0}


def book_flight_seat(flight_no, passenger, luggage_weight=15,
                     baggage_tags=None):
    """Book a seat and record its baggage details."""
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    FLIGHTS[flight_no]["seats"] -= 1
    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True

    RESERVATION_STATE["total_revenue"] += FLIGHTS[flight_no]["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel a booking when the flight number exists."""
    if flight_no in FLIGHTS:
        FLIGHTS[flight_no]["seats"] += 1
        FLIGHTS[flight_no]["is_full"] = False


def check_seat_availability(flight_no):
    """Return whether a flight has seats available."""
    if FLIGHTS.get(flight_no) is None:
        return False
    return not FLIGHTS[flight_no]["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate=0.15):
    """Calculate the baggage fee using a validated surcharge rate."""
    if flight_no not in FLIGHTS:
        raise ValueError(f"Unknown flight number: {flight_no}")
    if not 0 <= surcharge_rate <= 1:
        raise ValueError("Surcharge rate must be between 0 and 1.")

    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Generate a SHA-256 hash for the passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit boarding PIN."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Export the flight manifest to a text file."""
    with open(filename, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(str(FLIGHTS))
    print(f"Boarding manifest saved to {filename}")


def get_flight_summary(flight_data):
    """Return the number of flights that are not full."""
    available_count = 0
    for details in flight_data.values():
        if not details["is_full"]:
            available_count += 1
    return available_count


def main():
    """Run sample flight reservation operations."""

    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))


if __name__ == "__main__":
    main()

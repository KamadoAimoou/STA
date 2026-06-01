import re


def find_first(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Not found"


def parse_ticket(text):
    airline = "Air Astana" if "air astana" in text.lower() else "Not found"

    ticket_type = "e-ticket" if "e-ticket" in text.lower() else "Not found"

    route = find_first(
        r"Route\s+([A-ZА-ЯЁ\s\-]+)",
        text
    )

    time = find_first(
        r"\b([0-2]?\d:[0-5]\d)\b",
        text
    )

    booking_ref = find_first(
        r"\b([A-Z0-9]{6})\b",
        text
    )

    return {
        "airline": airline,
        "ticket_type": ticket_type,
        "route": route,
        "time": time,
        "booking_ref": booking_ref,
    }


def format_ticket_summary(data):
    return (
        "✈️ Ticket Summary\n\n"
        f"Airline: {data['airline']}\n"
        f"Ticket type: {data['ticket_type']}\n"
        f"Route: {data['route']}\n"
        f"Time: {data['time']}\n"
        f"Booking ref: {data['booking_ref']}\n\n"
        "✅ Advice:\n"
        "Arrive at the airport at least 2 hours before departure.\n"
        "Check terminal and gate on the airport screen.\n"
        "Aimurat the world love you "
    )
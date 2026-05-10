import re


def find_candidates(patterns, text):
    candidates = []

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)

        for match in matches:
            value = match.group(1) if match.lastindex else match.group(0)

            candidates.append({
                "value": value.strip(),
                "confidence": 0.70
            })

    return candidates


def choose_best(candidates):
    if not candidates:
        return {
            "value": "Not found",
            "confidence": 0.0
        }

    return max(candidates, key=lambda item: item["confidence"])


def extract_entities(text):
    patterns = {
        "flight_number": [
            r"\b([A-Z]{2}\s?\d{3,4})\b",
            r"Flight[:\s]*([A-Z]{2}\s?\d{3,4})",
            r"Flight Number[:\s]*([A-Z]{2}\s?\d{3,4})",
        ],
        "time": [
            r"\b([0-2]?\d:[0-5]\d)\b",
            r"Departure[:\s]*([0-2]?\d:[0-5]\d)",
        ],
        "seat": [
            r"Seat[:\s]*([0-9]{1,2}[A-Z])",
            r"\b([0-9]{1,2}[A-Z])\b",
        ],
        "gate": [
            r"Gate[:\s]*([A-Z]?\d{1,3})",
            r"Boarding Gate[:\s]*([A-Z]?\d{1,3})",
        ],
        "booking_ref": [
            r"Booking[:\s]*([A-Z0-9]{5,8})",
            r"Booking Ref[:\s]*([A-Z0-9]{5,8})",
            r"Reservation[:\s]*([A-Z0-9]{5,8})",
        ],
    }

    result = {}

    for entity_name, entity_patterns in patterns.items():
        candidates = find_candidates(entity_patterns, text)
        best = choose_best(candidates)

        result[entity_name] = best

    return result


def format_entities(entities):
    return (
        "🤖 Smart Ticket Extraction\n\n"
        f"Flight number: {entities['flight_number']['value']} "
        f"({entities['flight_number']['confidence']:.0%})\n"
        f"Time: {entities['time']['value']} "
        f"({entities['time']['confidence']:.0%})\n"
        f"Seat: {entities['seat']['value']} "
        f"({entities['seat']['confidence']:.0%})\n"
        f"Gate: {entities['gate']['value']} "
        f"({entities['gate']['confidence']:.0%})\n"
        f"Booking ref: {entities['booking_ref']['value']} "
        f"({entities['booking_ref']['confidence']:.0%})\n\n"
        "✅ Advice:\n"
        "Check gate and boarding time on the airport screen."
    )
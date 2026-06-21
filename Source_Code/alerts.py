from datetime import datetime


def simulate_alert(latitude: float, longitude: float, contact: str, note: str) -> str:
    message = (
        f"[ALERT] {datetime.utcnow().isoformat()} | Contact: {contact} | "
        f"Location: ({latitude:.6f}, {longitude:.6f}) | Note: {note}"
    )
    print(message)
    return message

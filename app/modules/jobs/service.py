from app.modules.notifications.service import send_notification


def list_jobs() -> list:
    return []


def create_job(name: str) -> dict:
    job = {"id": 1, "name": name, "status": "queued"}
    send_notification(f"Job created: {name}")
    return job
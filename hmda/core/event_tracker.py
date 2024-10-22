import json
from datetime import datetime
from typing import List, Dict
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class EventTracker:
    def __init__(self, file_path: str = "events.json"):
        self.file_path = file_path
        self.events: List[Dict[str, str]] = []
        self.load_events()

    def load_events(self):
        try:
            with open(self.file_path, "r") as f:
                self.events = json.load(f)
        except FileNotFoundError:
            logger.info(f"Events file not found. Creating a new one at {self.file_path}")
        except json.JSONDecodeError:
            logger.warning(f"Error decoding events file. Starting with empty events.")

    def save_events(self):
        with open(self.file_path, "w") as f:
            json.dump(self.events, f, indent=2)

    def add_event(self, event_type: str, status: str, description: str):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "status": status,
            "description": description
        }
        self.events.append(event)
        self.save_events()
        logger.info(f"Event added: {event}")

    def get_events(self) -> List[Dict[str, str]]:
        return self.events
    
    def get_status(self, event_type: str) -> str:
        for event in self.events:
            if event["type"] == event_type:
                return event["status"]
        return "not_started"

event_tracker = EventTracker()

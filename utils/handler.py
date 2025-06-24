# utils/handler.py

from utils.time_utils import normalize_date, normalize_time
from utils.launch_app import AppLaunchHandler
from utils.ChangeWallpaper import suggest_wallpapers_until_accepted
import json

def handle_set_reminder(entities, user_id):
    # Your custom logic
    print(entities)
    task = entities.get("task")
    date = entities.get("date")
    time = entities.get("time")

    if not all([task, date, time]):
        return "I need the task, date, and time to set the reminder."

    # Save to file (JSON)
    reminder = {"task": task, "date": date, "time": time}
    try:
        with open("reminders.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(reminder)

    with open("reminders.json", "w") as f:
        json.dump(data, f, indent=4)

    return f"Reminder saved for '{task}' on {date} at {time}."

def handle_get_reminder(entities, user_id):
    # Your retrieval logic
    return "Here are your reminders."
def handle_get_reminder(entities):
    date = normalize_date(entities.get("date"))
    try:
        with open("reminders.json", "r") as f:
            data = json.load(f)
    except:
        return "No reminders saved yet."

    reminders = [r for r in data if r["date"] == date] if date else data
    if not reminders:
        return "No reminders found."

    return "\n".join([f"🔔 {r['time']}: {r['task']}" for r in reminders])

def handle_open_app(entities, user_id):
    # Your app launch logic

    launcher = AppLaunchHandler()


    # Extract the app_name safely
    app_name = next(iter(entities.values()), None)  # Gets 'terminal' or None if empty
    intent_payload = {"app_name": app_name}
    print(intent_payload)
    response = launcher.handle_intent('open_app', intent_payload)
    print(response)
    return f"opping {app_name}"

def WallpaperHandler():
    return suggest_wallpapers_until_accepted()

def Notepad():
    return AppLaunchHandler.notepad()
def Calculator():
    return AppLaunchHandler.calculator()
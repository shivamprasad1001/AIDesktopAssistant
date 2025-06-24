import os
import platform
import subprocess
import json
from difflib import get_close_matches

APP_REGISTRY_PATH = "app_registry.json"


def load_registry_from_file(path=APP_REGISTRY_PATH):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_APP_REGISTRY


def save_registry_to_file(registry, path=APP_REGISTRY_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)


DEFAULT_APP_REGISTRY = {
    "chrome": {
        "aliases": ["google chrome", "chrome browser", "browser", "open browser"],
        "executables": {
            "windows": "chrome.exe",
            "mac": "Google Chrome",
            "linux": "google-chrome"
        }
    },
    "vscode": {
        "aliases": ["vs code", "visual studio code", "code editor"],
        "executables": {
            "windows": "code",
            "mac": "Visual Studio Code",
            "linux": "code"
        }
    },
    "notepad": {
        "aliases": ["open notepad", "text editor", "write notes"],
        "executables": {
            "windows": "notepad.exe",
            "mac": "TextEdit",
            "linux": "gedit"
        }
    },
    "calculator": {
        "aliases": ["calc", "calculator", "do math"],
        "executables": {
            "windows": "calc.exe",
            "mac": "Calculator",
            "linux": "gnome-calculator"
        }
    },
    "camera": {
        "aliases": ["open camera", "take photo", "photo app"],
        "executables": {
            "windows": "start microsoft.windows.camera:",
            "mac": "Photo Booth",
            "linux": "cheese"
        }
    },
    "settings": {
        "aliases": ["system settings", "open settings", "control panel"],
        "executables": {
            "windows": "start ms-settings:",
            "mac": "System Settings",
            "linux": "gnome-control-center"
        }
    },
    "spotify": {
        "aliases": ["music", "spotify", "play songs", "music player"],
        "executables": {
            "windows": "spotify.exe",
            "mac": "Spotify",
            "linux": "spotify"
        }
    },
    "file_explorer": {
        "aliases": ["open files", "file explorer", "explorer"],
        "executables": {
            "windows": "explorer.exe",
            "mac": "Finder",
            "linux": "nautilus"
        }
    },
    "terminal": {
        "aliases": ["command prompt", "terminal", "cmd", "shell"],
        "executables": {
            "windows": "cmd.exe",
            "mac": "Terminal",
            "linux": "gnome-terminal"
        }
    },
    "paint": {
        "aliases": ["draw", "paint", "mspaint"],
        "executables": {
            "windows": "mspaint.exe",
            "mac": "Paintbrush",
            "linux": "pinta"
        }
    }
}


class AppLaunchHandler:
    def __init__(self):
        self.app_registry = load_registry_from_file()
        self.unlisted_log_file = "unlisted_apps.log"

    def handle_intent(self, intent, entities):
        if intent == "open_app":
            app_entity = entities.get("app_name")
            if app_entity:
                return self.launch_application(app_entity)
            else:
                return "🤖 Which application would you like me to open?"
        return None

    def resolve_app_name(self, user_app_name):
        user_app_lower = user_app_name.lower()
        if user_app_lower in self.app_registry:
            return user_app_lower

        for canonical_name, app_info in self.app_registry.items():
            if user_app_lower in app_info["aliases"]:
                return canonical_name

        suggestions = get_close_matches(user_app_lower,
            list(self.app_registry.keys()) +
            [alias for app in self.app_registry.values() for alias in app["aliases"]],
            n=1, cutoff=0.7
        )
        return suggestions[0] if suggestions else None

    def launch_application(self, app_name):
        canonical_name = self.resolve_app_name(app_name)

        if canonical_name in self.app_registry:
            return self.execute_launch(canonical_name)

        try:
            subprocess.Popen([app_name])
            self.log_unlisted_app(app_name)
            return f"⚠️ '{app_name}' was not listed, but I tried running it directly."
        except Exception:
            self.log_unlisted_app(app_name)
            suggestion = self.suggest_app_name(app_name)
            msg = f"❌ I couldn't find or launch '{app_name}'."
            if suggestion:
                msg += f" Did you mean '{suggestion}'?"
            print(msg + "\n💡 You can register this app if you use it often.")
            self.ask_user_to_register(app_name)

            if app_name.lower() in self.app_registry:
                return self.execute_launch(app_name.lower())
            else:
                return msg + "\n📝 Registration skipped or failed."

    def execute_launch(self, canonical_name):
        system = platform.system().lower()
        app_info = self.app_registry[canonical_name]
        executable = app_info["executables"].get(system)

        if not executable:
            return f"❌ I know about '{canonical_name}', but it's not available on {system}."

        try:
            if system == "windows" and executable.startswith("start "):
                subprocess.Popen(["cmd", "/c", executable])
            elif system == "windows":
                subprocess.Popen([executable], shell=True)
            elif system == "mac":
                subprocess.Popen(["open", "-a", executable])
            elif system == "linux":
                subprocess.Popen([executable])
            return f"✅ Launching {canonical_name}..."
        except Exception as e:
            return f"❌ Failed to launch '{canonical_name}': {e}"

    def log_unlisted_app(self, app_name):
        with open(self.unlisted_log_file, "a", encoding="utf-8") as f:
            f.write(f"{app_name}\n")

    def suggest_app_name(self, unknown_name):
        all_names = list(self.app_registry.keys()) + [alias for app in self.app_registry.values() for alias in app["aliases"]]
        matches = get_close_matches(unknown_name.lower(), all_names, n=1, cutoff=0.65)
        return matches[0] if matches else None

    def ask_user_to_register(self, new_app_name):
        should_register = input(f"❓ Would you like to register '{new_app_name}' as a new app? (yes/no): ").strip().lower()
        if should_register not in ['yes', 'y']:
            return

        system = platform.system().lower()
        executable = input(f"🔧 Enter the executable/command for '{new_app_name}' on {system}: ").strip()
        aliases = input(f"📝 Enter aliases for '{new_app_name}' (comma-separated): ").strip().split(",")

        self.app_registry[new_app_name.lower()] = {
            "aliases": [alias.strip().lower() for alias in aliases],
            "executables": {
                system: executable
            }
        }

        save_registry_to_file(self.app_registry)
        print(f"✅ Registered new app '{new_app_name}' for {system}!")



# launcher = AppLaunchHandler()

# intent = "open_app"
# entities = {
#     "app_name": "camera"  # from your NER model or user input
# }

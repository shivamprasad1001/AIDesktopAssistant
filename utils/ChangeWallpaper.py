import os
import platform
import subprocess
import ctypes
import random
import shutil

# Example config (load this from config.json)
config = {
    "wallpaper": {
        "dir_location": "D:/wall"
    }
}

def apply_wallpaper(image_path, system):
    if not os.path.exists(image_path):
        return f"❌ File not found: {image_path}"

    try:
        if system == "windows":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        elif system == "linux":
            subprocess.run([
                "gsettings", "set",
                "org.gnome.desktop.background", "picture-uri",
                f"file://{image_path}"
            ], check=True)
        elif system == "darwin":
            subprocess.run([
                "osascript", "-e",
                f'tell application "Finder" to set desktop picture to POSIX file \"{image_path}\"'
            ])
        else:
            return "❌ Unsupported OS."
    except Exception as e:
        return f"❌ Error setting wallpaper: {e}"

    return f"✅ Wallpaper set to: {os.path.basename(image_path)}"

def get_previous_wallpaper_windows():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Control Panel\Desktop", 0, winreg.KEY_READ) as key:
            current = winreg.QueryValueEx(key, "WallPaper")[0]
            return current if os.path.exists(current) else None
    except:
        return None

def suggest_wallpapers_until_accepted():
    system = platform.system().lower()
    wallpaper_dir = config.get("wallpaper", {}).get("dir_location")

    if not wallpaper_dir or not os.path.exists(wallpaper_dir):
        return "❌ Wallpaper directory is not configured correctly."

    images = [f for f in os.listdir(wallpaper_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        return "❌ No wallpaper images found."

    previous_wallpaper = None
    if system == "windows":
        previous_wallpaper = get_previous_wallpaper_windows()

    tried = set()

    while True:
        if len(tried) == len(images):
            return "⚠️ No more wallpapers to suggest."

        selected = random.choice(images)
        if selected in tried:
            continue
        tried.add(selected)

        image_path = os.path.join(wallpaper_dir, selected)
        result = apply_wallpaper(image_path, system)
        print(f"{result}")
        comform_msg = f"🖼️ Look, I’ve changed your wallpaper to '{selected}'. Take a look — is it okay? (yes/no/stop)"
        print(comform_msg)
        user_input = input("👉 ").strip().lower()
        if user_input in ["yes", "y"]:
            return f"✅ Great! Keeping wallpaper: {selected}"
        elif user_input in ["stop", "cancel"]:
            if previous_wallpaper:
                print("🔁 Reverting to previous wallpaper...")
                apply_wallpaper(previous_wallpaper, system)
                return "🔁 Reverted. No wallpaper was changed."
            else:
                return "❌ Canceled. No previous wallpaper to revert to."
        else:
            print("🔄 Okay, let me try another one...\n")


        

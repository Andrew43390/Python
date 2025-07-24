import os
import shutil
import datetime
import json

BASE_PATH = r"C:\Users\james\Desktop\Network"
CONFIG_FILE = "unwanted_files.txt"
UNDO_RECORD_FILE = "last_cleanup_undo.json"

def load_unwanted_files():
    print(f"🔍 Looking for config file '{CONFIG_FILE}'...")
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file '{CONFIG_FILE}' NOT found. Cannot continue.")
        return []
    with open(CONFIG_FILE, "r") as f:
        files = [line.strip() for line in f if line.strip()]
    print(f"✅ Config loaded. {len(files)} unwanted file(s) listed.")
    return files

def find_files_by_name(root_dir, target_files):
    found = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in target_files:
                full_path = os.path.join(dirpath, filename)
                found.append(full_path)
    return found

def move_files(files_to_move, archive_root):
    moved = []
    for original_path in files_to_move:
        relative_path = os.path.relpath(original_path, BASE_PATH)
        archive_path = os.path.join(archive_root, relative_path)
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        print(f"\n📦 Move '{relative_path}'?")
        confirm = input("→ Move this file? (y/n): ").strip().lower()
        if confirm == 'y':
            shutil.move(original_path, archive_path)
            moved.append((archive_path, original_path))
            print(f"✅ Moved: {original_path} -> {archive_path}")
        else:
            print("⏩ Skipped.")
    return moved

def save_undo_data(moved_files):
    if moved_files:
        with open(UNDO_RECORD_FILE, "w") as f:
            json.dump(moved_files, f)
        print(f"\n💾 Undo info saved to '{UNDO_RECORD_FILE}'.")

def undo_last_cleanup():
    if not os.path.exists(UNDO_RECORD_FILE):
        print("⚠️ No undo record found.")
        return
    with open(UNDO_RECORD_FILE, "r") as f:
        moved_files = json.load(f)
    print("\n⏪ Undoing previous cleanup...")
    for src, dest in moved_files:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(src, dest)
        print(f"✅ Restored: {src} -> {dest}")
    os.remove(UNDO_RECORD_FILE)
    print("🧹 Undo complete. Record file deleted.")

def main():
    print("🚀 Cleanup.py started\n")

    unwanted_files = load_unwanted_files()
    if not unwanted_files:
        return

    matched_files = find_files_by_name(BASE_PATH, unwanted_files)
    if not matched_files:
        print("📂 No unwanted files found in the directory tree.")
        return

    timestamp = datetime.datetime.now().strftime("archive_unwanted_%Y%m%d_%H%M%S")
    archive_dir = os.path.join(BASE_PATH, timestamp)
    print(f"\n📁 Archive directory: {archive_dir}")

    moved_files = move_files(matched_files, archive_dir)

    if moved_files:
        print(f"\n📦 Moved {len(moved_files)} file(s).")
        save_undo_data(moved_files)
    else:
        print("\n📦 No files moved.")

    choice = input("\nUndo move? (y/n): ").strip().lower()
    if choice == 'y':
        undo_last_cleanup()
    else:
        print("✅ Done. No undo requested.")

if __name__ == "__main__":
    main()

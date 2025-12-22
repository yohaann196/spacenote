import json
import os
import tempfile

NOTES_FILE = "notes.json"


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: notes file corrupted. Starting fresh.\n")
        return []


notes = load_notes()


def save_notes():
    fd, temp_path = tempfile.mkstemp()
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
    os.replace(temp_path, NOTES_FILE)


def prompt_multiline(prompt):
    print(prompt)
    print("(finish with an empty line)")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def list_notes():
    if not notes:
        print("No notes yet.\n")
        return False
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']}")
    print()
    return True


def get_index(prompt):
    if not list_notes():
        return None
    choice = input(prompt).strip()
    if not choice.isdigit():
        print("Invalid number.\n")
        return None
    idx = int(choice) - 1
    if idx < 0 or idx >= len(notes):
        print("Out of range.\n")
        return None
    return idx


def add_note():
    while True:
        title = input("Title: ").strip()
        if title:
            break
        print("Title cannot be empty.")
    content = prompt_multiline("Content:")
    notes.append({"title": title, "content": content})
    save_notes()
    print("Note added.\n")


def view_note():
    idx = get_index("View note #: ")
    if idx is None:
        return
    note = notes[idx]
    print("\n" + "=" * 40)
    print(note["title"])
    print("-" * 40)
    print(note["content"] or "(empty)")
    print("=" * 40 + "\n")


def edit_note():
    idx = get_index("Edit note #: ")
    if idx is None:
        return
    note = notes[idx]

    new_title = input(f"New title (enter to keep '{note['title']}'): ").strip()
    if new_title:
        note["title"] = new_title

    print("Edit content")
    new_content = prompt_multiline("New content (leave empty to keep current):")
    if new_content:
        note["content"] = new_content

    save_notes()
    print("Note updated.\n")


def delete_note():
    idx = get_index("Delete note #: ")
    if idx is None:
        return
    removed = notes.pop(idx)
    save_notes()
    print(f"Deleted '{removed['title']}'.\n")


def menu():
    print("=== Spacenote ===")
    print("1. Add note")
    print("2. List notes")
    print("3. View note")
    print("4. Edit note")
    print("5. Delete note")
    print("6. Exit")
    return input("> ").strip()


def main():
    while True:
        choice = menu()
        if choice == "1":
            add_note()
        elif choice == "2":
            list_notes()
        elif choice == "3":
            view_note()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()

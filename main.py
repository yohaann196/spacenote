import json
import os

NOTES_FILE = "notes.json"

# Load notes from file if it exists
if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
else:
    notes = []

def save_notes():
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def add_note():
    title = input("Enter note title: ").strip()
    content = input("Enter note content: ").strip()
    notes.append({"title": title, "content": content})
    save_notes()
    print(f"Note '{title}' added.\n")

def view_notes():
    if not notes:
        print("No notes yet.\n")
        return
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']}")
    print("")

def view_note_detail():
    view_notes()
    if not notes:
        return
    idx = input("Enter note number to view: ").strip()
    if not idx.isdigit() or int(idx) < 1 or int(idx) > len(notes):
        print("Invalid note number.\n")
        return
    note = notes[int(idx)-1]
    print(f"\nTitle: {note['title']}\nContent: {note['content']}\n")

def edit_note():
    view_notes()
    if not notes:
        return
    idx = input("Enter note number to edit: ").strip()
    if not idx.isdigit() or int(idx) < 1 or int(idx) > len(notes):
        print("Invalid note number.\n")
        return
    note = notes[int(idx)-1]
    new_title = input(f"Enter new title (leave blank to keep '{note['title']}'): ").strip()
    new_content = input(f"Enter new content (leave blank to keep current content): ").strip()
    if new_title:
        note['title'] = new_title
    if new_content:
        note['content'] = new_content
    save_notes()
    print("Note updated.\n")

def delete_note():
    view_notes()
    if not notes:
        return
    idx = input("Enter note number to delete: ").strip()
    if not idx.isdigit() or int(idx) < 1 or int(idx) > len(notes):
        print("Invalid note number.\n")
        return
    note = notes.pop(int(idx)-1)
    save_notes()
    print(f"Deleted note '{note['title']}'.\n")

def menu():
    print("=== Spacenote ===")
    print("1. Add Note")
    print("2. View Notes")
    print("3. View Note Detail")
    print("4. Edit Note")
    print("5. Delete Note")
    print("6. Exit")
    choice = input("Choose an option: ").strip()
    return choice

def main():
    while True:
        choice = menu()
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            view_note_detail()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()

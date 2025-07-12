import os

# Create documents directory if it doesn't exist
if not os.path.exists("CLI Mode/documents/"):
    os.makedirs("CLI Mode/documents/")

def save_file(content, filepath):
    """Save the content to a file."""
    with open(filepath, 'w') as file:
        file.write(content)
    print(f"File saved as {filepath}\n")

def read_file(filepath):
    """Read the content of the file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    else:
        print("File does not exist.")
        return None

def notepad():
    """Main notepad function."""
    while True:
        print("Notepad")
        print("1. Create new file")
        print("2. Read and edit an existing file")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            # New file creation
            filename = input("Enter filename (or press Enter to auto-save in 'CLI Mode/documents/'): ")
            if not filename:
                filename = "CLI Mode/documents/untitled.txt"
            else:
                filename = "CLI Mode/documents/" + filename

            print("Enter text (type 'SAVE' on a new line to save the file):")
            content = []
            while True:
                line = input()
                if line.strip().upper() == 'SAVE':
                    break
                content.append(line)

            save_file("\n".join(content), filename)

        elif choice == '2':
            # Read and edit an existing file
            filepath = input("Enter the full path of the file to open: ")
            content = read_file(filepath)
            if content:
                print("Current file content:")
                print(content)
                print("\nEditing file. Type 'SAVE' on a new line to save the file.")
                new_content = []
                for line in content.splitlines():
                    new_content.append(line)
                while True:
                    new_line = input()
                    if new_line.strip().upper() == 'SAVE':
                        break
                    new_content.append(new_line)

                save_file("\n".join(new_content), filepath)

        elif choice == '3':
            # Exit
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the notepad app
notepad()

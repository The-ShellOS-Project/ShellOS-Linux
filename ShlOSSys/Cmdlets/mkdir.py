import os

# Function to create a new directory
def make_directory():
    new_dir = input("Enter the name of the directory you want to create: ")
    
    # Check if the directory already exists
    if not os.path.exists(new_dir):
        try:
            os.mkdir(new_dir)  # Attempt to create the directory
            print(f"Directory '{new_dir}' created successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Directory '{new_dir}' already exists.")

# Function to remove a directory
def remove_directory():
    dir_to_remove = input("Enter the name of the directory you want to remove: ")
    if os.path.exists(dir_to_remove) and os.path.isdir(dir_to_remove):
        try:
            os.rmdir(dir_to_remove)
            print(f"Directory '{dir_to_remove}' removed successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Directory '{dir_to_remove}' does not exist or is not a directory.")

# Main loop for creating and removing directories
while True:
    action = input("\nDo you want to (1) create a directory, (2) remove a directory, or (3) exit? Enter 1/2/3: ").strip()
    
    if action == '1':
        make_directory()
    elif action == '2':
        remove_directory()
    elif action == '3':
        print("Exiting the program.")
        break
    else:
        print("Invalid input, please enter 1, 2, or 3.")

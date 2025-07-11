import os
import sys
import zipfile
import shutil
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAMS_DIR = BASE_DIR
DEFAULT_REPO = "https://github.com/The-ShellOS-Project/ShellOS-Packages/raw/main/"
INDEX_URL = f"{DEFAULT_REPO}index.json"


def load_index():
    try:
        response = requests.get(INDEX_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[WARN] Could not load index.json (status {response.status_code})")
            return {}
    except Exception as e:
        print(f"[WARN] Failed to load index.json: {e}")
        return {}


def get_package_info(name, index):
    key = name.lower()
    if key in index:
        entry = index[key]
        return entry['file'], entry.get('description', 'No description')
    # Fallbacks
    for ext in ['.zip', '.py']:
        fallback_file = f"{key}{ext}"
        fallback_url = f"{DEFAULT_REPO}{fallback_file}"
        if requests.head(fallback_url).status_code == 200:
            return fallback_file, "No description (fallback)"
    return None, None


def install_package(arg):
    if not os.path.exists(PROGRAMS_DIR):
        os.makedirs(PROGRAMS_DIR)

    is_url = arg.startswith("http://") or arg.startswith("https://")

    if is_url:
        filename = os.path.basename(arg)
        name = filename.split(".")[0]
        url = arg
    else:
        index = load_index()
        filename, _ = get_package_info(arg, index)
        if not filename:
            print(f"[ERROR] Package '{arg}' not found.")
            return
        name = filename.split(".")[0]
        url = f"{DEFAULT_REPO}{filename}"

    dest_path = os.path.join(PROGRAMS_DIR, filename)
    extract_path = os.path.join(PROGRAMS_DIR, name)

    try:
        print(f"[INFO] Downloading {url}...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[ERROR] Failed to download '{filename}'. Status code: {response.status_code}")
            return

        with open(dest_path, 'wb') as f:
            f.write(response.content)

        if filename.endswith(".zip"):
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)
            print("[INFO] Extracting package...")
            with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            os.remove(dest_path)
            print(f"[SUCCESS] Installed '{name}' from zip.")
        else:
            print(f"[SUCCESS] Installed '{filename}' as standalone .py script.")

    except Exception as e:
        print(f"[ERROR] Install failed: {e}")


def uninstall_package(input_name):
    name = input_name.lower()
    found = False
    for folder in os.listdir(PROGRAMS_DIR):
        if folder.lower() == name or folder.lower() == f"{name}.py":
            path = os.path.join(PROGRAMS_DIR, folder)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"[SUCCESS] Uninstalled '{folder}'")
            found = True
            break
    if not found:
        print(f"[ERROR] Package '{input_name}' not found.")


def list_packages():
    try:
        print("[INFO] Fetching package list...")
        index_url = "https://github.com/The-ShellOS-Project/ShellOS-Packages/raw/main/index.json"
        response = requests.get(index_url)

        if response.status_code != 200:
            print(f"[ERROR] Failed to load index.json: {response.status_code} - {response.text}")
            return

        index_data = response.json()
        if not index_data:
            print("[INFO] No packages found in index.json.")
            return

        print("[INFO] Packages:")
        for package, details in index_data.items():
            print(f"- {package}: {details['description']} (File: {details['file']})")
    except Exception as e:
        print(f"[ERROR] Failed to fetch or parse index.json: {e}")


def print_help():
    print("""SPM Help:
  SPM Help                  Show this help message
  SPM Install <name/url>   Install package from name or URL
  SPM Uninstall <name>     Uninstall a package (folder or script)
  SPM List                 List available packages from repo
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "help":
        print_help()
    elif command == "install" and len(sys.argv) == 3:
        install_package(sys.argv[2])
    elif command == "uninstall" and len(sys.argv) == 3:
        uninstall_package(sys.argv[2])
    elif command == "list":
        list_packages()
    else:
        print("[ERROR] Unknown or invalid command.")
        print_help()


if __name__ == "__main__":
    main()

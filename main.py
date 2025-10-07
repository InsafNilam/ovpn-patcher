import os
import re
import socket
import shutil
import zipfile

def extract_zip(zip_path, extract_dir):
    """Extracts the given zip file into extract_dir."""
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"📂 Extracted files to {extract_dir}")

def resolve_auth_in_file(lines):
    """
    Ensures 'auth-user-pass' and 'redirect-gateway def1' exist in the .ovpn lines.
    Returns modified lines.
    """
    modified = []
    redirect_added = False
    auth_added = any("auth-user-pass" in line for line in lines)

    for line in lines:
        stripped = line.strip()
        # Insert redirect-gateway before <ca>
        if stripped == "<ca>" and not redirect_added:
            modified.append("redirect-gateway def1\n")
            redirect_added = True
        # Normalize auth-user-pass
        if stripped.startswith("auth-user-pass"):
            modified.append("auth-user-pass /home/<username>/vpn-auth.txt\n")
            continue

        modified.append(line)

    if not auth_added:
        modified.insert(0, "auth-user-pass /home/<username>/vpn-auth.txt\n")

    return modified

def resolve_host_in_file(lines):
    """Resolves hostnames in 'remote' lines and returns modified lines."""
    modified = []
    for line in lines:
        if line.strip().startswith("remote "):
            parts = line.strip().split()
            if len(parts) == 3:
                _, host, port = parts
                try:
                    ip_addr = socket.gethostbyname(host)
                    print(f"[+] {host} resolved to {ip_addr}")
                    modified.append(f"remote {ip_addr} {port}\n")
                except Exception as e:
                    print(f"[!] Failed to resolve {host}: {e}")
                    modified.append(line)
            else:
                modified.append(line)
        else:
            modified.append(line)
    return modified

def rename_file(filename):
    """Removes NCVPN- prefix and -UDP/-TCP suffix."""
    name = re.sub(r"^NCVPN-", "", filename)
    return name.replace("-UDP", "").replace("-TCP", "")

def process_ovpn_files(input_dir, output_dir):
    """Processes all .ovpn files from extract_dir and writes to output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".ovpn"):
            path = os.path.join(input_dir, filename)
            with open(path, "r") as f:
                lines = f.readlines()
            lines = resolve_host_in_file(lines)
            lines = resolve_auth_in_file(lines)
            new_name = rename_file(filename)
            output_path = os.path.join(output_dir, new_name)
            with open(output_path, "w") as f:
                f.writelines(lines)
            print(f"✅ Processed {filename} → {new_name}")

def clean_up(path):
    """Deletes the temporary extraction directory."""
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"🗑️ Deleted temporary folder: {path}")

def main():
    choice = input("Do you want to provide a ZIP file or a folder? [zip/folder]: ").strip().lower()
    if choice not in ["zip", "folder"]:
        print("❌ Invalid choice. Please enter 'zip' or 'folder'.")
        return

    if choice == "zip":
        zip_path = input("Enter the path to your VPN config zip file: ").strip()
        if not os.path.isfile(zip_path):
            print("❌ File not found. Exiting.")
            return
        extract_dir = "extracted_ovpn"
        extract_zip(zip_path, extract_dir)
        input_dir = extract_dir
        cleanup_needed = True
    else:  # folder
        input_dir = input("Enter the path to your folder with .ovpn files: ").strip()
        if not os.path.isdir(input_dir):
            print("❌ Folder not found. Exiting.")
            return
        cleanup_needed = False

    output_dir = input("Enter the output directory for patched configs: ").strip()
    process_ovpn_files(input_dir, output_dir)

    if cleanup_needed:
        clean_up(extract_dir)

    print(f"\n🎉 All files processed. Resolved configs saved in: {output_dir}")

if __name__ == "__main__":
    main()
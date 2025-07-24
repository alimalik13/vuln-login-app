# vulnapp.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Updated HTML_FORM: Title and heading changed, removed "demo" and "vulnerable"
HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYTAS - Login System</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 400px;
            box-sizing: border-box;
        }
        h2 {
            color: #333;
            margin-bottom: 25px;
            font-size: 1.8em;
            border-bottom: 2px solid #eee;
            padding-bottom: 15px;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: calc(100% - 20px);
            padding: 12px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 1em;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            transition: background-color 0.3s ease, transform 0.2s ease;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        hr {
            border: 0;
            height: 1px;
            background: #eee;
            margin: 25px 0;
        }
        .result-section {
            text-align: left;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 8px;
            margin-top: 20px;
            color: #333;
            font-size: 0.95em;
        }
        .result-section h3 {
            margin-top: 0;
            color: #007bff;
        }
        .result-section ul {
            list-style: none;
            padding: 0;
        }
        .result-section li {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
        }
        .error-message {
            color: #dc3545; /* Red color for error messages */
            font-weight: bold;
        }
        /* Responsive adjustments */
        @media (max-width: 600px) {
            .container {
                margin: 20px;
                padding: 20px;
            }
            h2 {
                font-size: 1.5em;
            }
            input[type="text"],
            input[type="password"],
            input[type="submit"] {
                padding: 10px;
                font-size: 0.95em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>CYTAS - Login System</h2>
        <form method="POST" action="/login">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="text" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <hr>
        <div class="result-section">
            {{ result|safe }}
        </div>
    </div>
</body>
</html>
'''

def vulnerable_login(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        # 🚨 SQL Injection Vulnerability (still present)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("[DEBUG] SQL:", query)
        result = cursor.execute(query).fetchall()
        conn.close()
        return result
    except Exception as e:
        # Return a specific error structure that can be easily identified
        return [("ERROR", f"Exception: {e}")]

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM, result="")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    users = vulnerable_login(username, password)

    # Check if the returned 'users' list contains an error message
    if users and users[0][0] == "ERROR":
        # 🚨 XSS Vulnerability: Reflecting username and error message directly into the HTML without sanitization
        # Try entering a username like: <script>alert('XSS!')</script>
        error_message = users[0][1] # Get the detailed exception message
        result = f"<h3 class='error-message'>❌ An error occurred for user '{username}':</h3><p class='error-message'>{error_message}</p>"
    elif users:
        result = "<h3>🎉 Logged in! Showing matching user(s):</h3><ul>"
        for u in users:
            # Ensure 'u' has enough elements before accessing them
            # This handles cases where a valid query might return fewer columns than expected,
            # though the primary fix is for the error handling path.
            if len(u) >= 6: # Check if the tuple has at least 6 elements (indices 0 to 5)
                result += f"<li>ID: {u[0]}, Username: {u[1]}, Email: {u[3]}, DOB: {u[4]}, Location: {u[5]}</li>"
            else:
                result += f"<li>Incomplete user data: {u}</li>" # Fallback for malformed data
        result += "</ul>"
    else:
        # 🚨 XSS Vulnerability: Reflecting username directly into the HTML without sanitization
        # Try entering a username like: <script>alert('XSS!')</script>
        result = f"<h3>❌ Login failed. No match found for user: {username}</h3>"
    return render_template_string(HTML_FORM, result=result)

if __name__ == "__main__":
    app.run(debug=True)

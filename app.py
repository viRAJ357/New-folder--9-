#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8080

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Demo Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6fb;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .card {
            width: 360px;
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        input {
            width: 100%;
            padding: 10px 12px;
            margin: 8px 0 16px;
            box-sizing: border-box;
            border: 1px solid #dfe3ea;
            border-radius: 8px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .message {
            margin-top: 12px;
            color: #1f2937;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Secure Demo Login</h2>
        <form method="POST" action="/">
            <label>Username</label>
            <input type="text" name="username" required />
            <label>Password</label>
            <input type="password" name="password" required />
            <button type="submit">Login</button>
        </form>
        <div class="message">This is a local demo only. No credentials are sent anywhere.</div>
    </div>
</body>
</html>
"""

VALID_USERS = {
    "demo": "password123"
}

class DemoLoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(LOGIN_HTML.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        form = parse_qs(raw, keep_blank_values=True)

        username = form.get("username", [""])[0]
        password = form.get("password", [""])[0]

        if VALID_USERS.get(username) == password:
            message = "Login successful"
            success = True
        else:
            message = "Invalid username or password"
            success = False

        payload = json.dumps({
            "success": success,
            "message": message
        }).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), DemoLoginHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
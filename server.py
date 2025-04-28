import socket
import threading
import os

# Configuration
HOST = 'localhost'
PORT = 8080
WEBROOT = 'webroot'
VALID_EXTENSIONS = {'.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript'}

# Helper function to send HTTP responses
def send_response(client_socket, status_code, status_message, content_type, content):
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    client_socket.sendall(response.encode() + content)

# Handles each client connection
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            client_socket.close()
            return

        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        print(f"Received request: {request_line}")

        if method != 'GET':
            error_body = b"<html><body><h1>Error 405: Method Not Allowed</h1></body></html>"
            send_response(client_socket, "405", "Method Not Allowed", "text/html", error_body)
            return

        # Prevent directory traversal
        safe_path = os.path.normpath(path).lstrip('/')
        full_path = os.path.join(WEBROOT, safe_path)

        # Validate file extension
        ext = os.path.splitext(full_path)[1]
        if ext not in VALID_EXTENSIONS:
            error_body = b"<html><body><h1>Error 403: Forbidden</h1></body></html>"
            send_response(client_socket, "403", "Forbidden", "text/html", error_body)
            return

        # Check if file exists
        if os.path.exists(full_path) and os.path.isfile(full_path):
            with open(full_path, 'rb') as f:
                content = f.read()
            send_response(client_socket, "200", "OK", VALID_EXTENSIONS[ext], content)
        else:
            error_body = b"<html><body><h1>Error 404: Page Not Found</h1></body></html>"
            send_response(client_socket, "404", "Not Found", "text/html", error_body)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Web server running on http://{HOST}:{PORT}/")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
        server_socket.close()

if __name__ == "__main__":
    start_server()

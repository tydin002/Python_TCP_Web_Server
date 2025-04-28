# python-tcp-web-server

A simple multi-threaded web server built with Python using TCP sockets.  
It handles basic HTTP GET requests and serves static `.html`, `.css`, and `.js` files from a `webroot/` directory.

## Features
- Supports serving static web files (HTML, CSS, JavaScript)
- Multi-threaded handling of multiple client connections
- Basic HTTP error responses: `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed`
- Prevents directory traversal attacks
- Configurable host and port settings

  ##Usage
 - Run server:
  python server.py
- Open browser and visit:
http://localhost:8080/index.html  

##Project Structure 
/python-tcp-web-server
  ├── server.py      # Main server code
  └── webroot/       # Folder containing static files (HTML, CSS, JS)
      ├── index.html
      ├── about.html
      ├── styles.css
      └── script.js

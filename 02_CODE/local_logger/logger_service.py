import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from logger import append_trade_event


class TradeEventHandler(BaseHTTPRequestHandler):
    """
    Simple HTTP handler for receiving TRADE_EVENT objects via POST.

    - Accepts POST /trade_event with JSON body.
    - Validates and appends the event using append_trade_event.
    - Returns a JSON response with status.
    """

    def _set_headers(self, status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

    def do_POST(self):
        if self.path != "/trade_event":
            self._set_headers(404)
            resp = {"status": "error", "message": "Not found"}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Parse JSON
        try:
            event = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._set_headers(400)
            resp = {"status": "error", "message": "Invalid JSON"}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # Try to append the trade event using our existing logger
        try:
            append_trade_event(event)
        except Exception as e:
            # Any validation or logging error becomes a 400 response
            self._set_headers(400)
            resp = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # Success
        self._set_headers(200)
        resp = {"status": "ok"}
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    # Optional: silence default logging to keep console cleaner
    def log_message(self, format, *args):
        return  # comment this out if you want default access logs


def run_server(host: str = "127.0.0.1", port: int = 8080):
    server_address = (host, port)
    httpd = HTTPServer(server_address, TradeEventHandler)
    print(f"TRUEEDGE logger service running on http://{host}:{port}")
    print("POST TRADE_EVENT JSON to /trade_event to log an event.")
    print("Press Ctrl+C in this window to stop the server.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        httpd.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    run_server()

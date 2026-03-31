from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from g4f.client import Client

client = Client()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query params
            query = parse_qs(urlparse(self.path).query)

            prompt = query.get("prompt", [""])[0]
            model = query.get("model", ["bing"])[0]

            if not prompt:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing prompt"}).encode())
                return

            # Generate image
            response = client.images.generate(
                model=model,
                prompt=prompt,
                response_format="url"
            )

            image_url = response.data[0].url

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "prompt": prompt,
                "model": model,
                "image_url": image_url
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
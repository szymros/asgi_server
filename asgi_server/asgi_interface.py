class AsgiInterface:
    def __init__(self, parsed_requested: dict):
        self.body = parsed_requested.pop("body")
        self.body = b""
        self.scope = {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.5"},
            "scheme": "http",
        }
        self.scope.update(parsed_requested)
        self.response = {}

    # this is what  app uses to send the message to server
    async def send(self, message):
        self.response.update(message)

    # this is what server uses to send the message to the app
    async def receive(self):
        asgi_event = {"type": "http.request", "body": self.body, "more_body": False}
        return asgi_event

    async def run(self, app):
        await app(self.scope, self.receive, self.send)

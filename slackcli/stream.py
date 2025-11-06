from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

from . import errors
from . import names
from . import slack
from . import messaging
from . import token as token_module


def receive(sources):
    try:
        loop(sources)
    except KeyboardInterrupt:
        pass


def loop(sources):
    # Get the app-level token for Socket Mode
    app_token = token_module.load_app_token()
    if not app_token:
        app_token = token_module.ask_app_token()
        token_module.save_app_token(app_token)

    # Initialize Socket Mode client
    socket_client = SocketModeClient(
        app_token=app_token,
        web_client=slack.client()._web_client
    )

    def process_message(client: SocketModeClient, req: SocketModeRequest):
        # Acknowledge the request immediately
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # Handle events API messages
        if req.type == "events_api":
            event = req.payload.get("event", {})

            # Filter for message events (no subtype means it's a regular message)
            if event.get("type") == "message" and "subtype" not in event:
                channel_id = event.get("channel")
                if channel_id:
                    source_name = names.sourcename(channel_id)
                    if source_name in sources or "all" in sources:
                        print(messaging.format_incoming_message(source_name, event))

    # Register the message handler
    socket_client.socket_mode_request_listeners.append(process_message)

    # Connect and keep the connection alive
    socket_client.connect()

    # Block until interrupted
    from time import sleep
    try:
        while True:
            sleep(1)
    finally:
        socket_client.close()

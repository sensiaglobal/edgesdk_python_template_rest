"""subscriptions.py

Contains classes to create, delete and manage all active message subscriptions.
"""

import queue
import logging
import threading
import asyncio
from http import HTTPStatus

# Third party
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.serving import make_server

# Local
from api.hcc2_rest_schema import (
    SimpleMessage, ComplexMessage, DataPoint
)
from api import RestAPI
from config import AppConfig


class PortManager:
    """Manage the available ports for HCC2 message subscriptions."""

    def __init__(self, port_range):
        """Initialize the PortManager with a range of ports."""

        self.available_ports = set(range(port_range[0], port_range[1] + 1))
        self.allocated_ports = set()

    def allocate_port(self):
        """Allocate the next available port and mark it as in use."""

        if not self.available_ports:
            raise Exception("No ports available for allocation.")

        port = min(self.available_ports)
        self.available_ports.remove(port)
        self.allocated_ports.add(port)
        return port

    def release_port(self, port):
        """Release a port and make it available for reuse."""

        if port in self.allocated_ports:
            self.allocated_ports.remove(port)
            self.available_ports.add(port)

    def allocated_ports_list(self):
        """Get a list of currently allocated ports."""

        return sorted(self.allocated_ports)

    def available_ports_list(self):
        """Get a list of currently available ports."""

        return sorted(self.available_ports)


class WebhookListener:
    """A single HCC2 message subscription thread.
    
    Starts a flask application thread which routes POST data from a single subscription.
    Data recieved is placed into a thread safe FIFO queue.
    """

    def __init__(self, callback_api, port):
        self.callback_api = callback_api
        self.app = Flask(__name__)
        self.queue = queue.Queue()
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
        self.server_shutdown_event = threading.Event()

        # Ignore flask app logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.CRITICAL)

        # Route callback URL
        @self.app.route(self.callback_api, methods=['POST'])
        def webhook():
            try:
                data = request.get_json()

                # Simple Message
                if data.get("value", None) is not None:
                    self.queue.put(SimpleMessage(**data))

                # Complex Message
                elif (dp := data.get("datapoints", None)):
                    subtags = []

                    # Extract datapoints
                    for subtag in dp:
                        subtags.append(DataPoint(**subtag))

                    self.queue.put(
                        ComplexMessage(
                            data['topic'],
                            subtags,
                            data['msgSource']
                        )
                    )

                if data:
                    return jsonify({"status": "OK"}), 200

                return jsonify({"error": "invalid payload"}), 400

            except BadRequest as e:
                return jsonify({"error": str(e)}), 400
            except InternalServerError as e:
                return jsonify({"error": f"Internal server error {e}"}), 500

    def start_server(self):
        """Start webhook server."""
        if self.running:
            raise RuntimeError("Server already running.")

        def run():
            self.server = make_server(AppConfig.app_ip, self.port, self.app)
            self.running = True
            self.server.serve_forever()

        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        """Stop webhook server."""
        if not self.running:
            raise RuntimeError("Server not running.")
        self.server.shutdown()
        self.server_thread.join(timeout=1)
        self.running = False

    def get(self) -> SimpleMessage | ComplexMessage:
        """Retrieve the next value from the queue if available."""
        if not self.queue.empty():
            return self.queue.get()
        return None

    def latest(self) -> SimpleMessage | ComplexMessage:
        """Retrieve the latest value from the queue, discarding older values."""
        latest = None
        while not self.queue.empty():
            latest = self.queue.get()
        return latest

    @property
    def uri(self):
        """Full message subscription callback URI."""
        return f"http://{AppConfig.app_ip}:{self.port}{self.callback_api}"


class Subscriptions:
    """Class to manage active subscriptions."""

    subscription_api = RestAPI()
    active = {}

    # Exposed TCP ports for docker container
    port_manager = PortManager([14000, 14100])

    @classmethod
    def subscribe(cls, topic: str) -> bool:
        """Subscribe to an HCC2 message and create a webhook listener application on an unallocated port."""

        port = cls.port_manager.allocate_port()
        callback_uri = cls.subscription_api.subscribe(
            AppConfig.app_func_name,
            f"http://{AppConfig.app_ip}:{port}/api/subdata",
            topic)

        if callback_uri:

            # Create and start the webhook flask application
            webhook = WebhookListener('/api/subdata', port=port)
            webhook.start_server()

            cls.active.update({topic: webhook})

            return True
        return False

    @classmethod
    def unsubscribe(cls, topic: str) -> bool:
        """Unsubscribe from any number of HCC2 messages."""

        response = cls.subscription_api.unsubscribe(
            AppConfig.app_func_name,
            topic)

        if response.status_code == HTTPStatus.OK:
            webhook = cls.active[topic]

            cls.port_manager.release_port(webhook.port)
            webhook.stop_server()

            del cls.active[topic]

            return True
        return False

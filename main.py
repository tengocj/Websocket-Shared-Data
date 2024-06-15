import asyncio
import websockets
import json
import logging
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class WebSocketServer:
    def __init__(self):
        self.connected_clients = {}
        self.test_data = None
        self.data_cache = None
        self.cache_expiry = datetime.now()

    async def fetch_data(self):
        # Placeholder function to simulate data fetching from an external source
        await asyncio.sleep(2)  # Simulating a network delay
        fetched_data = {"data": f"Fetched data {random.randint(1, 100)}", "timestamp": datetime.now().isoformat()}
        return fetched_data

    async def update_test_data(self):
        while True:
            if not self.data_cache or datetime.now() >= self.cache_expiry:
                self.test_data = await self.fetch_data()
                self.data_cache = self.test_data
                self.cache_expiry = datetime.now() + timedelta(seconds=10)
                logging.info("Fetched new data and updated cache")

            if self.connected_clients:
                await asyncio.wait([client.send(json.dumps(self.test_data)) for client in self.connected_clients.values()])
                logging.info("Sent updated data to all connected clients")

            await asyncio.sleep(5)

    async def handler(self, websocket, path):
        client_id = id(websocket)
        self.connected_clients[client_id] = websocket
        logging.info(f"New client connected: {client_id}")

        try:
            async for message in websocket:
                await self.process_message(client_id, websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logging.info(f"Client disconnected: {client_id}")
        finally:
            self.connected_clients.pop(client_id, None)
            logging.info(f"Client removed: {client_id}")

    async def process_message(self, client_id, websocket, message):
        try:
            request = json.loads(message)
            if request.get("action") == "get_data":
                await websocket.send(json.dumps(self.test_data))
                logging.info(f"Sent data to client {client_id}")
            elif request.get("action") == "subscribe":
                # Client subscription logic can be implemented here
                logging.info(f"Client {client_id} subscribed for updates")
            elif request.get("action") == "unsubscribe":
                # Client unsubscription logic can be implemented here
                logging.info(f"Client {client_id} unsubscribed from updates")
        except json.JSONDecodeError:
            logging.error("Invalid JSON received")
        except Exception as e:
            logging.error(f"Error processing message from client {client_id}: {e}")

    async def main(self):
        server = await websockets.serve(self.handler, "localhost", 8765)
        logging.info("WebSocket server started on ws://localhost:8765")
        await self.update_test_data()

if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.main())

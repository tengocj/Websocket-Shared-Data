# WebSocket Server with Asyncio

This repository contains a WebSocket server built with Python's `asyncio` and `websockets` libraries. The server handles incoming connections, updates them with test data, and shares the same test data with clients to save resources.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install dependencies:
    ```sh
    pip install websockets
    ```

## Usage

1. Run the server:
    ```sh
    python server.py
    ```

2. The server will start on `localhost` at port `8765`.

## How It Works

- The server maintains a set of connected clients.
- It periodically updates a shared piece of test data fetched from an external source.
- It uses a data cache to avoid unnecessary fetches and sets a cache expiry time.
- When a client requests the test data, the server sends the current test data to the client.
- The server supports client subscriptions for updates.
- Comprehensive logging is implemented for traceability.

## Code Overview

- `WebSocketServer` class:
  - `fetch_data`: Placeholder function to simulate fetching data from an external source.
  - `update_test_data`: Periodically updates the test data with fetched data and sends it to all connected clients.
  - `handler`: Handles incoming WebSocket connections and messages.
  - `process_message`: Processes messages received from clients, including handling subscriptions.
  - `main`: Starts the WebSocket server and begins updating test data.

Feel free to modify the code and add more features as needed.

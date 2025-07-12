import gpiod
import asyncio
import websockets

# Set to keep track of connected WebSocket clients
connected_clients = set()

async def vcu_status():
    
    
    chip_name = "gpiochip6"
    line_offsets = list(range(7))  # Pins 0 to 7
    chip = gpiod.Chip(chip_name)
    
    # Request all 8 lines as inputs
    lines = [chip.get_line(offset) for offset in line_offsets]
    for line in lines:
        line.request(consumer="gpio-monitor", type=gpiod.LINE_REQ_DIR_IN)
    
    # Get initial values
    last_values = [line.get_value() for line in lines]
    print(f"Initial GPIO values: {':'.join(str(v) for v in last_values)}")
    
    try:
        # Send initial status to clients
        if connected_clients:
            status = ":".join(str(v) for v in last_values)
            await asyncio.gather(
                *[client.send(status) for client in connected_clients]
            )
        
        while True:
            # Read current values
            current_values = [line.get_value() for line in lines]
            
            # Check if any value has changed
            if current_values != last_values:
                status = ":".join(str(v) for v in current_values)
                print(f"GPIO values changed: {status}")
                # Broadcast new status to all connected clients
                if connected_clients:
                    await asyncio.gather(
                        *[client.send(status) for client in connected_clients]
                    )
                last_values = current_values[:]
            
            await asyncio.sleep(0.10)  # Non-blocking delay
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        # Release all lines and close chip
        for line in lines:
            line.release()
        chip.close()

async def handle_client(websocket):
    # Register the client
    connected_clients.add(websocket)
    print(f"Client connected. Active clients: {len(connected_clients)}")
    try:
        # Keep connection open, waiting for messages
        async for message in websocket:
            print(f"Received message from client: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)

async def main():
    # Start the WebSocket server
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("WebSocket server started on ws://0.0.0.0:8765")
    
    # Run GPIO monitoring concurrently
    await vcu_status()

def start_server():
    """Non-async function to start the WebSocket server and GPIO monitoring."""
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

if __name__ == "__main__":
    start_server()

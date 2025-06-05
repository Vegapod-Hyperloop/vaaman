import asyncio
import websockets
import serial
import threading
import time
import queue
import mvcu

# UART configurations
UART_PORTS = {
    'UART1': {'port': '/dev/ttyPERI0', 'letter': 'A'},
    'UART2': {'port': '/dev/ttyPERI1', 'letter': 'B'},
    'UART3': {'port': '/dev/ttyPERI2', 'letter': 'C'},
    'UART4': {'port': '/dev/ttyPERI3', 'letter': 'D'},
    'UART5': {'port': '/dev/ttyPERI4', 'letter': 'E'},
    'UART6': {'port': '/dev/ttyPERI5', 'letter': 'F'}
}
BAUDRATE = 1500000
TIMEOUT = 5  # Timeout in seconds
uarts = {}
# WebSocket configurations
WS_PORT = 8456

# Shared queue for UART messages to WebSocket
message_queue = queue.Queue()

# List to keep track of connected WebSocket clients
connected_clients = set()

# Lock for thread-safe printing
print_lock = threading.Lock()

def initialize_uarts():
    """Initialize UARTs and return the uarts dictionary."""
    global uarts
    for uart_name, uart_info in UART_PORTS.items():
        try:
            uart = serial.Serial(
                port=uart_info['port'],
                baudrate=BAUDRATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=TIMEOUT,
            )
            uarts[uart_name] = uart
            with print_lock:
                print(f"{uart_name} initialized on {uart_info['port']}")
        except serial.SerialException as e:
            with print_lock:
                print(f"{uart_name}: Error opening or configuring UART: {e}")
    return uarts

def receive_data(uart_name, uart, stop_event, source_letter, uarts):
    """Function to handle receiving data for a UART."""
    buffer = bytearray()
    in_packet = False
    
    while not stop_event.is_set():
        try:
            byte = uart.read(1)
            if byte:
                buffer.extend(byte)
                while True:
                    if not in_packet:
                        start_idx = buffer.find(b'$')
                        if start_idx == -1:
                            buffer.clear()
                            break
                        in_packet = True
                        buffer = buffer[start_idx + 1:]
                    else:
                        end_idx = buffer.find(b'@')
                        if end_idx == -1:
                            break
                        packet = buffer[:end_idx]
                        try:
                            message = packet.decode('utf-8', errors='ignore')
                            formatted_message = f"{source_letter}={message}"
                            print(source_letter, message)
                            # Trigger processing and response after every message
                            mvcu.process_and_respond(uart_name, source_letter, message, uarts)
                            
                            # Continue with original functionality
                            #with print_lock:
                            #    print(f"{uart_name} received: {formatted_message}")
                            #message_queue.put(formatted_message)
                        except UnicodeDecodeError:
                            with print_lock:
                                print(f"{uart_name}: Invalid UTF-8 data received")
                        buffer = buffer[end_idx + 1:]
                        in_packet = False
        except serial.SerialException as e:
            with print_lock:
                print(f"{uart_name}: Receive error: {e}")
            break

def send_data(uart_name, uarts, message, dest_letter):
    """Function to send data to a UART."""
    try:
        if uart_name not in uarts:
            raise KeyError(f"UART {uart_name} not found in uarts dictionary")
        uart = uarts[uart_name]
        packet = f"{message}!".encode('utf-8')
        uart.write(packet)
        uart.flush()
        with print_lock:
            print(f"{uart_name}: Sent: {packet.decode('utf-8', errors='ignore')}")
    except serial.SerialException as e:
        with print_lock:
            print(f"{uart_name}: Send error: {e}")
    except KeyError as e:
        with print_lock:
            print(f"{uart_name}: {e}")

async def handler(websocket, uarts):
    """Handle WebSocket connections."""
    connected_clients.add(websocket)
    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                with print_lock:
                    print(f"Received from client: {message}")
                if len(message) >= 5 and message[1:3] == '+^' and message[-1] == '^':
                    dest_letter = message[0]
                    payload = message[3:-1]
                    for uart_name, uart_info in UART_PORTS.items():
                        if uart_info['letter'] == dest_letter:
                            send_data(uart_name, uarts, payload, dest_letter)
                            break
                    else:
                        with print_lock:
                            print(f"Invalid destination letter: {dest_letter}")
                else:
                    with print_lock:
                        print(f"Invalid message format from client: {message}")
            except asyncio.TimeoutError:
                pass
            except websockets.ConnectionClosed:
                break
    finally:
        connected_clients.remove(websocket)
        with print_lock:
            print("Client disconnected")

async def send_ws_messages():
    """Send UART messages from queue to WebSocket clients."""
    while True:
        try:
            message = message_queue.get_nowait()
            if connected_clients:
                tasks = [asyncio.create_task(client.send(message)) 
                         for client in connected_clients]
                if tasks:
                    await asyncio.gather(*tasks)
            message_queue.task_done()
        except queue.Empty:
            await asyncio.sleep(0.1)

async def main():
    # Initialize UARTs
    initialize_uarts()
    stop_events = {}
    threads = []

    try:
        # Start UART receive threads
        for uart_name, uart_info in UART_PORTS.items():
            if uart_name in uarts:
                stop_events[uart_name] = threading.Event()
                receive_thread = threading.Thread(
                    target=receive_data,
                    args=(uart_name, uarts[uart_name], stop_events[uart_name], uart_info['letter'], uarts),
                    daemon=True
                )
                threads.append(receive_thread)
                receive_thread.start()

        # Start WebSocket server
        async def handler_wrapper(websocket):
            await handler(websocket, uarts)
        
        server = await websockets.serve(
            handler_wrapper,
            "0.0.0.0",
            WS_PORT
        )
        with print_lock:
            print(f"WebSocket server started on ws://localhost:{WS_PORT}")

        # Start sending UART messages to WebSocket clients
        await send_ws_messages()

    except Exception as e:
        with print_lock:
            print(f"Unexpected error: {e}")
    finally:
        for stop_event in stop_events.values():
            stop_event.set()
        for thread in threads:
            thread.join(timeout=1)
        for uart_name, uart in uarts.items():
            if uart.is_open:
                uart.close()
                with print_lock:
                    print(f"{uart_name}: UART device closed.")

if __name__ == "__main__":
    asyncio.run(main())

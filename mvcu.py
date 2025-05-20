import main
import breaking
import cooling
import battery
def process_and_respond(uart_name, source_letter, message, uarts):
    """    
    Args:
        uart_name (str): Name of the UART that received the message.
        source_letter (str): Letter assigned to the source UART.
        message (str): The received message.
        uarts (dict): Dictionary of all UART objects.
    """
    if source_letter == 'A':
        breaking.breaking_rec(message, uarts)
    if source_letter == 'B':
        cooling.cooling_rec(message, uarts)
    if source_letter == 'C':
        battery.battery_rec(message, uarts)
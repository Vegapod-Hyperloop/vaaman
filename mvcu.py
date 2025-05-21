import main
import braking
import cooling
import battery
import inverter 

def process_and_respond(uart_name, source_letter, message, uarts):
    """    
    Args:
        uart_name (str): Name of the UART that received the message.
        source_letter (str): Letter assigned to the source UART.
        message (str): The received message.
        uarts (dict): Dictionary of all UART objects.
    """
    if source_letter == 'A':
        battery.battery_rec(message, uarts)
    if source_letter == 'B':
        braking.braking_rec(message, uarts)
    if source_letter == 'C':
        cooling.cooling_rec(message, uarts)
    if source_letter == 'D':
        inverter.inverter_rec(message, uarts)
    # if source_letter == 'E':
        


def handle_shutdown():
    main.send_data('A', main.uarts['UART1'], '#0:1&', 'A')
    main.send_data('B', main.uarts['UART2'], '#1:1&', 'B')

def handle_cooling(state):
    if state == '1':
        main.send_data('C', main.uarts['UART3'], '#1&', 'C')
    else:
        main.send_data('C', main.uarts['UART3'], '#0&', 'C')
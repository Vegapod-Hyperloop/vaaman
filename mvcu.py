import logic

def process_and_respond(uart_name, source_letter, message, uarts):
    """
    Process the received message, perform calculations, and send a response to a desired UART.
    
    Args:
        uart_name (str): Name of the UART that received the message.
        source_letter (str): Letter assigned to the source UART.
        message (str): The received message.
        uarts (dict): Dictionary of all UART objects.
    """
    if source_letter == 'A' and int(message) < 20:
        target_letter = 'B'  # UART2 has letter 'B'
        response = 'error+engage-break'
        logic.send_data('UART2', uarts['UART2'], response, target_letter)
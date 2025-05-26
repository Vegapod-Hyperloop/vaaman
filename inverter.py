import main
import logging
import mvcu
def inverter_rec(message, uarts):

    input_string = message[2:] 
    logging.add_to_log(message, 'inverter')
    
    if not (input_string.startswith('$') and input_string.endswith('@')):
        raise ValueError("Input string must start with '$' and end with '@'")
    
    values = input_string[1:-1].split(':')
    if len(values) != 12:
        raise ValueError("Expected 12 values in the string")
    try:
        DS1 = float(values[0])
        DS2 = float(values[1])
        DS3 = float(values[2])
        DS4 = float(values[3])
        CS1 = float(values[4])
        CS2 = float(values[5])
        CS3 = float(values[6])
        CS4 = float(values[7])
        CS5 = float(values[8])
        CS6 = float(values[9])
        LIEF = values[10] == '1'
        RIEF = values[11] == '1'

        if RIEF or LIEF:
            logging.add_to_log('RIEF or LIEF error raised', 'inverter')
            mvcu.handle_shutdown()
            return
        for i, CS in enumerate([CS1, CS2, CS3, CS4, CS5, CS6], 1):
            if CS > 35.0:
                logging.add_to_log(f"{CS} > 35.0", 'inverter')
                mvcu.handle_shutdown()
                return
        
        return
    except ValueError as e:
        logging.error(f"Error parsing message {message}: {str(e)}")
        raise ValueError(f"Invalid value format in string: {str(e)}") from e

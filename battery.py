import mvcu
import logging
def battery_rec(message, uarts):
    return
    input_string = message[2:]
    logging.add_to_log(message, 'battery')
    
    if not (input_string.startswith('$') and input_string.endswith('@')):
        raise ValueError("Input string must start with '$' and end with '@'")
    
    values = input_string[1:-1].split(':')
    if len(values) != 27:
        raise ValueError("Expected 13 values in the string")

    try:
        HVTV = [float(v) for v in values[0:8]]
        HVCV = [float(v) for v in values[8:56]]        
        HVSOC = [float(v) for v in values[56:64]]      
        HVT = [float(v) for v in values[64:112]]       
    except ValueError as e:
        logging.error(f"Error parsing message {message}: {str(e)}")
        raise ValueError(f"Invalid value format in string: {str(e)}") from e
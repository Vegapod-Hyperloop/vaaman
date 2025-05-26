import mvcu
import logging
def imu_rec(message, uarts):
    input_string = message[2:]
    logging.add_to_log(message, 'imu')
    
    if not (input_string.startswith('start') and input_string.endswith('stop')):
        raise ValueError("Input string must start with 'stop' and end with 'stop'")
    
    
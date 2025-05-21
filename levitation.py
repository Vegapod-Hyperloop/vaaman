import main
import logging

def levitation_front_rec(message, uarts):

    input_string = message[2:] 
    logging.add_to_log(message, 'levitation-front')
    
    if not (input_string.startswith('$') and input_string.endswith('@')):
        raise ValueError("Input string must start with '$' and end with '@'")
    
    values = input_string[1:-1].split(':')
    if len(values) != 16:
        raise ValueError("Expected 16 values in the string")
    # try:
    #     DS1 = float(values[0])
    #     DS2 = float(values[1])
    #     T1 = float(values[2])
    #     T2 = float(values[3])
    #     T3 = float(values[4])
    #     T4 = float(values[5])
    #     CS1 = float(values[6])
    #     CS2 = float(values[7])
    #     DEF = values[8] == '1'
    #     TEF = values[9] == '1'
    #     CEF = values[10] == '1'
    #     return DS1, DS2, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14

import mvcu
#import logging
def battery_rec(message, uarts):
    
    values = message.split(':')
    print(len(values))
    if len(values) != 112:
        raise ValueError("Expected 112 values in the string")

    try:
        HVTV = [float(v) for v in values[0:8]]
        HVCV = [float(v) for v in values[8:56]]        
        HVSOC = [float(v) for v in values[56:64]]      
        HVT = [float(v) for v in values[64:112]]
               
    except ValueError as e:
        #logging.error(f"Error parsing message {message}: {str(e)}")
        raise ValueError(f"Invalid value format in string: {str(e)}") from e

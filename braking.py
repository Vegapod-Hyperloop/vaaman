#import logging
import mvcu

def braking_rec(message, uarts=None):
    """
    Args:
        message (str): The received message.
        uarts (dict, optional): Dictionary of all UART objects. Defaults to None.
    """
    
    values = message.split(":")
    print(len(values))
    if len(values) != 13:
        raise ValueError("Expected 13 values in the string")
    
    try:
        # Parse P1-P4 as floats and validate range (5.5 to 10.0)
        P1 = float(values[0])
        P2 = float(values[1])
        P3 = float(values[2])
        P4 = float(values[3])
        BS = values[4] == '1'
        E1 = values[5] == '1'
        E2 = values[6] == '1'
        E3 = values[7] == '1'
        E4 = values[8] == '1'
        TL = values[9] == '1'
        TR = values[10] == '1'
        BL = values[11] == '1'
        BR = values[12] == '1'
        print("Values:", values)
        
        for i, p in enumerate([P1, P2, P3, P4], 1):
            if not 5.5 <= p <= 10.0:
                #logging.add_to_log(f"P{i} value {p} is out of range [5.5, 10.0]", 'breaking')
                print("issue")
                mvcu.handle_shutdown()

                # raise ValueError(f"P{i} value {p} is out of range [5.5, 10.0]")

        for i, e in enumerate([E1, E2, E3, E4], 1):
            if e == '1':
                #logging.add_to_log(f"Error in E{i}", 'breaking')
                mvcu.handle_shutdown()
                # raise ValueError(f"E{i} value {e} is out of range [0, 1]")
        
        #Check for TL, TR, BL, BR if they match with Web Socket 
        return {
            'P1': P1,
            'P2': P2,
            'P3': P3,
            'P4': P4,
            'BS': BS,
            'E1': E1,
            'E2': E2,
            'E3': E3,
            'E4': E4,
            'TL': TL,
            'TR': TR,
            'BL': BL,
            'BR': BR
        }
    except ValueError as e:
        #logging.error(f"Error parsing message {message}: {str(e)}")
        raise ValueError(f"Invalid value format in string: {str(e)}") from e

# # Example usage
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     try:
#         result = braking_rec('B+$6.5:7.3:8.7:9.2:1:1:0:1:0:1:0:1:0@')
#         print(result)
#     except ValueError as e:
#         print(f"Error: {e}")

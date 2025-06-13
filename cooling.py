# import main
#import logging
import mvcu
def cooling_rec(message, uarts):
    """    
    Args:
        uart_name (str): Name of the UART that received the message.
        source_letter (str): Letter assigned to the source UART.
        message (str): The received message.
        uarts (dict): Dictionary of all UART objects.
    """
    #logging.add_to_log(message, 'cooling')
    
    values = message.split(':')
    if len(values) != 27:
        raise ValueError("Expected 13 values in the string")
    try:
        t1 = float(values[0])
        t2 = float(values[1])
        t3 = float(values[2])
        t4 = float(values[3])
        t5 = float(values[4])
        t6 = float(values[5])
        t7 = float(values[6])
        t8 = float(values[7])
        t9 = float(values[8])
        t10 = float(values[9])
        t11 = float(values[10])
        t12 = float(values[11])
        t13 = float(values[12])
        t14 = float(values[13])
        t15 = float(values[14])
        t16 = float(values[15])
        t17 = float(values[16])
        t18 = float(values[17])
        t19 = float(values[18])
        t20 = float(values[19])
        FS1 = float(values[20])
        FS2 = float(values[21])
        LS = float(values[22])
        PS = values[23] == '1'
        TEF = values[24] == '1'
        FSEF = values[25] == '1'
        LSEF = values[26] == '1'
        tempratures = [float(v) for v in values[0:20]]
        
        for i, t in enumerate(tempratures, 1):
            if t >= 80.0:
                #logging.add_to_log(f"P{i} value {p} is out of range [5.5, 10.0]", 'breaking')
                print("issue")
                mvcu.handle_shutdown()
        if FSEF or LSEF:
            print("Cool off")
            mvcu.handle_cooling('0')
            mvcu.handle_shutdown()
            return
        else:
            print("Cool on")
            mvcu.handle_cooling('1')
            return
        #TODO: Verify Level sensor value  
        if LS < 20:
            mvcu.handle_cooling('0')
            mvcu.handle_shutdown()
            return
        if FS1 < 5000 or FS2 < 5000:
            mvcu.handle_cooling('0')
            mvcu.handle_shutdown()
            return
        return
    except ValueError as e:
        #logging.error(f"Error parsing message {message}: {str(e)}")
        raise ValueError(f"Invalid value format in string: {str(e)}") from e

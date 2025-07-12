import main
import logging
import mvcu

def levitation_front_rec(message, uarts):
    print(message)
    return
    input_string = message[2:] 
    logging.add_to_log(message, 'levitation-front')
    
    if not (input_string.startswith('$') and input_string.endswith('@')):
        raise ValueError("Input string must start with '$' and end with '@'")
    
    values = input_string[1:-1].split(':')
    if len(values) != 16:
        raise ValueError("Expected 16 values in the string")

    try:
        DSL = float(values[0])
        DSR = float(values[1])
        TLL = float(values[2])
        TLR = float(values[3])
        TRL = float(values[4])
        TRR = float(values[5])
        CSL = float(values[6])
        CSR = float(values[7])
        DEF = values[8] == '1'
        TEF = values[9] == '1'
        CEF = values[10] == '1'
        PO = float(values[11])
        IO = float(values[12])
        DO = float(values[13])
        CCLEF = values[14] == '1'
        CCREF = values[15] == '1'

        if DEF or TEF or CEF or CCLEF or CCREF:
            logging.add_to_log('DEF or TEF or CEF or CCLEF or CCREF error raised', 'levitation-front')
            mvcu.handle_shutdown()
            return
        if CSL > 20 or CSR > 20:
            logging.add_to_log('CSL or CSR error out of range', 'levitation-front')
            mvcu.handle_shutdown()
            return
        for i, T in enumerate([TLL, TLR, TRR, TRR], 1):

            if T >= 80.0:
                logging.add_to_log(f"{T} < 80.0 temprature warning", 'levitation-front')
            if T >= 100.0:
                logging.add_to_log(f"{T} > 100.0 temprature error", 'levitation-front')
                mvcu.handle_shutdown()
                return

    except:
        logging.add_to_log('error in levitation_front_rec', 'levitation-front')
        main.mvcu.handle_shutdown()
        return

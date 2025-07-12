import gpiod
import time




def vcuStatus():
    chip_name = "gpiochip6"
    line_offset = 7
    chip = gpiod.Chip(chip_name)
    line = chip.get_line(line_offset)
    line.request(consumer="gpio-monitor", type=gpiod.LINE_REQ_DIR_IN)

    last_value = line.get_value()
    print(f"Initial GPIO value: {'HIGH' if last_value else 'LOW'}")
    try:
        while True:
            current_value = line.get_value()
            if current_value != last_value:
                print(f"GPIO changed: {'HIGH' if current_value else 'LOW'}")
                last_value = current_value
            time.sleep(0.10)  # Slight delay to prevent CPU hogging
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        line.release()
        chip.close()

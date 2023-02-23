import serial
from src import get_data
import keyboard as kb

if __name__ == "__main__":

    # get_data(keyboard='q')
    while True:
        try:
            if kb.is_pressed('q'):  # -> click
                print("qqq")
                get_data(keyboard='q')
            if kb.is_pressed('w'):  # -> begin
                print("www")
                get_data(keyboard='w')
            if kb.is_pressed('e'):  # -> end
                get_data(keyboard='e')
            if kb.is_pressed('r'):  # -> press
                get_data(keyboard='r')
            if kb.is_pressed('t'):  # -> drop
                get_data(keyboard='t')
            if kb.is_pressed('m'):
                print("Out!")
                break
        except:
            break

import os
import re
import subprocess
import time

import EM4325

PORT_COM = 17

def uhf_read(testing: bool = False):
    devices = []

    if testing:
        with open('test_read_uhf', 'r') as file:
            data = file.read().rstrip()
    else:
        data = subprocess.check_output(os.path.abspath(os.getcwd()) + "\\Read.exe tmr:///com" + str(PORT_COM) + " --ant 1", shell=True, text=True)

    if (match := re.findall(EM4325.REGEX, data)) is not None:
        for m in match:
            device = EM4325.Device(m)
            devices.append(device)

    return devices


def uhf_leds(tag_id: int, led1: bool, led2: bool):
    cmd = os.path.abspath(os.getcwd()) + \
    "\\Leds.exe tmr:///com" + str(PORT_COM) + \
          " --ant 1 --led1 " + str(int(led1)) + \
          " --led2 " + str(int(led2)) + \
          " --epc " + str(tag_id)
    
    print(cmd)
    subprocess.check_output(cmd,
          shell=True, text=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    toggle = True
    while True:
        toggle = not toggle
        devices = uhf_read(testing=False)
        print("\n==================================================")
        print("Read UHL: ")
        n = 0
        for device in devices:
            print("Tag id n°" + str(n) + ": " + str(device.tag_id))
            if n % 2 == 1:
                uhf_leds(device.tag_id, toggle, not toggle)
            else:
                uhf_leds(device.tag_id, not toggle, toggle)
            n += 1
        print("==================================================\n")
        time.sleep(1)

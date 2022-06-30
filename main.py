import os
import re
import subprocess
import time

import EM4325
import test

COMMAND = "D:\\Users\\Gabin\\OneDrive\\Documents\\Cours\\S10\\RFID\\CS\\cs\\Samples\\Codelets\\Read\\bin\\Debug\\Read.exe"


def uhf_read(testing: bool = False):
    devices = []

    if testing:
        with open('test_read_uhf', 'r') as file:
            data = file.read().rstrip()
    else:
        res = subprocess.run([COMMAND, "tmr:///com4", "--ant 1"], capture_output=True, text=True)
        data = res.stdout

    if (match := re.findall(EM4325.REGEX, data)) is not None:
        for m in match:
            device = EM4325.Device(m)
            devices.append(device)

    return devices


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        print("\n==================================================")
        print("Read UHL: ")
        devices = uhf_read(testing=True)
        n = 0
        for device in devices:
            print("Tag id n°" + str(n) + ": " + str(device.tag_id))
            n += 1
        print("==================================================\n")
        time.sleep(1)

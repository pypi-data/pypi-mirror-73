import re
import time
import serial
import asyncio

from serial.tools import list_ports
from serial.serialutil import SerialException


def find_usb(timeout=10, print_countdown=False):
    timeout_at = time.time() + timeout
    found_kyanit = None

    def get_serial_devices():
        return [port.device for port in list_ports.comports()]

    async def read_port(device):
        nonlocal found_kyanit
        
        while True:
            try:
                ser = serial.Serial(device, 115200)
            except SerialException:
                # can not open serial device
                if found_kyanit is not None or time.time() > timeout_at:
                    # another concurrent task found the Kyanit, or we timed out
                    return
                await asyncio.sleep(0)
            else:
                # open successful
                break
        
        in_bytes = b''
        while True:
            if found_kyanit is not None or time.time() > timeout_at:
                # Kyanit was found, or we timed out
                ser.close()
                return
            if ser.inWaiting():
                in_bytes += ser.read(ser.inWaiting())
            if b'KYANIT Run.' in in_bytes:
                kyanit_fw_ver = re.search(br'KYANIT Version: (.*)\r\n', in_bytes).group(1).decode()
                kyanit_id = re.search(br'KYANIT ID: (.*)\r\n', in_bytes).group(1).decode()
                found_kyanit = {
                    'port': device,
                    'version': kyanit_fw_ver,
                    'id': kyanit_id
                }
            if len(in_bytes) > 512:
                in_bytes = in_bytes[-512:]
            await asyncio.sleep(0)
    
    async def countdown():
        for i in range(int(timeout * 10), 0, -1):
            if print_countdown:
                print('Waiting...{:>5}'.format(i / 10), end='\r')
            if found_kyanit is not None:
                # Kyanit was found
                return
            await asyncio.sleep(.1)

    async def start_finding():
        # attempt to open all serial devices
        tasks = [task for task in [asyncio.create_task(read_port(device))
                                   for device in get_serial_devices()]]
        tasks.append(asyncio.create_task(countdown()))
        await asyncio.gather(*tasks)
        if print_countdown:
            print()

    asyncio.run(start_finding())

    return found_kyanit


if __name__ == '__main__':
    print('Kyanit must be connected through USB.')
    print('Press RESET on Kyanit now!')
    kyanit = find_usb(15, print_countdown=True)
    if kyanit is None:
        print('Timed out.')
    else:
        print('Kyanit {id} found on {port} (fw: {version}) '
              .format(**kyanit))

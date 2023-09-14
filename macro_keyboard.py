import evdev
import os
import time
import requests
import json

def list_devices():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for i, device in enumerate(devices):
        print(f"{i+1}: {device.name}")
    return devices

def send_post_request(status):
    url = "/update-status"  # Replace with your actual URL
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'current_status': status})

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print("Successfully updated status:", response.json())
        else:
            print("Failed to update status:", response.text)
    except Exception as e:
        print("Error:", e)

def main():
    print("Listing available devices...")
    devices = list_devices()
    choice = int(input("Choose the device number you want to listen to: "))

    dev = devices[choice-1]

    print("Listening to device:", dev.name)

    while True:
        try:
            for event in dev.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    data = evdev.categorize(event)
                    if data.keystate == 1:  # Down events only
                        print(f"You Pressed the {data.keycode} key!")
                        if 2 <= data.scancode <= 4:
                            send_post_request(data.scancode)
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()

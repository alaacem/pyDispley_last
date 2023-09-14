import hid
import usb.core
import usb.util

# Find your device by Vendor ID and Product ID
VENDOR_ID = 0x8089  # Convert to hexadecimal
PRODUCT_ID = 0x0003  # Convert to hexadecimal

dev = hid.device()
dev.open(VENDOR_ID, PRODUCT_ID)

# Or use pyusb
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found')

import bmpsensor
import hmcsensor
import time

from pathlib import Path
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont


def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)

def main():
    fontname,size = ("DejaVuSansMono.ttf",12)
    font = make_font(fontname, size) if fontname else None

    fontname2,size2 = ("FreePixel.ttf",13)
    font2 = make_font(fontname2, size2) if fontname else None
    sensor = bmpsensor.bmp180()
    compass = hmcsensor.hmc5883l(gauss = 4.7, declination = (-2,5))
    while True:
        temp, pressure, altitude = sensor.readBmp180()
        (x ,y ,z) = compass.axes()
        print("Temperature is ",temp)  # degC
        print("Pressure is ",pressure) # Pressure in Pa
        print("Altitude is ",altitude) # Altitude in meters
        print("\n")
        print('Axis X: {0:0.2f}, Axis Y: {1:0.2f}, Axis Z: {2:0.2f}'.format(x,y,z))
        print("Heading: " +str(compass.degrees(compass.heading())))
        with canvas(device) as draw:
            draw.text((0, 0),"Temp:{0:0.1f} lat:{1:0.2f}".format(temp,altitude), font=font2, fill="white")
            draw.text((0, 13),"atm: {0:05d}".format(pressure), font=font, fill="white")
            draw.line((0, 27, device.width, 27), fill="white")
            draw.text((0, 28),"Axis X:{0:0.2f}".format(x), font=font, fill="white")
            draw.text((0, 40),"Axis Y:{0:0.2f}".format(y), font=font, fill="white")
            draw.text((0, 52),"Axis Z:{0:0.2f}".format(z), font=font, fill="white")
        time.sleep(2)

if __name__ == "__main__":
    try:
        serial = i2c(port=0, address=0x3C)
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass
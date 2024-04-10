from thonny import rp2040
#import thonny.plugins.micropython.rp2040 as rp2040

# Replace 'COM3' with your Pico's port
pico = rp2040.Pico(port='COM7') 
pico.connect()

# Write your MicroPython script here
script = """
import machine
led = machine.Pin(25, machine.Pin.OUT)
led.toggle()
"""

# Transfer and run the script on Pico
pico.run(script)

pico.disconnect()
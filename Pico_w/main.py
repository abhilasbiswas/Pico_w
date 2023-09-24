import network
import machine
from machine import Pin
import time as t
from socket import socket

ssid = "Wifi name" #enter the targeted wifi name
pswd = "password" #enter the targeted wifi password
port = 80

pin = Pin("LED", Pin.OUT)


def page_on():
    return """
        <html lang="en">
        <body>
            <form action="./lighton">
                <input type="submit" value="on">
            </form>
            
        </body>
        </html>
        """

def page_off():
    return """
        <html lang="en">
        <body>
            <form action="./lightoff">
                <input type="submit" value="off">
            </form>
        </body>
        </html>
        """


def led_on():
    global pin
    print("Turning on...")
    pin.high()
    pass

def led_off():
    global pin
    print("Turning off...")
    pin.low()

def connect():
    print("connecting...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pswd)
    while wlan.isconnected() == False:
        t.sleep(1)
        pass
    
    ip = wlan.ifconfig()[0]
    print(f"Connected to {ip}\n Open browser and navigate to {ip}")
    return (ip, port)

def open_socket(addr):
    print("starting the server...")
    connetion = socket()
    connetion.bind(addr)
    connetion.listen(5)
    print("server started")
    return connetion

def serve(connection):
    global n
    while True:
        try:
            client = connection.accept()[0]
            req = client.recv(1024)
            req = str(req).split()[1]
            if req == "/lighton?":
                led_on()
                client.send(page_off())
            
            if req == "/lightoff?":
                led_off()
                client.send(page_on())
            
            
            client.close()
        except KeyboardInterrupt:
            client.close()
            break

try:
    addr = connect()
    connection = open_socket(addr)
    serve(connection)

except KeyboardInterrupt:
    machine.reset()


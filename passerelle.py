import serial
import serial.tools.list_ports as list_ports
import time
import paho.mqtt.client as mqtt
import requests
import os
from dotenv import load_dotenv


PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None


if __name__ == '__main__':
    load_dotenv()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv('MQTT_BROKER_HOST'), int(os.getenv('MQTT_BROKER_PORT')), 60)

    try:
        # Ouvrir le port série
        ser = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
        data = requests.get('ifconfig.me').text

        # Envoie la chaîne via la liaison série
        ser.write(data.encode())

    except serial.SerialException:
        print(f"Le port série n'a pas pu être ouvert. Assurez-vous que le périphérique est correctement connecté.")
    except KeyboardInterrupt:
        # Gérer l'interruption (Ctrl+C) pour fermer proprement le port série
        ser.close()
        print("Fermeture du port série.")

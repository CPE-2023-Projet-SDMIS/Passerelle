import serial
import re
import time
import paho.mqtt.client as mqtt
import requests
import os
from dotenv import load_dotenv


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


if __name__ == '__main__':
    load_dotenv()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.MQTT_BROKER_HOST, os.MQTT_BROKER_PORT, 60)

    #Port série utilisé
    port = '/dev/ttyACM0'

    # Paramètres de la communication série
    baudrate = 115200

    try:
        # Ouvrir le port série
        ser = serial.Serial(port, baudrate)
        data = requests.get('ifconfig.me').text

        # Envoie la chaîne via la liaison série
        ser.write(data.encode())

    except serial.SerialException:
        print(f"Le port série {port} n'a pas pu être ouvert. Assurez-vous que le périphérique est correctement connecté.")
    except KeyboardInterrupt:
        # Gérer l'interruption (Ctrl+C) pour fermer proprement le port série
        ser.close()
        print("Fermeture du port série.")

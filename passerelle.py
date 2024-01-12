import serial
import serial.tools.list_ports as list_ports
import time
import paho.mqtt.client as mqtt
import requests
import os
import json
from dotenv import load_dotenv


# connect to the broker
def on_connect(client, userdata, flags, rc):
    print("mqtt connection result code : "+str(rc))
    client.subscribe("simulator/SensorEvents")

# mqtt message received
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "simulator/SensorEvents":
        print("Message reçu du simulateur")
        message = msg.payload.decode('utf-8')
        print("event id received via mqtt : " + message)


        # json_data = requests.get(API_URL + "/api/passerelle/getEvent?eventid=" + message).text
        json_data = '[{"sensorID":1,"intensity":5},{"sensorID":2,"intensity":5},{"sensorID":5,"intensity":5},{"sensorID":99,"intensity":5}]'
        data = json.loads(json_data)

        serial_string = ""
        for i in range(15):
            if i < len(data):
                serial_string = serial_string + str(data[i]["sensorID"]) + " " + str(data[i]["intensity"]) + " "
            else:
                serial_string = serial_string + "0 0 "
        serial_string = serial_string[:-1]
        print("serial string : " + serial_string)
        ser.write(serial_string.encode() + b'\n')




if __name__ == '__main__':
    load_dotenv()

    MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST')
    MQTT_BROKER_PORT = os.getenv('MQTT_BROKER_PORT')
    MQTT_USERNAME = os.getenv('MQTT_USERNAME')
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
    API_URL = os.getenv('API_URL')


    print("mqtt host : " + MQTT_BROKER_HOST)
    print("mqtt port : " + MQTT_BROKER_PORT)
    print("mqtt username : " + MQTT_USERNAME)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60)

    try:
        # Ouvrir le port série
        ser = serial.Serial(os.getenv('SERIAL_PORT'), int(os.getenv('SERIAL_BAUDRATE')))
        data = requests.get('https://ifconfig.me').text

        # Envoie la chaîne via la liaison série
        ser.write(data.encode())
        print("Envoi de la chaîne : " + data)
        client.loop_forever()
    except serial.SerialException:
        print(f"Le port série n'a pas pu être ouvert. Assurez-vous que le périphérique est correctement connecté.")
    except KeyboardInterrupt:
        # Gérer l'interruption (Ctrl+C) pour fermer proprement le port série
        ser.close()
        print("Fermeture du port série.")

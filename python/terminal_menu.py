#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import signal
import traceback
import string
import ssl

import json
import requests
import random
import paho.mqtt.client as mqtt

from dotenv import load_dotenv
from json_texts import ORG_NUM, get_json_example

# Ensure the .env file is loaded from the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path, override=True)

# Credenciales MQTT
ORG_NAME = os.getenv('CLIENTE_ID')
MQTT_USE_TLS = os.getenv('MQTT_USE_TLS')
MQTT_CERT_FILE_PATH = os.path.join(current_dir, os.getenv('MQTT_CA_FILE'))
MQTT_CLIENT_ID = os.getenv('CLIENTE_ID')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_SERVERURL = os.getenv('MQTT_SERVER_HOST')
MQTT_SERVERPORT = int(os.getenv('MQTT_SERVER_PORT'))
MQTT_TOPIC_TO_SEND = os.getenv('MQTT_TOPIC_TO_SEND')
MQTT_TOPIC_TO_RECEIVE = os.getenv('MQTT_TOPIC_TO_RECEIVE')
MQTT_QOS = int(os.getenv('MQTT_QOS', 2))
MQTT_KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE', 60))

contador_global_de_respuestas = 0

def send_to_mqtts(topic, msg, print_topic_and_msg):
	if print_topic_and_msg == True:
		os.write(sys.stdout.fileno(), topic.encode('utf-8'))
		os.write(sys.stdout.fileno(), msg.encode('utf-8'))
		os.write(sys.stdout.fileno(), "\n".encode('utf-8'))

	mqtt_client.publish(MQTT_TOPIC_TO_SEND, msg, qos=MQTT_QOS, retain=False)

def on_connect(client, userdata, flags, rc):
	print("Connected to broker")
	client.subscribe(MQTT_TOPIC_TO_RECEIVE)

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Client disconnected successfully.")
    else:
        print(f"MQTT Error #{rc}")

def on_log(client, userdata, level, buf):
	#print("Buffer ", buf)
	pass

def on_message(client, userdata, msg):
	global contador_global_de_respuestas
	mqtt_msg = ""
	mqtt_msg = msg.payload.decode('utf-8')
	#mqtt_msg = mqtt_msg.replace("b'","")
	#mqtt_msg = mqtt_msg.replace("'","\"")
	#mqtt_msg = mqtt_msg.replace("”","\"")
	try:
		json_msg = json.loads(mqtt_msg)
		contador_global_de_respuestas += 1
		respuesta_a_imprimir = "Respuesta : " + str(contador_global_de_respuestas) + " - " + mqtt_msg

		# Check if the ORG_NAME is the same as the one in the .env file
		nombre_de_organizacion = ""
		nombre_de_organizacion = json_msg['gym']
		if nombre_de_organizacion == "" or nombre_de_organizacion != ORG_NAME:
			return
		else:
			respuesta_a_imprimir = "Respuesta : " + str(contador_global_de_respuestas) + " - " + json.dumps(json.loads(mqtt_msg), indent=4, sort_keys=True)
			print(respuesta_a_imprimir)
	except:
		print("\n\n\nError al convertir el mensaje recibido a JSON\n\n\n")
		return

#############################################
######### MQTT CLIENT CONFIGURATION #########
#############################################

mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.on_log = on_log

# Update TLS configuration
if MQTT_USE_TLS.lower() == "true":
    if os.path.isfile(MQTT_CERT_FILE_PATH):
        try:
            mqtt_client.tls_set(
                MQTT_CERT_FILE_PATH,
                tls_version=ssl.PROTOCOL_TLSv1_2  # Explicitly set TLS version
            )
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            sys.exit(1)
    else:
        print(f"Error: Certificate file not found at {MQTT_CERT_FILE_PATH}")
        sys.exit(1)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_SERVERURL, MQTT_SERVERPORT, keepalive=MQTT_KEEPALIVE)

# Signal handler for graceful shutdown
def handle_exit_signal(signum, frame):
    print("\nSignal received, shutting down...")
    try:
        if mqtt_client.is_connected():
            mqtt_client.disconnect()
            mqtt_client.loop_stop()
            print("MQTT client disconnected successfully.")
    except Exception as e:
        print(f"Error during MQTT disconnection: {e}")
    finally:
        sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_exit_signal)
signal.signal(signal.SIGTERM, handle_exit_signal)

if __name__ == "__main__":
	mqtt_client.loop_start()
	
	os.system('clear')

	menu="---------------------------------------------\n"
	menu += "Username: " + MQTT_USERNAME + "\n"
	menu += "Topic to send: " + MQTT_TOPIC_TO_SEND + "\n"
	menu += "Topic to receive: " + MQTT_TOPIC_TO_RECEIVE + "\n"
	menu += "---------------------------------------------\n"
	menu += "1. Agregar sin fotografía (Toma unos 2.4 segundos)\n"
	menu += "2. Aplicar nivel de acceso\n"
	menu += "3. Obtener información de la persona con su mnt_id_persona\n"
	menu += "4. Editar un usuario (para editar la fotografía utiliza la opción 6)\n"
	menu += "5. Editar un rostro (Toma unos 5 - 7 segundos en responder)\n"
	menu += "6. Eliminar un usuario\n"
	menu += "7. Obtener el mnt_id_persona a partir del persona_id\n"
	menu += "8. Agregar varios usuarios\n"
	menu += "s. Salir...\n"
	print(menu)

	while True:
		# Agregar soporte apra CTRL-C y en ese caso enviar a handler
		# para que pregunte si se quiere salir o no
		input_text = input("")

		if input_text == '1':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('agregar_usuario'), False)
		elif input_text == '2':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('update_access_level'), False)
		elif input_text == '3':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('obtener_informacion_de_persona_por_id'), False)
		elif input_text == '4':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('editar_usuario'), False)
		elif input_text == '5':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('editar_rostro'), False)
		elif input_text == '6':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('eliminar_usuario'), False)
		elif input_text == '7':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('obtener_mnt_id_persona'), False)
		elif input_text == '8':
			# Digita la cantidad de usuarios que se desean simular
			cantidad_de_usuarios = input("Ingrese la cantidad de usuarios a simular: ")
			# Genera un conjunto de cuatro letras aleatorias
			id_en_letras = ''.join(random.choices(string.ascii_uppercase, k=4))
			json_people = []
			for i in range(int(cantidad_de_usuarios)):
				nombre_de_persona = id_en_letras + str(i)
				# Convert the json to a dictionary
				json_example = json.loads(get_json_example('agregar_usuarios_bulk'))
				json_example['body']['nombre'] = nombre_de_persona
				json_example['body']['persona_id'] = nombre_de_persona + str(i)
				json_people.append(json_example)

			for __json__ in json_people:
				# Convert dictionary to json string
				__json__ = json.dumps(__json__)
				# Print json beautified
				#print(json.dumps(json.loads(__json__), indent=4, sort_keys=True))
				# Send the json string to the MQTT server
				send_to_mqtts(MQTT_TOPIC_TO_SEND, __json__, False)

		elif input_text == 's' or input_text == 'S':
			os.system('clear')
			# Safely close the MQTT session
			try:
				if mqtt_client.is_connected():  # Check if the client is connected
					mqtt_client.disconnect()  # Disconnect first
					mqtt_client.loop_stop()  # Then stop the loop
			except Exception as e:
				pass  # Suppress any errors during disconnection
			finally:
				sys.exit(0)  # Exit silently with code 0
		else:
			print("\n\n\nOpción no válida\n\n\n")
		
		os.system('clear')
		print(menu)
		print("La respuesta se imprimirá a continuación...")
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import signal
import traceback
import string

import json
import requests
import random
import paho.mqtt.client as mqtt

from dotenv import load_dotenv
from json_texts import get_json_example

load_dotenv(override=True)

# Credenciales MQTT
MQTT_CERT_FILE_PATH = os.getenv('MQTT_CERT_FILE_PATH')
MQTT_CLIENT_ID = os.getenv('Cliente_ID')
MQTT_USERNAME = os.getenv('Cliente_Username')
MQTT_PASSWORD = os.getenv('Cliente_Password')
MQTT_SERVERURL = os.getenv('MQTT_SERVER_HOST')
MQTT_SERVERPORT = int(os.getenv('MQTT_SERVER_PORT'))
MQTT_TOPIC_TO_SEND = os.getenv('MQTT_TOPIC_TO_SEND')
MQTT_TOPIC_TO_RECEIVE = os.getenv('MQTT_TOPIC_TO_RECEIVE')

contador_global_de_respuestas = 0

def send_to_mqtts(topic, msg, print_topic_and_msg):
	if print_topic_and_msg == True:
		os.write(sys.stdout.fileno(), topic.encode('utf-8'))
		os.write(sys.stdout.fileno(), msg.encode('utf-8'))
		os.write(sys.stdout.fileno(), "\n".encode('utf-8'))
	mqtt_client.publish(MQTT_TOPIC_TO_SEND, msg, qos=2, retain=False)

def on_connect(client, userdata, flags, rc):
	print("Connected to broker")
	client.subscribe(MQTT_TOPIC_TO_RECEIVE)

def on_disconnect(client, userdata, rc):
	print("MQTT Error #", rc)
	print("Client disconnected ok")

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
		#json_msg = json.loads(mqtt_msg)
		# Print JSON Beautified
		contador_global_de_respuestas += 1
		respuesta_a_imprimir = "Respuesta : " + str(contador_global_de_respuestas) + " - " + mqtt_msg
		print(respuesta_a_imprimir)
		#print(json.dumps(json_msg, indent=4, sort_keys=True))
	except:
		print("\n\n\nError al convertir el mensaje recibido a JSON\n\n\n")
		return

#############################################
######### MQTT CLIENT CONFIGURATION #########
#############################################

mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.on_log = on_log
#mqtt_client.tls_set(MQTT_CERT_FILE_PATH)
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_SERVERURL, MQTT_SERVERPORT, keepalive=15)

if __name__ == "__main__":
	mqtt_client.loop_start()
	
	os.system('clear')

	menu="---------------------------------------------\n"
	menu += "Username: " + MQTT_USERNAME + "\n"
	menu += "Topic to send: " + MQTT_TOPIC_TO_SEND + "\n"
	menu += "Topic to receive: " + MQTT_TOPIC_TO_RECEIVE + "\n"
	menu += "---------------------------------------------\n"
	menu += "1. Agregar un usuario con fotografia (Toma unos 5 - 7 segundos en responder)\n"
	menu += "2. Agregar sin fotografía (Toma unos 2.4 segundos)\n"
	menu += "3. Aplicar nivel de acceso\n"
	menu += "4. Obtener información de la persona con su mnt_id_persona\n"
	menu += "5. Editar un usuario (para editar la fotografía utiliza la opción 6)\n"
	menu += "6. Editar un rostro (Toma unos 5 - 7 segundos en responder)\n"
	menu += "7. Eliminar un usuario\n"
	menu += "8. Obtener el mnt_id_persona a partir del persona_id\n"
	menu += "9. Agregar varios usuarios\n"
	menu += "s. Salir...\n"
	print(menu)

	while True:
		# Agregar soporte apra CTRL-C y en ese caso enviar a handler
		# para que pregunte si se quiere salir o no
		input_text = input("")

		if input_text == '1':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('agregar_usuario'), False)
		elif input_text == '2':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('agregar_usuario_sin_foto'), False)
		elif input_text == '3':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('actualizar_nivel_de_acceso'), False)
		elif input_text == '4':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('obtener_informacion_de_persona_por_id'), False)
		elif input_text == '5':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('editar_usuario'), False)
		elif input_text == '6':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('editar_rostro'), False)
		elif input_text == '7':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('eliminar_usuario'), False)
		elif input_text == '8':
			send_to_mqtts(MQTT_TOPIC_TO_SEND, get_json_example('obtener_mnt_id_persona'), False)
		elif input_text == '9':
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
			# Cerrar la sesión MQTT
			mqtt_client.loop_stop()
			exit(1)
		else:
			print("\n\n\nOpción no válida\n\n\n")
		
		os.system('clear')
		print(menu)
		print("La respuesta se imprimirá a continuación...")
import os
import json
import time
import base64
import random

from dotenv import load_dotenv
load_dotenv(override=True)

EXAMPLE_PHOTO_FOLDER_PATH = os.environ.get('PHOTO_FOLDER')

def get_json_info_from_photo(photo_path):
	with open(photo_path, "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

		# Export the encoded image to a file
		with open("encoded_image.txt", "w") as text_file:
			text_file.write(encoded_image)


		return encoded_image

############################################################
##########  JSON EXAMPLES FOR THE API REQUESTS   ###########
############################################################

obtener_version = \
{
	"module":"obtener_version",
	"body":""
}

obtener_informacion_de_organizaciones = \
{
  "module": "obtener_informacion_de_organizaciones",
  "body":{
	"num_pag": 1,
	"tam_pag": 100
  }
}

agregar_usuario = \
{
  "module": "agregar_usuario",
  "body": {
	"nombre": "John",
	"apellido": "Doe",
	"persona_id": "100",
	"org_num": "1",
	"add_fotografia": [
		  {
		"add_foto64": "face_information"
	  }
	],
	"tarjetas": [
	  {
		"tarjeta": "card_id"
	  }
	],
	"acceso_inicio": "2000-01-01T00:00:00-06:00",
	"acceso_final": "2037-12-31T11:59:59-06:00"
  }
}

agregar_usuario_sin_foto = \
{
  "module": "agregar_usuario_sin_foto",
  "body": {
	"nombre": "John Michael",
	"apellido": "Doe",
	"persona_id": "100",
	"org_num": "1",
	"tarjetas": [
	  {
		"tarjeta": "card_id"
	  }
	],
	"acceso_inicio": "2000-01-01T00:00:00-06:00",
	"acceso_final": "2037-12-31T11:59:59-06:00"
  }
}

actualizar_nivel_de_acceso = \
{
  "module": "actualizar_nivel_de_acceso",
  "body": {
	"mnt_id_persona": "23"
  }
}

obtener_informacion_de_persona_por_id = \
{
	"module": "obtener_informacion_de_persona_por_id",
	"body": {
		"mnt_id_persona": "110"
	}
}

editar_usuario = \
{
  "module": "editar_usuario",
  "body": {
	"mnt_id_persona": "110",
	"nombre": "Jonathan",
	"apellido": "Doe Doe",
	"foto": [
		  {
		"foto64": "face_information"
	  }
	],
	"tarjetas": [
	  {
		"tarjeta": "17005172533"
	  }
	],
	"acceso_inicio": "2000-04-26T15:00:00-06:00",
	"acceso_final": "2025-01-01T00:00:00-06:00"
  }
}

editar_rostro = \
{
	  "module": "editar_rostro",
	  "body": {
		"mnt_id_persona": "110",
		"add_foto64": "face_information"
	  }
}

eliminar_usuario = \
{
  "module": "eliminar_usuario",
  "body": {
		"mnt_id_persona": "100"
	}
}

def get_random_card_id():
	# Get epoch time in seconds and store in card_id variable
	epoch_time = int(time.time())
	card_id = str(epoch_time)
	return card_id

############################################################
########              RETURN FUNCTION             ##########
############################################################

def get_json_example(module):
	
	if module == "obtener_version":
		return json.dumps(obtener_version)
	
	elif module == "obtener_informacion_de_organizaciones":
		return json.dumps(obtener_informacion_de_organizaciones)
	
	elif module == "agregar_usuario":
		card_id = get_random_card_id()
		agregar_usuario['body']['persona_id'] = card_id

		# Select 1 of 4 photos to send
		photo_to_send = EXAMPLE_PHOTO_FOLDER_PATH + str(random.randint(2, 4)) + ".jpeg"
		agregar_usuario['body']['add_fotografia'][0]['add_foto64'] = get_json_info_from_photo(photo_to_send)

		# Convert the dictionary to json
		json_de_retorno = json.dumps(agregar_usuario).replace("card_id", card_id)
		return json_de_retorno
	
	elif module == "agregar_usuario_sin_foto":
		card_id = get_random_card_id()
		agregar_usuario_sin_foto['body']['persona_id'] = card_id

		# Convert the dictionary to json
		json_de_retorno = json.dumps(agregar_usuario_sin_foto).replace("card_id", card_id)
		return json_de_retorno
	
	elif module == "actualizar_nivel_de_acceso":
		# Input the personId
		id_de_la_persona = input("Ingrese el id MNT: ")
		
		# Change the personId value to the new personId
		actualizar_nivel_de_acceso['body']['mnt_id_persona'] = str(id_de_la_persona)
		
		# Convert the dictionary to json
		json_de_retorno = json.dumps(actualizar_nivel_de_acceso)
		return json_de_retorno
	
	elif module == "obtener_informacion_de_persona_por_id":
		# Input the personId
		id_de_la_persona = input("Ingrese el el id MNT: ")

		# Change the personId value to the new personId
		obtener_informacion_de_persona_por_id['body']['mnt_id_persona'] = str(id_de_la_persona)

		# Convert the dictionary to json
		json_de_retorno = json.dumps(obtener_informacion_de_persona_por_id)
		return json_de_retorno
	
	elif module == "editar_usuario":
		card_id = get_random_card_id()

		# Input the personId
		personId = input("Ingrese el id MNT: ")

		# Change the personId value to the new personId
		editar_usuario['body']['mnt_id_persona'] = personId
		
		# Change the cardNo value to the new card_id
		editar_usuario['body']['tarjetas'][0]['tarjeta'] = card_id
		
		# Convert the dictionary to json
		json_de_retorno = json.dumps(editar_usuario)
		return json_de_retorno
	
	elif module == "editar_rostro":

		# Input the personId
		personId = input("Ingrese el id MNT: ")
		
		# Change the personId value to the new personId
		editar_rostro['body']['mnt_id_persona'] = str(personId)
		
		# Edit user with photo #1
		photo_to_send = EXAMPLE_PHOTO_FOLDER_PATH + "1.jpeg"
		editar_rostro['body']['add_foto64'] = get_json_info_from_photo(photo_to_send)
		
		# Convert the dictionary to json
		json_de_retorno = json.dumps(editar_rostro)
		return json_de_retorno
	
	elif module == "eliminar_usuario":

		# Input the personId
		id_de_la_persona = input("Ingrese el id MNT: ")

		# Change the personId value to the new personId
		eliminar_usuario['body']['mnt_id_persona'] = str(id_de_la_persona)

		# Convert the dictionary to json
		json_de_retorno = json.dumps(eliminar_usuario)
		return json_de_retorno
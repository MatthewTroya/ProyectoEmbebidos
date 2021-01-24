import time
import serial
import requests

voltaje = int(input("Voltaje del dispositivo: "))
potencia = 0
url = 'https://eu80.chat-api.com/instance219005/message?token=7s12mtchi27flpy6'

try:
	ser = serial.Serial('/dev/ttyS3',9600,timeout = 3.0)
	while True:
		ser.flush()
		if (ser.in_waiting > 0):
			corriente = ser.readline().strip()
			print("Valor de dato recibido: "+corriente.decode()+" [I]")
			potencia += float(corriente.decode())*voltaje
			#Escritura de datos a Thingsboard
			#enviar = requests.get("https://api.thingspeak.com/update?api_key=XXXXXXXXXXXXXXXX&field1="+str(lista[0])+"&field2="+str(lista[1]))  #cuando se quiere enviar dos o mas datos
			enviar = requests.get("https://api.thingspeak.com/update?api_key=9D4GKP51608937YQ&field1="+str(potencia))
			if enviar.status_code == requests.codes.ok:
		    		if enviar.text != '0':
		        		print("Datos enviados correctamente")
		    		else:
		        		print("Tiempo de espera insuficiente (>15seg)")
			else:
		    		print("Error en el request: ",enviar.status_code)
		time.sleep(15)
		#Envio de datos x WhatsApp
		if float(potencia) > 200:
			data = ({"phone": "593983138196", "body": "Alerta, Consumo de energia de dispositivo alto"})
			res = requests.post(url, json=data)
			print (res.text)

except KeyboardInterrupt: #Cierra el serial cuando el usuario cierra forzosamente el proceso
	print ()
	ser.close()

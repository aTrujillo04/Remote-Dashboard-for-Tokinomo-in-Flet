import requests #Import requests library

RASP_IP = "http://192.168.1.169:5000" #Raspberry Pi IP address

def control_gadget(gadget, state): #Define function to control gadgets logic
    action = "on" if state == "on" else "off" #Determine action based on state
    try:
        Answer = requests.post( 
            f"{RASP_IP}/control", #Endpoint to control gadgets
            json={"gadget": gadget, "action": action}, #Send the request to server with gadget and action defined or pushed in button
            timeout=3
        )

        #Trying to decode JSON safely
        try:
            data = Answer.json() #Decode JSON response
        except ValueError: #Handle JSON decoding error
            print(f"⚠️ No JSON message received from Raspberry ({gadget}): {Answer.text}") #Log non-JSON response
            data = {"status": "error", "message": "Respuesta no válida del servidor"}

        print(f"✅ Sent: {gadget} -> {action} | Answer: {data}") #Log successful action with response data

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error while connecting to Raspberry ({gadget}): {e}") #Connection error message


def set_motor_pwm(value): #Define function to set motor PWM
    try:
        respuesta = requests.post( 
            f"{RASP_IP}/pwm", #Endpoint to set PWM
            json={"value": int(value)}, #Send the PWM value as int value in json format
            timeout=3
        )

        # Trying to decode JSON safely
        try:
            data = respuesta.json()
        except ValueError:
            print(f"⚠️ No JSON message received from Raspberry (PWM): {respuesta.text}") #Log non-JSON response
            data = {"status": "error", "message": "Respuesta no válida del servidor"}

        print(f"✅ PWM motor: {value}% | Answer: {data}") #Log successful PWM setting with response data

    except requests.exceptions.RequestException as ex:
        print(f"⚠️ Error while sending PWM: {ex}") #Connection error message

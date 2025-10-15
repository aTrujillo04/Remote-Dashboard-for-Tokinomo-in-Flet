import requests

RASP_IP = "http://192.168.1.169:5000"

def control_gadget(gadget, state):
    action = "on" if state == "on" else "off"
    try:
        Answer = requests.post(
            f"{RASP_IP}/control",
            json={"gadget": gadget, "action": action},
            timeout=3
        )

        #Trying to decode JSON safely
        try:
            data = Answer.json()
        except ValueError:
            print(f"⚠️ Respuesta no JSON desde Raspberry ({gadget}): {Answer.text}")
            data = {"status": "error", "message": "Respuesta no válida del servidor"}

        print(f"✅ Sent: {gadget} -> {action} | Answer: {data}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error while connecting to Raspberry ({gadget}): {e}")


def set_motor_pwm(value):
    try:
        respuesta = requests.post(
            f"{RASP_IP}/pwm",
            json={"value": int(value)},
            timeout=3
        )

        # Intentar decodificar JSON de forma segura
        try:
            data = respuesta.json()
        except ValueError:
            print(f"⚠️ Respuesta no JSON desde Raspberry (PWM): {respuesta.text}")
            data = {"status": "error", "message": "Respuesta no válida del servidor"}

        print(f"✅ PWM motor: {value}% | Answer: {data}")

    except requests.exceptions.RequestException as ex:
        print(f"⚠️ Error while sending PWM: {ex}")

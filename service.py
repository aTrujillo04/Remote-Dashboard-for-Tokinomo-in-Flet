import requests

import requests

RASP_IP = "http://192.168.1.169:5000"

def controlar_dispositivo_gpio(dispositivo, estado):
    accion = "on" if estado == "encender" else "off"
    try:
        respuesta = requests.post(
            f"{RASP_IP}/control",
            json={"dispositivo": dispositivo, "accion": accion},
            timeout=3
        )
        data = respuesta.json()
        print(f"✅ Enviado: {dispositivo} -> {accion} | Respuesta: {data}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al conectar con Raspberry ({dispositivo}): {e}")

def set_motor_pwm(valor):
    try:
        respuesta = requests.post(
            f"{RASP_IP}/pwm",
            json={"valor": int(valor)},
            timeout=3
        )
        data = respuesta.json()
        print(f"✅ PWM motor: {valor}% | Respuesta: {data}")
    except requests.exceptions.RequestException as ex:
        print(f"⚠️ Error al enviar PWM: {ex}")
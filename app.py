import flet as ft
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

def main(page: ft.Page):
    page.title = "Panel de Control Octynomo"
    page.window_height = 800
    page.window_width = 1200
    page.scroll = ft.ScrollMode.ALWAYS

    fondo_diseño = ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#0288d1", "#81d4fa", "#b3e5fc"]
                ),
                expand=True,
            ),
            *[
                ft.Container(
                    bgcolor="rgba(255,255,255,0.15)",
                    width=2000,
                    height=2,
                    rotate=ft.Rotate(angle=0.7),
                    top=i * 100,
                    left=-500,
                )
                for i in range(10)
            ],
        ],
        expand=True,
    )

    estado_dispositivos = {"luz": False, "sonido": False, "rutina": False, "motor": False}
    mapeo_data = {"Luz": "luz", "Sonido": "sonido", "Rutina": "rutina", "Motor": "motor"}

    # Login
    txt_usuario = ft.TextField(
        hint_text="Usuario", border_radius=12, bgcolor="white",
        height=55, content_padding=15, text_align=ft.TextAlign.LEFT
    )
    txt_password = ft.TextField(
        hint_text="Contraseña", password=True, can_reveal_password=True,
        border_radius=12, bgcolor="white", height=55, content_padding=15, text_align=ft.TextAlign.LEFT
    )
    txt_error = ft.Text("⚠️ Usuario o contraseña incorrectos", color="red500", visible=False)

    def login_click(e):
        if txt_usuario.value == "adm" and txt_password.value == "1":
            page.go("/panel")
        else:
            txt_error.visible = True
            page.update()

    login_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Text(
                    "Inicio de sesión",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="blueGrey900",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=15, color="transparent"),

                ft.Image(
                    src="https://images.icon-icons.com/3446/PNG/512/account_profile_user_avatar_icon_219236.png", 
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                ),

                ft.Divider(height=25, color="transparent"),
                txt_usuario,
                txt_password,
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Text("Entrar", size=20, weight=ft.FontWeight.BOLD),
                    on_click=login_click,
                    bgcolor="blue700",
                    color="white",
                    height=50
                ),
                txt_error,
                ft.Container(expand=True),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        height=600,
        padding=35,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="black26"),
        alignment=ft.alignment.center,
    )

    login_view = ft.View(
        "/",
        [
            ft.Stack(
                controls=[
                    fondo_diseño,
                    ft.Container(content=login_form, alignment=ft.alignment.center, expand=True),
                    ft.Container(
                        content=ft.Image(
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png",
                            fit=ft.ImageFit.CONTAIN, opacity=0.7
                        ),
                        width=160, height=100, alignment=ft.alignment.bottom_right, right=10, bottom=10
                    )
                ],
                expand=True,
            )
        ]
    )

    # Panel
    def toggle_dispositivo(e):
        btn = e.control
        nombre_display = btn.data
        dispositivo_key = mapeo_data.get(nombre_display)
        if not dispositivo_key:
            return

        estado_dispositivos[dispositivo_key] = not estado_dispositivos[dispositivo_key]
        encendido = estado_dispositivos[dispositivo_key]
        btn.bgcolor = "green700" if encendido else "red700"
        btn.text = f"{nombre_display}: {'Encendido' if encendido else 'Apagado'}"
        page.update()
        controlar_dispositivo_gpio(dispositivo_key, "encender" if encendido else "apagar")

    def slider_cambio(e):
        valor = int(e.control.value)
        velocidad_value.value = f"Velocidad: {valor}%"
        page.update()
        set_motor_pwm(valor)

    # Boton deslizador
    velocidad_value = ft.Text("Velocidad: 0%", size=16, color="white")
    velocidad_slider = ft.Slider(
        min=0, max=100, divisions=100, value=0,
        on_change=slider_cambio,
        active_color="blue700", thumb_color="blue900", expand=True
    )
    slider_container = ft.Container(
        content=ft.Column(
            [velocidad_slider, velocidad_value],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=25,
        border_radius=15,
        bgcolor="rgba(255,255,255,0.15)",
        expand=True
    )

    # Botones
    botones_row = ft.ResponsiveRow(
        spacing=25,
        controls=[
            ft.Container(
                content=ft.ElevatedButton(
                    text=f"{dispositivo}: Apagado", data=dispositivo,
                    on_click=toggle_dispositivo,
                    bgcolor="red700", color="white",
                    height=90, expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                col={"xs":12, "sm":6, "md":3},
                expand=True,
            ) for dispositivo in ["Luz", "Sonido", "Motor", "Rutina"]
        ]
    )

    # Contenido del panel
    panel_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Control de Octynomo", size=34, weight="bold", color="white"),
                ft.Text("Control de funciones", size=22, color="white70"),
                botones_row,
                ft.Divider(height=40, color="transparent"),
                slider_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        ),
        padding=ft.padding.only(left=40, right=40, top=30, bottom=80),
        border_radius=20,
        bgcolor="rgba(255,255,255,0.1)",
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="black26"),
        expand=True
    )

    panel_view = ft.View(
        "/panel",
        [
            ft.Stack(
                controls=[
                    fondo_diseño,
                    ft.Container(content=panel_content, expand=True, alignment=ft.alignment.center),
                    ft.Container(
                        content=ft.Image(
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png",
                            fit=ft.ImageFit.CONTAIN, opacity=0.7
                        ),
                        width=130, height=100,
                        alignment=ft.alignment.bottom_right, right=10, bottom=10
                    )
                ],
                expand=True
            )
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(login_view)
        if page.route == "/panel":
            page.views.append(panel_view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)

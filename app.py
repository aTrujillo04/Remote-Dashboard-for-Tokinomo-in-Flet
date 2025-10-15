import flet as ft
import requests
from service import control_gadget, set_motor_pwm 

def main(page: ft.Page):
    page.title = "Octynomo Dashboard"
    page.window_height = 800
    page.window_width = 1200
    page.scroll = ft.ScrollMode.ALWAYS

    background_design = ft.Stack(
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

    gadget_states = {"ilumination": False, "sound": False, "routine": False, "motor": False}
    data_mapping = {"Ilumination": "ilumination", "Sound": "sound", "Routine": "routine", "Motor": "motor"}

    # Login
    txt_user = ft.TextField(
        hint_text="User", border_radius=12, bgcolor="white",
        height=55, content_padding=15, text_align=ft.TextAlign.LEFT
    )
    txt_password = ft.TextField(
        hint_text="Password", password=True, can_reveal_password=True,
        border_radius=12, bgcolor="white", height=55, content_padding=15, text_align=ft.TextAlign.LEFT
    )
    txt_error = ft.Text("⚠️ Incorrect user or password", color="red500", visible=False)

    def login_click(e):
        if txt_user.value == "adm" and txt_password.value == "1":
            page.go("/panel")
        else:
            txt_error.visible = True
            page.update()

    login_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Text(
                    "Login",
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
                txt_user,
                txt_password,
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Text("Enter", size=20, weight=ft.FontWeight.BOLD),
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
                    background_design,
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
    def gadget_toggle(e):
        btn = e.control
        display_name = btn.data
        gadget_key = data_mapping.get(display_name)
        if not gadget_key:
            return

        gadget_states[gadget_key] = not gadget_states[gadget_key]
        started = gadget_states[gadget_key]
        btn.bgcolor = "green700" if started else "red700"
        btn.text = f"{display_name}: {'On' if started else 'Off'}"
        page.update()
        control_gadget(gadget_key, "on" if started else "off")

    def change_slide(e):
        value = int(e.control.value)
        speed_value.value = f"Speed: {value}%"
        page.update()
        set_motor_pwm(value)

    # Boton deslizador
    speed_value = ft.Text("Speed: 0%", size=16, color="white")
    velocidad_slider = ft.Slider(
        min=0, max=100, divisions=100, value=0,
        on_change=change_slide,
        active_color="blue700", thumb_color="blue900", expand=True
    )
    slider_container = ft.Container(
        content=ft.Column(
            [velocidad_slider, speed_value],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=25,
        border_radius=15,
        bgcolor="rgba(255,255,255,0.15)",
        expand=True
    )

    # Botones
    buttons_row = ft.ResponsiveRow(
        spacing=25,
        controls=[
            ft.Container(
                content=ft.ElevatedButton(
                    text=f"{gadget}: Off", data=gadget,
                    on_click=gadget_toggle,
                    bgcolor="red700", color="white",
                    height=90, expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                col={"xs":12, "sm":6, "md":3},
                expand=True,
            ) for gadget in ["Ilumination", "Sound", "Motor", "Routine"]
        ]
    )

    # Contenido del panel
    panel_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Octynomo controls", size=34, weight="bold", color="white"),
                ft.Text("Features", size=22, color="white70"),
                buttons_row,
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
                    background_design,
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

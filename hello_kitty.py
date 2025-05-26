import flet as ft
import json
import pygetwindow as gw
from PIL import ImageGrab

# Roupas da Hello Kitty
roupas = {
    "camisa": [
        "assets/HelloKitty/camisa1.png",
        "assets/HelloKitty/camisa2.png",
        "assets/HelloKitty/camisa3.png"
    ],
    "acessorio": [
        "assets/HelloKitty/acessorio1.png",
        "assets/HelloKitty/acessorio2.png",
        "assets/HelloKitty/acessorio3.png"
    ],
    "lacinho": [
        "assets/HelloKitty/lacinho1.png",
        "assets/HelloKitty/lacinho2.png",
        "assets/HelloKitty/lacinho3.png"
    ]
}

# Estado inicial das roupas
estado = {"camisa": None, "acessorio": None, "lacinho": None}


def criar_personagem_hello_kitty(page: ft.Page):
    kitty_component_width = 200
    kitty_component_height = 200

    base_img = ft.Image(
        src="assets/base.png", width=kitty_component_width, height=kitty_component_height
    )
    camisa_img = ft.Image(width=kitty_component_width, height=kitty_component_height, visible=False)
    acessorio_img = ft.Image(width=kitty_component_width, height=kitty_component_height, visible=False)
    lacinho_img = ft.Image(width=kitty_component_width, height=kitty_component_height, visible=False)

    def atualizar_roupas_display():
        camisa_img.visible = estado["camisa"] is not None
        if camisa_img.visible:
            camisa_img.src = roupas["camisa"][estado["camisa"]]

        acessorio_img.visible = estado["acessorio"] is not None
        if acessorio_img.visible:
            acessorio_img.src = roupas["acessorio"][estado["acessorio"]]

        lacinho_img.visible = estado["lacinho"] is not None
        if lacinho_img.visible:
            lacinho_img.src = roupas["lacinho"][estado["lacinho"]]

    def trocar_roupa_action(e, tipo_roupa):
        if estado[tipo_roupa] is None:
            estado[tipo_roupa] = 0
        else:
            estado[tipo_roupa] = (estado[tipo_roupa] + 1) % len(roupas[tipo_roupa])
        atualizar_roupas_display()
        page.update()

    def salvar_look_action(e):
        try:
            with open("look_salvo.txt", "w") as f:
                json.dump(estado, f)

            window = gw.getWindowsWithTitle("Dress Up Hello Kitty")[0]
            left, top, width, height = window.left, window.top, window.width, window.height
            bbox = (left, top, left + width, top + height)

            screenshot = ImageGrab.grab(bbox=bbox)
            screenshot.save("look_print.png")

            page.snack_bar = ft.SnackBar(ft.Text("Look salvo com sucesso!"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex_msg:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar look: {ex_msg}"))
            page.snack_bar.open = True
            page.update()

    botoes_roupas_row = ft.Row(
        [
            ft.ElevatedButton(
                "Camisa",
                on_click=lambda e: trocar_roupa_action(e, "camisa"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Acessório",
                on_click=lambda e: trocar_roupa_action(e, "acessorio"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Chapéu",
                on_click=lambda e: trocar_roupa_action(e, "lacinho"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    botao_salvar_look = ft.ElevatedButton(
        "Salvar Look",
        on_click=salvar_look_action,
        style=ft.ButtonStyle(
            bgcolor="#a4aee8", color="white",
            text_style=ft.TextStyle(font_family="pixel", size=12)
        )
    )

    hello_kitty_visual_stack = ft.Stack(
        [base_img, camisa_img, acessorio_img, lacinho_img],
        width=kitty_component_width,
        height=kitty_component_height
    )

    conteudo_imagem_coluna = ft.Column(
        [
            hello_kitty_visual_stack,
            botoes_roupas_row,
            botao_salvar_look
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    root_stack = ft.Stack(
    [
        # Boneca + botões fixos
        ft.Container(
            content=conteudo_imagem_coluna,
            left=0,
            top=0
        )
    ],
    width=1024,
    height=768
)
    
    atualizar_roupas_display()
    return root_stack
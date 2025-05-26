import flet as ft
import json
import pygetwindow as gw
from PIL import ImageGrab

roupas = {
    "camisaKUROMI": [
        "assets/Kuromi/camisaKUROMI1.png",
        "assets/Kuromi/camisaKUROMI2.png",
        "assets/Kuromi/camisaKUROMI3.png"
    ],
    "acessorioKUROMI": [
        "assets/Kuromi/acessorioKUROMI1.png",
        "assets/Kuromi/acessorioKUROMI2.png",
        "assets/Kuromi/acessorioKUROMI3.png"
    ],
    "chapeuKUROMI": [
        "assets/Kuromi/chapeuKUROMI1.png",
        "assets/Kuromi/chapeuKUROMI2.png",
        "assets/Kuromi/chapeuKUROMI3.png"
    ]
}

estado_kuromi = {"camisaKUROMI": None, "acessorioKUROMI": None, "chapeuKUROMI": None}

def criar_personagem_kuromi(page: ft.Page):
    kuromi_component_width = 200
    kuromi_component_height = 200

    baseKUROMI_img = ft.Image(
        src="assets/baseKUROMI.png", width=kuromi_component_width, height=kuromi_component_height
    )
    camisaKUROMI_img = ft.Image(width=kuromi_component_width, height=kuromi_component_height, visible=False)
    acessorioKUROMI_img = ft.Image(width=kuromi_component_width, height=kuromi_component_height, visible=False)
    chapeuKUROMI_img = ft.Image(width=kuromi_component_width, height=kuromi_component_height, visible=False)

    def atualizar_roupas_display():
        camisaKUROMI_img.visible = estado_kuromi["camisaKUROMI"] is not None
        if camisaKUROMI_img.visible:
            camisaKUROMI_img.src = roupas["camisaKUROMI"][estado_kuromi["camisaKUROMI"]]

        acessorioKUROMI_img.visible = estado_kuromi["acessorioKUROMI"] is not None
        if acessorioKUROMI_img.visible:
            acessorioKUROMI_img.src = roupas["acessorioKUROMI"][estado_kuromi["acessorioKUROMI"]]

        chapeuKUROMI_img.visible = estado_kuromi["chapeuKUROMI"] is not None
        if chapeuKUROMI_img.visible:
            chapeuKUROMI_img.src = roupas["chapeuKUROMI"][estado_kuromi["chapeuKUROMI"]]
    
    def trocar_roupa_action(e, tipo_roupa):
        if estado_kuromi[tipo_roupa] is None:
            estado_kuromi[tipo_roupa] = 0
        else:
            estado_kuromi[tipo_roupa] = (estado_kuromi[tipo_roupa] + 1) % len(roupas[tipo_roupa])
        atualizar_roupas_display()
        page.update()
    
    def salvar_look_action(e):
        try:
            with open("look_salvo.txt", "w") as f:
                json.dump(estado_kuromi, f)

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
                on_click=lambda e: trocar_roupa_action(e, "camisaKUROMI"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Acessório",
                on_click=lambda e: trocar_roupa_action(e, "acessorioKUROMI"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Chapéu",
                on_click=lambda e: trocar_roupa_action(e, "chapeuKUROMI"),
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

    kuromi_visual_stack = ft.Stack(
        [baseKUROMI_img, camisaKUROMI_img, acessorioKUROMI_img, chapeuKUROMI_img],
        width=kuromi_component_width,
        height=kuromi_component_height
    )

    conteudo_imagem_coluna = ft.Column(
        [
            kuromi_visual_stack,
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
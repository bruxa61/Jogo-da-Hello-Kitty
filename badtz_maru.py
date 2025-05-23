import flet as ft
import json
import pygetwindow as gw
from PIL import ImageGrab

roupas = {
    "camisaMARU": [
        "assets/BadtzMaru/camisaMARU1.png",
        "assets/BadtzMaru/camisaMARU2.png",
        "assets/BadtzMaru/camisaMARU3.png"
    ],
    "acessorioMARU": [
        "assets/BadtzMaru/acessorioMARU1.png",
        "assets/BadtzMaru/acessorioMARU2.png",
        "assets/BadtzMaru/acessorioMARU3.png"
    ],
    "chapeuMARU": [
        "assets/BadtzMaru/chapeuMARU1.png",
        "assets/BadtzMaru/chapeuMARU2.png",
        "assets/BadtzMaru/chapeuMARU3.png"
    ]
}

estado_maru = {"camisaMARU": None, "acessorioMARU": None, "chapeuMARU": None}

def criar_personagem_badtz_maru(page: ft.Page):
    maru_component_width = 200
    maru_component_height = 200

    baseMARU_img = ft.Image(
        src="assets/baseMARU.png", width=maru_component_width, height=maru_component_height
    )
    camisaMARU_img = ft.Image(width=maru_component_width, height=maru_component_height, visible=False)
    acessorioMARU_img = ft.Image(width=maru_component_width, height=maru_component_height, visible=False)
    chapeuMARU_img = ft.Image(width=maru_component_width, height=maru_component_height, visible=False)

    def atualizar_roupas_display():
        camisaMARU_img.visible = estado_maru["camisaMARU"] is not None
        if camisaMARU_img.visible:
            camisaMARU_img.src = roupas["camisaMARU"][estado_maru["camisaMARU"]]

        acessorioMARU_img.visible = estado_maru["acessorioMARU"] is not None
        if acessorioMARU_img.visible:
            acessorioMARU_img.src = roupas["acessorioMARU"][estado_maru["acessorioMARU"]]

        chapeuMARU_img.visible = estado_maru["chapeuMARU"] is not None
        if chapeuMARU_img.visible:
            chapeuMARU_img.src = roupas["chapeuMARU"][estado_maru["chapeuMARU"]]
    
    def trocar_roupa_action(e, tipo_roupa):
        if estado_maru[tipo_roupa] is None:
            estado_maru[tipo_roupa] = 0
        else:
            estado_maru[tipo_roupa] = (estado_maru[tipo_roupa] + 1) % len(roupas[tipo_roupa])
        atualizar_roupas_display()
        page.update()
    
    def salvar_look_action(e):
        try:
            with open("look_salvo.txt", "w") as f:
                json.dump(estado_maru, f)

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
                on_click=lambda e: trocar_roupa_action(e, "camisaMARU"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Acessório",
                on_click=lambda e: trocar_roupa_action(e, "acessorioMARU"),
                style=ft.ButtonStyle(
                    bgcolor="#f48fb1", color="white",
                    text_style=ft.TextStyle(font_family="pixel", size=12)
                )
            ),
            ft.ElevatedButton(
                "Chapéu",
                on_click=lambda e: trocar_roupa_action(e, "chapeuMARU"),
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

    badtz_maru_visual_stack = ft.Stack(
        [baseMARU_img, camisaMARU_img, acessorioMARU_img, chapeuMARU_img],
        width=maru_component_width,
        height=maru_component_height
    )

    conteudo_imagem_coluna = ft.Column(
        [
            badtz_maru_visual_stack,
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
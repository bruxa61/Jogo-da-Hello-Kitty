import flet as ft
from hello_kitty import criar_personagem_hello_kitty
from badtz_maru import criar_personagem_badtz_maru

estado = {"camisa": None, "acessorio": None, "lacinho": None}
estado_maru = {"camisaMARU": None, "acessorioMARU": None, "chapeuMARU": None}

cores_paleta = [
    "#fed1dd", "#fdcee6", "#f4ccea", "#eac2e6", "#eeb4e8", 
    "#e8bad9", "#e4b7d7", "#dab5d8", "#d6b3df", "#c5afd8",
    "#c0afd1", "#aaacd1", "#afa9de", "#a2a7dc",
    "#fcd2d8", "#ffd4e6", "#fedcd4", "#fee1e7", "#fed3da", 
    "#ffc8da", "#ffc3da", "#f6bfe4", "#e5bee9", "#d9bee9", 
    "#c8c4f6", "#babcf3", "#a1a9e6", "#9da5dc"
]

def main(page: ft.Page):
    page.title = "Dress Up Hello Kitty"
    page.padding = 35
    page.bgcolor = "#fce4ec"
    page.fonts = {"pixel": "assets/PressStart2P-Regular.ttf"}

    hello_kitty = criar_personagem_hello_kitty(page)
    maru = criar_personagem_badtz_maru(page)

    personagem_hello = True  # Começa com Hello Kitty
    personagem_atual = ft.Column([hello_kitty])

    def mudar_cor_fundo(e, cor):
        page.bgcolor = cor
        page.update()

    def criar_cor_container(cor):
        return ft.Container(
            width=24,
            height=24,
            bgcolor=cor,
            on_click=lambda e, cor=cor: mudar_cor_fundo(e, cor),
            tooltip=cor,
            margin=ft.margin.all(0)
        )

    def trocar_personagem(e):
        nonlocal personagem_hello
        personagem_atual.controls.clear()

        if personagem_hello:
            personagem_atual.controls.append(maru)
        else:
            personagem_atual.controls.append(hello_kitty)

        personagem_hello = not personagem_hello
        page.update()

    botao_trocar = ft.ElevatedButton(
        text="Trocar Personagem",
        on_click=trocar_personagem,
        style=ft.ButtonStyle(
            bgcolor="#f48fb1",
            color="white",
            text_style=ft.TextStyle(font_family="pixel", size=12)
        )
    )

    coluna1_cores = cores_paleta[::2]
    coluna2_cores = cores_paleta[1::2]

    paleta_row = ft.Row(
        controls=[
            ft.Column(
                controls=[criar_cor_container(cor) for cor in coluna1_cores],
                spacing=5.7
            ),
            ft.Column(
                controls=[criar_cor_container(cor) for cor in coluna2_cores],
                spacing=5.7
            )
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER
    )

    root_stack = ft.Stack(
        [
            # Fundo fixo
            ft.Container(
                content=ft.Image(
                    src="assets/background.jpg",
                    width=1024,
                    height=768,
                    fit=ft.ImageFit.NONE
                ),
                left=70,
                top=-80
            ),

            # Paleta de cores fixa
            ft.Container(
                content=paleta_row,
                left=163.2,
                top=135.5,
                width=200,
            ),

            # Personagem atual (Hello Kitty ou Maru)
            ft.Container(
                content=personagem_atual,
                left=430,
                top=170
            ),

            # Botão para trocar personagem
            ft.Container(
                content=botao_trocar,
                left=430,
                top=520
            )
        ],
        width=1024,
        height=768
    )

    page.add(root_stack)
    page.update()

ft.app(target=main, assets_dir="assets")
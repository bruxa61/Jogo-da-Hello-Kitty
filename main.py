import flet as ft
from hello_kitty import criar_personagem_hello_kitty
from badtz_maru import criar_personagem_badtz_maru
from kuromi import criar_personagem_kuromi

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
    kuromi = criar_personagem_kuromi(page)

    indice_personagem = 0  # Começa com Hello Kitty
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
        nonlocal indice_personagem
        personagem_atual.controls.clear()

        if indice_personagem == 0:
            personagem_atual.controls.append(maru)
        elif indice_personagem == 1:
            personagem_atual.controls.append(kuromi)
        else:
            personagem_atual.controls.append(hello_kitty)

        indice_personagem = (indice_personagem + 1) % 3  # Cicla entre 0, 1 e 2
        page.update()

    # Setas com imagem
    seta_esquerda = ft.Container(
        content=ft.Image(src="assets/seta_esquerda.png", width=100, height=100),
        on_click=trocar_personagem,
        tooltip="Anterior"
    )

    seta_direita = ft.Container(
        content=ft.Image(src="assets/seta_direita.png", width=100, height=100),
        on_click=trocar_personagem,
        tooltip="Próximo"
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
            # Fundo
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

            # Paleta de cores
            ft.Container(
                content=paleta_row,
                left=163.2,
                top=135.5,
                width=200,
            ),

            # Seta esquerda
            ft.Container(
                content=seta_esquerda,
                left=370,
                top=250
            ),

            # Personagem
            ft.Container(
                content=personagem_atual,
                left=430,
                top=170
            ),

            # Seta direita
            ft.Container(
                content=seta_direita,
                left=730,
                top=250
            ),
        ],
        width=1024,
        height=768
    )

    page.add(root_stack)
    page.update()

ft.app(target=main, assets_dir="assets")

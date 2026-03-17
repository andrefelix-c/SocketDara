import flet as ft
from functions.socket_func import abandonar_partida

def iniciar_variaveis(page: ft.Page, servidor: int):
    if page.session.store.get("thread_iniciada") is None:
        page.session.store.set("thread_iniciada", False)

    # if page.session.store.get("conn_holder") is None:
    #     page.session.store.set("conn_holder", False)

    if page.session.store.get("meu_turno") is None:
        page.session.store.set("meu_turno", [True] if str(servidor)=="0" else [False])

    if page.session.store.get("tabuleiro_logico") is None:
        page.session.store.set("tabuleiro_logico", [0] * 30)

    # if page.session.store.get("pecas_colocadas") is None:
    #     page.session.store.set("pecas_colocadas", [0])

    if page.session.store.get("pecas_colocadas") is None:
        page.session.store.set("pecas_colocadas", [0, 0])

    if page.session.store.get("fase") is None:
        page.session.store.set("fase", 1)

    if page.session.store.get("comer_peça") is None:
        page.session.store.set("comer_peça", False)
    
    if page.session.store.get("idx_antigo") is None:
        page.session.store.set("idx_antigo", -1)

    if page.session.store.get("idx_aux") is None:
        page.session.store.set("idx_aux", -1)

def abrir_confirmacao_desistencia(e, page: ft.Page, on_click):

    # confirm_dialog = ft.AlertDialog(
    #     modal=True,
    #     title=ft.Text("Confirmar desistência"),
    #     content=ft.Text("Você tem certeza que deseja sair? O jogo será encerrado."),
    #     actions=[
    #         ft.TextButton("Sim", on_click= lambda e: abandonar_partida(e, page, on_click)),
    #         ft.TextButton("Não", on_click=lambda _: page.pop_dialog()),
    #     ],
    #     actions_alignment=ft.MainAxisAlignment.END,
    # )

    confirm_dialog = ft.AlertDialog(
        modal=True,
        content_padding=0,
        content=ft.Container(
            content=ft.Column(
                [
                    # ft.Text("Confirmar desistência", size=24),
                    ft.Text("Você tem certeza que deseja desistir?", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.TextButton("Confirmar", on_click= lambda e: abandonar_partida(e, page, on_click)),
                            ft.TextButton(content=ft.Text("Voltar para a partida", color="#00FF00"), on_click=lambda _: page.pop_dialog()),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
            border=ft.border.all(1, "#333333"), # Espessura e Cor
            border_radius=15,
            bgcolor="#1E1E1E", # Cor de fundo interna
            width=300,
        )
    )

    page.show_dialog(confirm_dialog)
    page.update()
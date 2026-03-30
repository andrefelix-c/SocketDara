import flet as ft
import socket
import threading
import time

from functions.socket_func import conectar_em_background, wait_for_client
from functions.game_logic_func import on_cell_click, send_chat
from functions.utils_func import iniciar_variaveis, abrir_confirmacao_desistencia

def auto_update(page: ft.Page):
    while True:
        time.sleep(0.1)
        try:
            page.update()
        except:
            break

def game_view(page: ft.Page, on_click):

    servidor = page.session.store.get("sou_servidor")
    iniciar_variaveis(page, servidor)

    status_text = ft.Text(value="Aguardando Oponente...", color="amber", weight="bold")
    botao_desistir = ft.Button(
        content=ft.Text("Abandonar a partida", color=ft.Colors.RED), 
        on_click=lambda e: abrir_confirmacao_desistencia(e, page, on_click)
        )
    board = ft.GridView(runs_count=6, width=300, height=260, spacing=5)
    for i in range(30):
        board.controls.append(ft.Container(bgcolor="white10", on_click=lambda e: on_cell_click(e, page), data=i, border_radius=5))
    chat_messages = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    chat_input = ft.TextField(label="Mensagem", expand=True, on_submit=lambda e: send_chat(e, page))

    page.session.store.set("status_text", status_text)
    page.session.store.set("board", board)
    page.session.store.set("chat_messages", chat_messages)
    page.session.store.set("chat_input", chat_input)

    
    threading.Thread(
        target=conectar_em_background, 
        args=(page, on_click), 
        daemon=True).start()
    
    threading.Thread(target=auto_update, args=(page,), daemon=True).start()
        
    
    return ft.View(
        route="/game",
        controls=[
            ft.Container(
                content=ft.Row(
                    [ft.Text("🕹️ Dara", size=20, weight="bold"), botao_desistir],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10 # Adiciona um respiro nas bordas
            ),
            # ft.Text("🕹️ Dara", size=20, weight="bold"),
            status_text,
            ft.Container(board, alignment=ft.Alignment.CENTER),
            ft.Divider(),
            ft.Container(chat_messages, expand=True, bgcolor=ft.Colors.BLACK12, padding=10, border_radius=10, width=float('inf')),
            ft.Row([chat_input, ft.IconButton(ft.Icons.SEND, on_click=lambda e: send_chat(e, page))]),
        ],
    )
    
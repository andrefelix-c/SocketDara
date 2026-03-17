import flet as ft
import socket
import threading

# FUNÇÕES PRINCIPAIS

def send_chat(e, page: ft.Page):

    chat_input = page.session.store.get("chat_input")
    chat_messages = page.session.store.get("chat_messages")
    socket_ativo = page.session.store.get("socket_ativo")

    if chat_input.value and socket_ativo:
        try:
            socket_ativo.sendall(f"MSG:{chat_input.value}\n".encode('utf-8'))
        except Exception as er:
            print(f"Erro no envio da mensagem: {er}")
        chat_messages.controls.append(ft.Text(f"Você: {chat_input.value}", color=ft.Colors.BLUE_200))
        chat_input.value = ""
        page.update()

def on_cell_click(e, page: ft.Page):

    socket_ativo = page.session.store.get("socket_ativo")
    servidor = page.session.store.get("sou_servidor")

    meu_turno = page.session.store.get("meu_turno")
    fase = page.session.store.get("fase")
    idx_antigo = page.session.store.get("idx_antigo")

    tabuleiro_logico = page.session.store.get("tabuleiro_logico")
    pecas_colocadas = page.session.store.get("pecas_colocadas")
    status_text = page.session.store.get("status_text")
    board = page.session.store.get("board")

    idx = e.control.data

    if not meu_turno[0] or (tabuleiro_logico[idx] != 0 and fase == 1) or not socket_ativo:
        return

    if (pecas_colocadas[0] + pecas_colocadas[1]) < 24 and valida_formacao_linha(idx, page) and fase==1:
        page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! É proibido formar linha de 3 nessa etapa!")))
        page.update()
        return
    
    if fase == 1:
        e.control.content = ft.CircleAvatar(bgcolor= ft.Colors.BLUE if str(servidor) == "0" else ft.Colors.RED, radius=15)
        tabuleiro_logico[idx] = 1 if str(servidor) == "0" else 2
        pecas_colocadas[0] += 1
        socket_ativo.sendall(f"ADD:{idx}\n".encode('utf-8'))
        if (pecas_colocadas[0] + pecas_colocadas[1]) == 24:
            page.session.store.set("fase", 2)
        meu_turno[0] = False 
        status_text.value = "Vez do Oponente..."
        status_text.color = ft.Colors.RED_400
        page.update()
    
    if fase == 2:

        if idx_antigo == -1:
            if not tabuleiro_logico[idx] != 0:
                page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! Escolha uma peça!!!!")))
                page.update()
                return
            if not minha_peça(idx, page):
                page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! Escolha uma peça sua!!!!")))
                page.update()
                return
            page.session.store.set("idx_antigo", idx)
            e.control.content = ft.CircleAvatar(bgcolor= ft.Colors.YELLOW, radius=15)

        elif idx_antigo == idx and not page.session.store.get("comer_peça"):
            page.session.store.set("idx_antigo", -1)
            e.control.content = ft.CircleAvatar(bgcolor= ft.Colors.BLUE if str(servidor) == "0" else ft.Colors.RED, radius=15)
        
        else:
            if page.session.store.get("comer_peça"):
                idx_aux = page.session.store.get("idx_aux")
                if minha_peça(idx, page):
                    page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! Escolha uma peça do adverário!!!!")))
                    page.update()
                    return
                comer_peça(idx, page)
                page.session.store.set("idx_antigo", -1)
                page.session.store.set("idx_aux", -1)
                page.session.store.set("comer_peça", False)
                socket_ativo.sendall(f"MOVEAT:{idx_antigo}-{idx_aux}-{idx}\n".encode('utf-8'))

            else:
                if tabuleiro_logico[idx] != 0:
                    page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! Escolha uma espaço vazio!!!!")))
                    page.update()
                    return
                
                if not verifica_adjacencia(idx_antigo, idx):
                    page.show_dialog(ft.SnackBar(ft.Text("⚠️ Eii!! Escolha uma espaço adjascente!!!!")))
                    page.update()
                    return
                
                tabuleiro_logico[idx_antigo] = 0 
                tabuleiro_logico[idx] = 1 if str(servidor) == "0" else 2

                board.controls[idx_antigo].content = None
                e.control.content = ft.CircleAvatar(bgcolor= ft.Colors.BLUE if str(servidor) == "0" else ft.Colors.RED, radius=15)

                if valida_formacao_linha(idx, page):
                    page.session.store.set("comer_peça", True)
                    page.session.store.set("idx_aux", idx)
                    page.show_dialog(ft.SnackBar(ft.Text("🍴 HORA DE COMER!!! Escolha uma peça do seu adversário.")))
                    page.update()
                    return

                socket_ativo.sendall(f"MOVE:{idx_antigo}-{idx}\n".encode('utf-8'))
                page.session.store.set("idx_antigo", -1)

            if pecas_colocadas[1] <= 2:
                meu_turno[0] = False
                status_text.value = "Fim de jogo. Você ganhou!!"
                status_text.color = ft.Colors.GREEN_400
            else:
                meu_turno[0] = False
                status_text.value = "Vez do Oponente..."
                status_text.color = ft.Colors.RED_400
                page.update()

# FUNÇÕES AUXILIARES

def valida_formacao_linha(idx, page: ft.Page):

    servidor = page.session.store.get("sou_servidor")
    tabuleiro_logico = page.session.store.get("tabuleiro_logico")

    cor = 1 if str(servidor) == "0" else 2

    x, y = idx % 6, idx // 6
    direcoes = [(1, 0), (0, 1)] # VERIFICAR SE CONSIDERA DIAGONAL (1, 1), (1, -1)

    for dx, dy in direcoes:
        contagem = 1
        for sentido in [1, -1]:
            for i in range(1, 3):
                nx, ny = x + (dx * i * sentido), y + (dy * i * sentido)
                if 0 <= nx < 6 and 0 <= ny < 5:
                    if tabuleiro_logico[ny * 6 + nx] == cor:
                        contagem += 1
                    else: break
                else: break
        if contagem >= 3: return True
    return False

def minha_peça(idx, page: ft.Page):
    servidor = page.session.store.get("sou_servidor")
    tabuleiro_logico = page.session.store.get("tabuleiro_logico")

    cor = 1 if str(servidor) == "0" else 2

    if tabuleiro_logico[idx] == cor:
        return True

    return False

def verifica_adjacencia(idx_antiga: int, idx: int):
    x_antigo, y_antigo = idx_antiga % 6, idx_antiga // 6
    x, y = idx % 6, idx // 6

    direcoes = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    dx, dy = x - x_antigo, y - y_antigo

    if (dx, dy) in direcoes:
        return True
    
    return False

def comer_peça(idx, page: ft.Page):

    board = page.session.store.get("board")
    tabuleiro_logico = page.session.store.get("tabuleiro_logico")
    pecas_colocadas = page.session.store.get("pecas_colocadas")
    
    board.controls[idx].content = None
    tabuleiro_logico[idx] = 0

    pecas_colocadas[1] -= 1
    

    

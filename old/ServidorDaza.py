# import flet as ft
# import socket
# import threading

# # --- CONFIGURAÇÃO DO SOCKET SERVIDOR ---
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('0.0.0.0', 5000)) # Escuta em todas as interfaces
# server_socket.listen(1)
    
# conn_holder = [None] # Lista para armazenar a conexão de forma mutável

# def main(page: ft.Page):
#     page.title = "Daza - SERVIDOR"
#     page.theme_mode = ft.ThemeMode.DARK
    
#     # # --- CONFIGURAÇÃO DO SOCKET SERVIDOR ---
#     # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # server_socket.bind(('0.0.0.0', 5000)) # Escuta em todas as interfaces
#     # server_socket.listen(1)
    
#     # conn_holder = [None] # Lista para armazenar a conexão de forma mutável

#     meu_turno = [True]
#     tabuleiro_logico = [0] * 30 
#     pecas_colocadas = [0]

#     def wait_for_client():
#         print("Aguardando oponente...")
#         conn, addr = server_socket.accept()
#         conn_holder[0] = conn
#         chat_messages.controls.append(ft.Text(f"Sistema: Oponente conectado de {addr[0]}", color="green"))
#         page.update()
        
#         # Inicia a escuta de dados após conectar
#         while True:
#             try:
#                 data = conn.recv(1024).decode('utf-8')
#                 print(data)
#                 if not data: break                
#                 if data.startswith("MSG:"):
#                     chat_messages.controls.append(ft.Text(f"Oponente: {data[4:]}", color=ft.Colors.RED_200))
#                     page.update()
#                 elif data.startswith("MOVE:"):
#                     meu_turno[0] = True
#                     print(f"Turno atual pós jogada do adversário: {meu_turno[0]}")
#                     idx = int(data[5:])
#                     board.controls[idx].content = ft.CircleAvatar(bgcolor=ft.Colors.RED, radius=15)
#                     tabuleiro_logico[idx] = 2
#                     pecas_colocadas[0] += 1 
#                     status_text.value = "Sua Vez..."
#                     status_text.color = ft.colors.RED_400
#                     page.update()                   
#             except:
#                 break

#     # Inicia a thread que espera o cliente
#     threading.Thread(target=wait_for_client, daemon=True).start()

#     # --- FUNÇÕES DE ENVIO ---
#     def on_cell_click(e):
#         minha_cor_id = 1
#         print(f"Turno atual antes: {meu_turno[0]}")
#         if not meu_turno[0]:
#             print("Aguarde a vez do oponente!")
#             abrir_alerta("Aguarde a vez do oponente!")
#             return
        
#         idx = board.controls.index(e.control)
#         conn = conn_holder[0]

#         if pecas_colocadas[0] < 24:
#             if valida_formacao_linha(idx, minha_cor_id):
#                 abrir_alerta("Proibido formar linha de 3 nesta fase!")
#                 return
            
#         tabuleiro_logico[idx] = 1
#         pecas_colocadas[0] += 1

#         if not e.control.content and conn:
#             e.control.content = ft.CircleAvatar(bgcolor=ft.Colors.BLUE, radius=15)
#             try:
#                 print(f"enviando: MOVE:{idx}")
#                 conn.sendall(f"MOVE:{idx}".encode('utf-8'))
#                 meu_turno[0] = False 
#                 status_text.value = "Vez do Oponente..."
#                 status_text.color = ft.Colors.RED_400
#                 print(f"Turno atual depois: {meu_turno[0]}")
#             except:
#                 print("Erro ao enviar jogada")
#             page.update()

#     def send_chat(e):
#         conn = conn_holder[0]
#         if chat_input.value and conn:
#             try:
#                 conn.send(f"MSG:{chat_input.value}".encode('utf-8'))
#                 chat_messages.controls.append(ft.Text(f"Você: {chat_input.value}", color=ft.Colors.BLUE_200))
#                 chat_input.value = ""
#                 page.update()
#             except:
#                 print("Erro ao enviar mensagem")

#     def valida_formacao_linha(idx, cor):
#         # Coordenadas X (coluna) e Y (linha)
#         x = idx % 6
#         y = idx // 5

#         # Direções para verificar: (dx, dy) -> Horizontal, Vertical, Diagonais
#         direcoes = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
#         for dx, dy in direcoes:
#             contagem = 1 # A peça que acabei de colocar
            
#             # Verifica em dois sentidos (ex: para frente e para trás na horizontal)
#             for sentido in [1, -1]:
#                 for i in range(1, 3): # Checa até 2 casas de distância
#                     nx, ny = x + (dx * i * sentido), y + (dy * i * sentido)
                    
#                     # Verifica se está dentro do tabuleiro
#                     if 0 <= nx < 6 and 0 <= ny < 5:
#                         if tabuleiro_logico[ny * 5 + nx] == cor:
#                             contagem += 1
#                         else:
#                             break
#                     else:
#                         break
            
#             if contagem >= 3:
#                 return True # Formou linha de 3!
                
#         return False # Movimento válido

#     # --- INTERFACE ---
#     chat_messages = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=150, width=float("inf"))

#     chat_container = ft.Container(
#         content=chat_messages,
#         height=300, # Aumente a altura para ficar proporcional ao tabuleiro
#         expand=True, # Faz o container esticar horizontalmente
#         border_radius=10,
#         padding=10,
#     )

#     alerta_dialogo = ft.AlertDialog(
#         title=ft.Text("Movimento Inválido"),
#         content=ft.Text("Você não pode realizar esse movimento!"),
#         on_dismiss=lambda e: print("Alerta fechado")
#     )    

#     # Função auxiliar para abrir o alerta com mensagens diferentes
#     def abrir_alerta(mensagem):
#         alerta_dialogo.content = ft.Text(mensagem)
#         page.dialog = alerta_dialogo
#         alerta_dialogo.open = True
#         page.update()

#     board = ft.GridView(expand=False, runs_count=6, width=300, height=300, spacing=5)
    
#     for i in range(30):
#         board.controls.append(
#             ft.Container(bgcolor="white10", border_radius=5, on_click=on_cell_click, data=i)
#         )

#     chat_input = ft.TextField(label="Mensagem", on_submit=send_chat, expand=True)

#     status_text = ft.Text(value="Iniciando jogo... Sua Vez!" if meu_turno else "Iniciando jogo... Vez do oponente!", color="amber")

#     page.add(
#         ft.Text("Daza Online (SERVER)", size=20, weight="bold"),
#         ft.Text("Aguardando conexão na porta 5000...", italic=True, size=12),
#         status_text,
#         board,
#         ft.Divider(),
#         chat_container,
#         ft.Row([chat_input, ft.IconButton(ft.Icons.SEND, on_click=send_chat)])
#     )

# # Use ft.app(target=main) para rodar o Flet
# ft.run(main)

import flet as ft
import socket
import threading

# --- PROTEÇÃO GLOBAL (FORA DA MAIN) ---
socket_ouvinte = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_ouvinte.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_ouvinte.bind(('0.0.0.0', 5000))
socket_ouvinte.listen(1)

conn_holder = [None]
thread_iniciada = False
meu_turno = [True] 
tabuleiro_logico = [0] * 30 
pecas_colocadas = [0]

def main(page: ft.Page):
    global thread_iniciada
    page.title = "Daza - SERVIDOR"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800

    # --- LÓGICA DE RECEBIMENTO ---
    def wait_for_client():
        print("Aguardando oponente...")
        conn, addr = socket_ouvinte.accept()
        conn_holder[0] = conn
        chat_messages.controls.append(ft.Text(f"Sistema: Oponente conectado!", color="green"))
        page.update()
        
        while True:
            try:
                raw_data = conn.recv(1024).decode('utf-8')
                if not raw_data: break
                
                # Trata mensagens grudadas pelo \n
                for data in raw_data.split('\n'):
                    if not data: continue
                    
                    if data.startswith("MSG:"):
                        chat_messages.controls.append(ft.Text(f"Oponente: {data[4:]}", color=ft.Colors.RED_200))
                    elif data.startswith("MOVE:"):
                        idx = int(data[5:])
                        meu_turno[0] = True
                        board.controls[idx].content = ft.CircleAvatar(bgcolor=ft.Colors.RED, radius=15)
                        tabuleiro_logico[idx] = 2
                        pecas_colocadas[0] += 1 
                        status_text.value = "Sua Vez!"
                        status_text.color = ft.Colors.GREEN_400
                    page.update()
            except:
                break

    if not thread_iniciada:
        threading.Thread(target=wait_for_client, daemon=True).start()
        thread_iniciada = True

    # --- VALIDAÇÃO ---
    def valida_formacao_linha(idx, cor):
        x, y = idx % 6, idx // 6
        direcoes = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in direcoes:
            contagem = 1
            for sentido in [1, -1]:
                for i in range(1, 3):
                    nx, ny = x + (dx * i * sentido), y + (dy * i * sentido)
                    if 0 <= nx < 6 and 0 <= ny < 5:
                        if tabuleiro_logico[ny * 6 + nx] == cor: # Corrigido para 6
                            contagem += 1
                        else: break
                    else: break
            if contagem >= 3: return True
        return False

    # --- COMPONENTES ---
    status_text = ft.Text(value="Aguardando Oponente...", color="amber", weight="bold")
    chat_messages = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def on_cell_click(e):
        idx = e.control.data
        if not meu_turno[0] or tabuleiro_logico[idx] != 0 or not conn_holder[0]:
            return

        if pecas_colocadas[0] < 24 and valida_formacao_linha(idx, 1):
            page.show_dialog(ft.SnackBar(ft.Text("Proibido linha de 3 agora!")))
            page.update()
            return

        e.control.content = ft.CircleAvatar(bgcolor=ft.Colors.BLUE, radius=15)
        tabuleiro_logico[idx] = 1
        pecas_colocadas[0] += 1
        conn_holder[0].sendall(f"MOVE:{idx}\n".encode('utf-8'))
        meu_turno[0] = False 
        status_text.value = "Vez do Oponente..."
        status_text.color = ft.Colors.RED_400
        page.update()

    board = ft.GridView(runs_count=6, width=300, height=260, spacing=5)
    for i in range(30):
        board.controls.append(ft.Container(bgcolor="white10", on_click=on_cell_click, data=i, border_radius=5))

    chat_input = ft.TextField(label="Mensagem", expand=True, on_submit=lambda _: send_chat(None))

    def send_chat(e):
        if chat_input.value and conn_holder[0]:
            conn_holder[0].sendall(f"MSG:{chat_input.value}\n".encode('utf-8'))
            chat_messages.controls.append(ft.Text(f"Você: {chat_input.value}", color=ft.Colors.BLUE_200))
            chat_input.value = ""
            page.update()

    page.add(
        ft.Text("DAZA - SERVIDOR", size=20, weight="bold"),
        status_text,
        ft.Container(board, alignment=ft.Alignment.CENTER),
        ft.Divider(),
        ft.Container(chat_messages, expand=True, bgcolor=ft.Colors.BLACK12, padding=10, border_radius=10),
        ft.Row([chat_input, ft.IconButton(ft.Icons.SEND, on_click=send_chat)])
    )

ft.app(target=main)
import flet as ft
import socket
import threading
import time

def iniciar_conexao(servidor, IP: str, Port: int):
    # Força a exibição imediata para sabermos que a função FOI chamada
    print("\n" + "="*30)
    print(f"FUNÇÃO CHAMADA!")
    print(f"Recebi servidor: {servidor} (Tipo: {type(servidor)})")
    print("="*30 + "\n")

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if str(servidor) == "0": 
        print(">>> SUCESSO: Entrando no bloco SERVIDOR")
        try:
            print(f"Tentando BIND em {IP}:{Port}...")
            my_socket.bind((IP, Port))
            my_socket.listen(1)
            print(f"Servidor ouvindo em {IP}:{Port}...")
            conn, addr = my_socket.accept()
            return conn
        except Exception as e:
            print(f"ERRO DENTRO DO BIND/ACCEPT: {e}")
            return None
            
    elif str(servidor) == "1":
        print(">>> SUCESSO: Entrando no bloco CLIENTE")
        destino = '127.0.0.1' if IP == '0.0.0.0' else IP
        tentativas = 0
        while tentativas <= 10:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                print(f"Tentativa {tentativas + 1}: Conectando em {destino}:{Port}...")
                my_socket.connect((destino, Port))
                print(">>> CONECTADO COM SUCESSO!")
                return my_socket
            except Exception as e:
                tentativas += 1
                print(f"Servidor não encontrado. Tentando novamente em 2 segundos... ({e})")
                time.sleep(2)
        return None
    else:
        print(f">>> ALERTA: O valor '{servidor}' não é 0 nem 1!")
        return None
    
def conectar_em_background(page: ft.Page, on_click):

    ip = page.session.store.get("ip_servidor")
    porta = page.session.store.get("porta_servidor")
    sou_servidor = page.session.store.get("sou_servidor")

    status_text = page.session.store.get("status_text")

    try:
        socket_ativo = iniciar_conexao(sou_servidor, ip, int(porta))           
        if socket_ativo:
            page.session.store.set("socket_ativo", socket_ativo)
            status_text.value = "Oponente conectado! Sua vez." if str(sou_servidor) == "0" else "Conectado! Vez do Oponente."
            status_text.color = "green"

            if not page.session.store.get("thread_iniciada"):
                threading.Thread(
                    target=wait_for_client, 
                    args=(page, on_click),
                    daemon=True).start()
                page.session.store.set("thread_iniciada", True)    

            try:
                page.update()
            except Exception as e:
                print(f"Aviso: Não foi possível atualizar a UI (Página pode ter sido fechada): {e}")
        else:
            status_text.value = "Falha na conexão. Tente novamente."
            status_text.color = "red"
            page.update()
            
    except Exception as e:
        print(f"Erro capturado na thread de conexão: {e}")

def wait_for_client(page: ft.Page, on_click):

    socket_ativo = page.session.store.get("socket_ativo")
    servidor = page.session.store.get("sou_servidor")

    status_text = page.session.store.get("status_text")
    board = page.session.store.get("board")
    chat_messages = page.session.store.get("chat_messages")

    meu_turno = page.session.store.get("meu_turno")
    tabuleiro_logico = page.session.store.get("tabuleiro_logico")
    pecas_colocadas = page.session.store.get("pecas_colocadas")
    
    while True:
        try:
            raw_data = socket_ativo.recv(1024).decode('utf-8')
            if not raw_data: break         
            
            for data in raw_data.split('\n'):
                if not data: continue

                if data.startswith("MSG:"):
                    chat_messages.controls.append(ft.Text(f"Oponente: {data[4:]}", color=ft.Colors.RED_200))
                
                elif data.startswith("ADD:"):
                    idx = int(data[4:])
                    meu_turno[0] = True
                    board.controls[idx].content = ft.CircleAvatar(bgcolor=ft.Colors.RED if str(servidor) == "0" else ft.Colors.BLUE, radius=15)
                    tabuleiro_logico[idx] = 2 if str(servidor) == "0" else 1 
                    pecas_colocadas[1] += 1 
                    if (pecas_colocadas[0] + pecas_colocadas[1]) == 24:
                        page.session.store.set("fase", 2)
                    status_text.value = "Sua Vez!" if (pecas_colocadas[0] + pecas_colocadas[1]) != 24 else "Fase de movimentações! Sua Vez."
                    status_text.color = ft.Colors.GREEN_400
                
                elif data.startswith("MOVE:"):
                    idx_antigo, idx = [int(i) for i in data[5:].split("-")]
                    board.controls[idx_antigo].content = None
                    board.controls[idx].content = ft.CircleAvatar(bgcolor=ft.Colors.RED if str(servidor) == "0" else ft.Colors.BLUE, radius=15)
                    tabuleiro_logico[idx_antigo] = 0
                    tabuleiro_logico[idx] = 2 if str(servidor) == "0" else 1
                    meu_turno[0] = True
                    status_text.value = "Sua Vez!"
                    status_text.color = ft.Colors.GREEN_400

                elif data.startswith("MOVEAT:"):
                    idx_antigo, idx, idx_comido = [int(i) for i in data[7:].split("-")]
                    board.controls[idx_antigo].content = None
                    board.controls[idx].content = ft.CircleAvatar(bgcolor=ft.Colors.RED if str(servidor) == "0" else ft.Colors.BLUE, radius=15)
                    tabuleiro_logico[idx_antigo] = 0
                    tabuleiro_logico[idx] = 2 if str(servidor) == "0" else 1
                    board.controls[idx_comido].content = None
                    tabuleiro_logico[idx_comido] = 0
                    pecas_colocadas[0] -= 1
                    if pecas_colocadas[0] <= 2:   
                        meu_turno[0] = False
                        status_text.value = "Fim de jogo. Você Perdeu!!"
                        status_text.color = ft.Colors.RED_400
                    else:
                        meu_turno[0] = True
                        status_text.value = "Sua Vez!"
                        status_text.color = ft.Colors.GREEN_400
                
                elif data.startswith("EXIT"):
                    print("Pediu pra sair")
                    mostrar_aviso_vitoria(page, on_click)
                    
                page.update()
        
        except Exception as e:
            print(f"Erro no recebimento: {e}")
            break

def abandonar_partida(e, page: ft.Page, on_click):

    socket_ativo = page.session.store.get("socket_ativo")
    if socket_ativo:
        try:
            # Envia um aviso de saída ao oponente antes de fechar
            socket_ativo.sendall("MSG:O oponente desistiu.\n".encode('utf-8'))
            time.sleep(1)
            socket_ativo.sendall("EXIT\n".encode('utf-8'))
            socket_ativo.close()
        except:
            pass

    page.session.store.clear()

    page.pop_dialog()
    
    page.run_task(on_click)

def mostrar_aviso_vitoria(page: ft.Page, on_click):
    def fechar_e_voltar(e):
        page.pop_dialog()
        page.session.store.clear()
        page.run_task(on_click)

    aviso_dialog = ft.AlertDialog(
        modal=True,
        content_padding=0,
        content=ft.Container(
            content=ft.Column(
                [
                    #ft.Text("Você Venceu!", size=24),
                    ft.Text("O oponente abandonou a partida", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.TextButton(content=ft.Text("Voltar para o início", color="#00FF00"), on_click=fechar_e_voltar),
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

    page.show_dialog(aviso_dialog)
    page.update()

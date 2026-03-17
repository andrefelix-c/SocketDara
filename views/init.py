import flet as ft

def init_view(page: ft.Page, on_click):

    cor_label = "#BBBBBB"
    cor_hint = "#555555"     
    cor_focus = "#00FF00"    

    txt_conn = ft.TextField(
        label="Digite o IP do servidor", 
        hint_text="Ex: 0.0.0.0",
        value="0.0.0.0", 
        border=ft.Border.all(1, ft.Colors.WHITE), 
        bgcolor="#1E1E1E",
        label_style=ft.TextStyle(
            color=cor_label,
            size=14,
        ),
        hint_style=ft.TextStyle(
            color=cor_hint,
        ),
        focused_color=cor_focus,
        focused_border_color=cor_focus,
        border_radius=10,
        border_color="#333333",
    )

    txt_adress = ft.TextField(
        label="Digite a porta do servidor", 
        value="8080",
        hint_text="Ex: 8000", 
        border=ft.Border.all(1, ft.Colors.WHITE), 
        bgcolor="#1E1E1E",
        label_style=ft.TextStyle(
            color=cor_label,
            size=14,
        ),
        hint_style=ft.TextStyle(
            color=cor_hint,
        ),
        focused_color=cor_focus,
        focused_border_color=cor_focus,
        border_radius=10,
        border_color="#333333",
    )
    
    opcoes_conexao = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value=0, label="Servidor", active_color=cor_focus),
            ft.Radio(value=1, label="Cliente", active_color=cor_focus),
        ], 
        alignment=ft.MainAxisAlignment.CENTER)
    )

    lbl_resultado = ft.Text(
        size=10, 
        weight=ft.FontWeight.W_300, 
        color=ft.Colors.RED_900, 
        visible=False,
        text_align=ft.TextAlign.CENTER
    )

    async def enviar_clique(e):
        if not txt_conn.value or not txt_adress.value or not opcoes_conexao.value:
            lbl_resultado.value = "Por favor, preencha todos os campos e selecione a função!"
            lbl_resultado.color = ft.Colors.RED
            lbl_resultado.visible = True
            page.update()
        else:
            page.session.store.set("ip_servidor", txt_conn.value)
            page.session.store.set("porta_servidor", txt_adress.value)
            page.session.store.set("sou_servidor", opcoes_conexao.value)
            await on_click(e)
        
    form_container = ft.Container(
         content=ft.Column(
              controls=[
                   ft.Text("🕹️ Dara", size=32, weight="bold"),
                   ft.Text("Escolha sua função na conexão", size=14, weight=ft.FontWeight.NORMAL),
                   opcoes_conexao,
                   ft.Text("Defina suas configurações de conexão", size=14, weight=ft.FontWeight.NORMAL),
                   ft.Text("Se você for o servidor deve escrever os dados da sua conexão, se for o cliente, os dados do servidor", size=10, weight=ft.FontWeight.W_300, text_align=ft.TextAlign.CENTER),
                   txt_conn,
                   txt_adress,
                   lbl_resultado,
                   ft.Button(
                        "Play!", 
                        on_click=enviar_clique,
                        bgcolor="#1E1E1E",
                        width=float("inf"),
                        style=ft.ButtonStyle(
                            color=ft.Colors.GREY_100,
                            shape=ft.RoundedRectangleBorder(radius=8), # 8 é um valor sutil e elegante
                            side=ft.BorderSide(2, "#00FF00"),
                        ),
                    ),
              ],
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              spacing=15,
         ),
        width=350,
        padding=40,
        bgcolor=ft.Colors.with_opacity(1, "#1E1E1E"),
        border=ft.Border.all(1, "#333333"),
        border_radius=15,
        shadow=ft.BoxShadow(
                blur_radius=25,          # Sombra bem esfumaçada
                spread_radius=-5,        # Retrai a sombra para não parecer um borrão sujo
                color=ft.Colors.with_opacity(0.4, "#000000"), # Sombra base
                offset=ft.Offset(0, 10),
            ),
    )

    return ft.View(
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route="/",
        controls=[
            form_container
        ],
    )


# def game_view(page):
#     return ft.View(
#         "/game",
#         controls=[
#             ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.BLUE_400),
#             ft.Text("Esta é a página inicial", size=25),
#             ft.ElevatedButton("Ir para Login", on_click=lambda _: page.go("/login")),
#         ],
#     )

def homePage(page: ft.Page, open_settings):

    def fechar_dialogo(e):
        print(confirm_dialog.open)
        confirm_dialog.open = False
        print(confirm_dialog.open)
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True, # Impede fechar clicando fora
        title=ft.Text("Confirmação"),
        content=ft.Text("Deseja realmente excluir este item?"),
        actions=[
            ft.TextButton("Sim", on_click=fechar_dialogo),
            ft.TextButton("Não", on_click=fechar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(confirm_dialog)

    def abrir_dialogo(e):
            print(confirm_dialog.open)
            # page.overlay.append(confirm_dialog)
            confirm_dialog.open = True
            print(confirm_dialog.open)
            page.update()

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(title=ft.Text("Flet app")),
            ft.Button("Excluir algo", on_click=abrir_dialogo),
            ft.Button("Go to settings", on_click=open_settings),
        ],
    )